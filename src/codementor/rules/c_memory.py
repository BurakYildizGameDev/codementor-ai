"""C bellek kuralları: `realloc` deseni ve denetlenmeyen tahsis (mimari §8.2).

C-MEM-001 `c.py`'de; buradaki kurallar onun yardımcılarını (`unwrap_call`, `callee_name`) paylaşır.
"""

from __future__ import annotations

from typing import NamedTuple

from tree_sitter import Node

from codementor.analysis._symbols import declarator_name, line, operator_of, text
from codementor.models.enums import AuditCategory, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.c import NON_OWNING, callee_name, unwrap_call
from codementor.rules.registry import register_rule

_ALLOCATORS = frozenset({"malloc", "calloc", "realloc"})
_MAX_KEY_BYTES = 200  # daha uzun hedef metni alınmaz (iç içe ifadede karesel süre olmasın)
_NULLS = frozenset({"NULL", "0", "nullptr"})
_CONDITIONS = frozenset(
    {"if_statement", "while_statement", "for_statement", "do_statement", "conditional_expression"}
)
_TRANSPARENT = frozenset({"parenthesized_expression", "assignment_expression", "cast_expression"})
# Açılan sarmalayıcı sayısı sınırlı: `(((a = 0) = 0) = 0)` zincirinde her atamada baştan
# açmak karesel olurdu (mimari §12); gerçek kodda 2-3 katman yeter
_MAX_UNWRAP = 6
_EXITS = frozenset({"exit", "abort", "_Exit", "quick_exit"})
# Faz 57: denetimin deyimi; deyimi içeren blok kullanımı da kapsıyorsa denetim o yoldadır
_STATEMENTS = frozenset(
    {
        "if_statement",
        "while_statement",
        "for_statement",
        "do_statement",
        "switch_statement",
        "expression_statement",
        "return_statement",
        "declaration",
    }
)
_LOOPS = frozenset({"while_statement", "for_statement", "do_statement"})
_MAX_CARRY = 8  # yeni tahsise taşınan döngü koşulu denetimi sayısı


def _key(node: Node | None) -> str | None:
    """Ad ya da alan ifadesinin karşılaştırma anahtarı (`s->buf`); başka ifadede None.

    Parantez, atama (`(p = malloc(..))` → `p`) ve tip dönüşümü açılır.
    """
    for _ in range(_MAX_UNWRAP):
        if node is None or node.type not in _TRANSPARENT:
            break
        if node.type == "assignment_expression":
            node = node.child_by_field_name("left")
        elif node.type == "cast_expression":
            node = node.child_by_field_name("value")
        else:
            node = next(iter(node.named_children), None)
    if node is None or node.type not in ("identifier", "field_expression"):
        return None
    if node.end_byte - node.start_byte > _MAX_KEY_BYTES:
        return None
    return "".join(text(node).split())


def _alloc_call(node: Node | None) -> Node | None:
    call = unwrap_call(node)
    if call is not None and call.type == "call_expression" and callee_name(call) in _ALLOCATORS:
        return call
    return None


@register_rule
class ReallocSelfAssign(Rule):
    """C-MEM-002: `p = realloc(p, ...)` (başarısızlıkta eski blok kaybolur)."""

    id = "C-MEM-002"
    title = "realloc sonucu aynı işaretçiye atanıyor"
    description = (
        "`realloc` başarısız olursa NULL döndürür ama eski blok serbest bırakılmaz. Sonuç "
        "doğrudan aynı işaretçiye yazıldığında eski bloğun adresi nerede kalır?"
    )
    languages = frozenset({Language.C})
    category = AuditCategory.MEMORY_SAFETY
    default_severity = Severity.HIGH

    def check(self, ctx: RuleContext) -> list[Finding]:
        calls = ctx.facts.calls
        if not any(c.name == "realloc" for c in calls):
            return []
        # Başarısızlıkta program sonlanıyorsa (`exit`, `abort`) kaybolan blok önemsiz
        exiting = {c.function for c in calls if c.name in _EXITS}
        owner = {c.line: c.function for c in calls if c.name == "realloc"}
        found: list[Finding] = []
        for node in ctx.nodes_in(ctx.root, "assignment_expression"):
            call = _alloc_call(node.child_by_field_name("right"))
            if call is None or callee_name(call) != "realloc" or operator_of(node) != "=":
                continue
            if owner.get(line(call)) in exiting:
                continue
            args = call.child_by_field_name("arguments")
            first = args.named_child(0) if args is not None and args.named_child_count else None
            target = _key(node.child_by_field_name("left"))
            if target is not None and target == _key(first):
                found.append(self.finding(ctx, line(node)))
        return found


class _Context(NamedTuple):
    """Bir düğümün en yakın deyimi, deyimin durduğu blok ve en içteki döngü (Faz 57).

    Gezinti yığınında taşınır; `.parent` çağrılmaz (tree-sitter'da kökten arar, derin ağaçta
    karesel olurdu — denetim K1).
    """

    statement: Node | None
    scope: Node | None
    loop: Node | None


class _Check(NamedTuple):
    node: Node
    context: _Context


class _NullChecks:
    """Bir fonksiyonda tahsis edilen, kullanılan ve NULL'a karşı denetlenen adlar.

    Tek geçiş, açık yığın (O(düğüm)); `sizeof *p` değerlendirilmediği için atlanır.
    Faz 57: açık denetim (`if`/`while` koşulu, `!p`, `p == NULL`, `assert`) yalnız tahsisten
    sonra ve ilk kullanımdan önce yapılmışsa ve denetimin deyimi kullanımla aynı blokta
    (ya da kullanımı kapsayan deyimde) duruyorsa sayılır. Yardımcı fonksiyona geçirme
    (`die_if_null(p)`) ve takma ad (`b = p; if (!b)`) belirsizdir: sıraya bakılmaz
    (muhafazakâr: kaçırma).
    """

    def __init__(self, fn: Node) -> None:
        self.allocs: dict[str, list[Node]] = {}
        self.uses: dict[str, list[Node]] = {}
        self.checks: dict[str, list[_Check]] = {}
        self.helper_checked: set[str] = set()
        self.aliases: dict[str, list[tuple[str, Node]]] = {}
        # (düğüm, bağlamı, alt deyimlerin bloğu); ön sıra: belge sırasıyla ziyaret
        stack: list[tuple[Node, _Context, Node]] = [(fn, _Context(None, None, None), fn)]
        while stack:
            node, context, holder = stack.pop()
            if node.type == "sizeof_expression":
                continue
            self._visit(node, context)
            children = [_child(node, context, holder, c) for c in node.named_children]
            stack.extend(reversed(children))
        # adın son denetiminin bitişi (takma ad kararında O(1))
        self.last_check = {k: max(c.node.end_byte for c in cs) for k, cs in self.checks.items()}

    def _visit(self, node: Node, context: _Context) -> None:
        kind = node.type
        if kind == "init_declarator":
            name = declarator_name(node.child_by_field_name("declarator"))
            self._bind(name, node.child_by_field_name("value"))
        elif kind == "assignment_expression" and operator_of(node) == "=":
            self._bind(node.child_by_field_name("left"), node.child_by_field_name("right"))
        elif kind in _CONDITIONS:
            self._check(node.child_by_field_name("condition"), context)
        elif kind == "unary_expression" and operator_of(node) == "!":
            self._check(node.child_by_field_name("argument"), context)
        elif kind == "binary_expression":
            self._binary(node, context)
        elif kind == "call_expression":
            self._call(node, context)
        elif (
            kind == "subscript_expression"
            or (kind == "pointer_expression" and operator_of(node) == "*")
            or (kind == "field_expression" and operator_of(node) == "->")
        ):
            self._use(node.child_by_field_name("argument"))

    def _bind(self, target: Node | None, value: Node | None) -> None:
        key = _key(target)
        if key is None:
            return
        if (call := _alloc_call(value)) is not None:
            self.allocs.setdefault(key, []).append(call)
        elif value is not None and (source := _key(value)) is not None and source != key:
            # `b = a`: `a`'nın tahsisi `b` üzerinden de denetlenebilir
            self.aliases.setdefault(source, []).append((key, value))

    def _check(self, node: Node | None, context: _Context) -> None:
        if node is not None and (key := _key(node)) is not None:
            self.checks.setdefault(key, []).append(_Check(node, context))

    def _use(self, node: Node | None) -> None:
        if node is not None and (key := _key(node)) is not None:
            self.uses.setdefault(key, []).append(node)

    def _binary(self, node: Node, context: _Context) -> None:
        op = operator_of(node)
        left, right = node.child_by_field_name("left"), node.child_by_field_name("right")
        if op in ("&&", "||"):
            self._check(left, context)
            self._check(right, context)
        elif op in ("==", "!="):
            for side, other in ((left, right), (right, left)):
                # kısa düğüm sınırı: uzun ifadenin metni alınmaz
                if other is not None and other.type == "cast_expression":
                    other = other.child_by_field_name("value")  # `(void *)0`
                if (
                    other is not None
                    and other.end_byte - other.start_byte <= len("nullptr")
                    and text(other) in _NULLS
                ):
                    self._check(side, context)

    def _call(self, node: Node, context: _Context) -> None:
        callee = callee_name(node)
        args = node.child_by_field_name("arguments")
        if args is None:
            return
        if callee == "assert":
            for arg in args.named_children:
                self._check(arg, context)
        elif callee in NON_OWNING:
            for arg in args.named_children:
                self._use(arg)
        elif callee not in _ALLOCATORS and callee != "free":
            # kullanıcı fonksiyonu (`die_if_null(p)`) denetliyor olabilir: muhafazakâr
            for arg in args.named_children:
                if (key := _key(arg)) is not None:
                    self.helper_checked.add(key)

    def _uncertain(self, key: str) -> bool:
        """Yardımcıya geçen ya da takma adı denetlenen ad: sıraya bakmadan bastırılır.

        Takma ad yalnız bir kullanımdan önce kurulmuş ve kurulduktan sonra denetlenmişse
        sayılır; `cur->next = n` gibi kullanımlardan sonra yapılan bağlama, `cur->next`'in
        önceki ilgisiz denetimiyle bulguyu gizlemesin.
        """
        if key in self.helper_checked:
            return True
        last_use = max(u.start_byte for u in self.uses[key])
        for alias, node in self.aliases.get(key, []):
            if node.start_byte >= last_use:
                continue
            if alias in self.helper_checked or self.last_check.get(alias, -1) > node.start_byte:
                return True
        return False

    def unchecked_lines(self) -> list[int]:
        return [n for key in self.allocs for n in self._unchecked(key)]

    def _unchecked(self, key: str) -> list[int]:
        """Tek sıralı tarama: her tahsisin ilk kullanımı, o tahsisten sonraki denetimlerle
        karşılaştırılır. Denetimler bitiş konumuna göre sıralanır; böylece
        `if ((p = malloc(n)) == NULL)` denetimi kendi tahsisinin penceresine düşer.
        Her denetim yalnız bir pencerede değerlendirilir (O(olay); mimari §12).
        """
        uses = self.uses.get(key, [])
        if not uses or self._uncertain(key):
            return []
        events: list[tuple[int, int, Node, _Check | None]] = sorted(
            [(c.start_byte, 0, c, None) for c in self.allocs[key]]
            + [(c.node.end_byte, 1, c.node, c) for c in self.checks.get(key, [])]
            + [(u.start_byte, 2, u, None) for u in uses],
            key=lambda event: (event[0], event[1]),
        )
        found: list[int] = []
        alloc: Node | None = None
        window: list[_Check] = []
        for _, kind, node, check in events:
            if kind == 0:
                # tahsisi çevreleyen döngünün koşulu (`while (!p) p = malloc(..)`) geçerli kalır
                carried = [c for c in window if _loop_condition_around(c, node)]
                alloc, window = node, carried[:_MAX_CARRY]
            elif check is not None:
                window.append(check)
            elif alloc is not None:
                if not any(_guards(c, alloc, node) for c in window):
                    found.append(line(alloc))
                alloc = None  # yalnız ilk kullanım belirleyicidir
        return found


def _child(
    parent: Node, context: _Context, holder: Node, child: Node
) -> tuple[Node, _Context, Node]:
    """Çocuğun bağlamı ve alt deyimlerinin bloğu.

    `else if` zincirindeki iç `if` en dıştaki `if` ile aynı deyim sayılır; etiket
    (`hata: if (..)`) şeffaftır, etiketli deyim etiketin bloğunda durur.
    """
    child_holder = holder if child.type == "labeled_statement" else child
    if child.type not in _STATEMENTS or (
        child.type == "if_statement" and parent.type == "else_clause"
    ):
        return child, context, child_holder
    loop = child if child.type in _LOOPS else context.loop
    return child, _Context(child, holder, loop), child_holder


def _contains(outer: Node, inner: Node) -> bool:
    return outer.start_byte <= inner.start_byte and inner.end_byte <= outer.end_byte


def _loop_condition_around(check: _Check, alloc: Node) -> bool:
    statement = check.context.statement
    return statement is not None and statement.type in _LOOPS and _contains(statement, alloc)


def _guards(check: _Check, alloc: Node, use: Node) -> bool:
    """`check` tahsisten sonra (ya da onu çevreleyen döngünün koşulunda) ve kullanımın yolunda mı.

    Yol: denetimin deyimini içeren blok kullanımı kapsar ya da denetim, tahsisi de içeren bir
    döngünün içinde olup kullanım döngüden sonradır (`while (1) { p = malloc(n); if (p)
    break; }`). Deyim bilinmiyorsa muhafazakâr davranılır: denetim sayılır.
    """
    statement, scope, loop = check.context
    if statement is None or scope is None:
        return True
    after = check.node.end_byte > alloc.start_byte or _loop_condition_around(check, alloc)
    if not after:
        return False
    if _contains(scope, use):
        return True
    return loop is not None and _contains(loop, alloc) and use.start_byte >= loop.end_byte


@register_rule
class UncheckedAllocation(Rule):
    """C-MEM-003: `malloc` dönüşü NULL'a karşı denetlenmeden kullanılıyor."""

    id = "C-MEM-003"
    title = "Tahsis sonucu NULL denetimi yok"
    description = (
        "`malloc`/`calloc`/`realloc` bellek ayıramazsa NULL döndürür. Bu işaretçi "
        "denetlenmeden kullanılıyor; tahsis başarısız olursa bu satırdan sonra ne olur?"
    )
    languages = frozenset({Language.C})
    category = AuditCategory.MEMORY_SAFETY
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        owners = {c.function for c in ctx.facts.calls if c.name in _ALLOCATORS}
        return [
            self.finding(ctx, n)
            for fn in ctx.function_nodes
            if fn.fact.name in owners
            for n in _NullChecks(fn.node).unchecked_lines()
        ]
