"""C bellek kuralları: `realloc` deseni ve denetlenmeyen tahsis (mimari §8.2).

C-MEM-001 `c.py`'de; buradaki kurallar onun yardımcılarını (`unwrap_call`, `callee_name`) paylaşır.
"""

from __future__ import annotations

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


class _NullChecks:
    """Bir fonksiyonda tahsis edilen, kullanılan ve NULL'a karşı denetlenen adlar.

    Tek geçiş, açık yığın (O(düğüm)); `sizeof *p` değerlendirilmediği için atlanır.
    Denetimin kullanımdan önce mi sonra mı yapıldığına bakılmaz (muhafazakâr: kaçırma).
    """

    def __init__(self, fn: Node) -> None:
        self.allocs: dict[str, list[int]] = {}
        self.used: set[str] = set()
        self.checked: set[str] = set()
        stack = [fn]
        while stack:
            node = stack.pop()
            if node.type == "sizeof_expression":
                continue
            self._visit(node)
            stack.extend(reversed(node.named_children))

    def _visit(self, node: Node) -> None:
        kind = node.type
        if kind == "init_declarator":
            name = declarator_name(node.child_by_field_name("declarator"))
            self._bind(name, node.child_by_field_name("value"))
        elif kind == "assignment_expression" and operator_of(node) == "=":
            self._bind(node.child_by_field_name("left"), node.child_by_field_name("right"))
        elif kind in _CONDITIONS:
            self._check(node.child_by_field_name("condition"))
        elif kind == "unary_expression" and operator_of(node) == "!":
            self._check(node.child_by_field_name("argument"))
        elif kind == "binary_expression":
            self._binary(node)
        elif kind == "call_expression":
            self._call(node)
        elif (
            kind == "subscript_expression"
            or (kind == "pointer_expression" and operator_of(node) == "*")
            or (kind == "field_expression" and operator_of(node) == "->")
        ):
            self._use(node.child_by_field_name("argument"))

    def _bind(self, target: Node | None, value: Node | None) -> None:
        call = _alloc_call(value)
        if call is not None and (key := _key(target)) is not None:
            self.allocs.setdefault(key, []).append(line(call))

    def _check(self, node: Node | None) -> None:
        if (key := _key(node)) is not None:
            self.checked.add(key)

    def _use(self, node: Node | None) -> None:
        if (key := _key(node)) is not None:
            self.used.add(key)

    def _binary(self, node: Node) -> None:
        op = operator_of(node)
        left, right = node.child_by_field_name("left"), node.child_by_field_name("right")
        if op in ("&&", "||"):
            self._check(left)
            self._check(right)
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
                    self._check(side)

    def _call(self, node: Node) -> None:
        callee = callee_name(node)
        args = node.child_by_field_name("arguments")
        if args is None:
            return
        if callee == "assert":
            for arg in args.named_children:
                self._check(arg)
        elif callee in NON_OWNING:
            for arg in args.named_children:
                self._use(arg)
        elif callee not in _ALLOCATORS and callee != "free":
            # kullanıcı fonksiyonu (`die_if_null(p)`) denetliyor olabilir: muhafazakâr
            for arg in args.named_children:
                self._check(arg)

    def unchecked_lines(self) -> list[int]:
        return [
            n
            for key, lines in self.allocs.items()
            if key in self.used and key not in self.checked
            for n in lines
        ]


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
