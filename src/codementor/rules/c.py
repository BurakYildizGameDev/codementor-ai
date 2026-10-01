"""C kuralları (mimari §8.2)."""

from __future__ import annotations

import re

from tree_sitter import Node

from codementor.analysis._symbols import declarator_name, line, operator_of, text
from codementor.analysis.parsers import iter_nodes
from codementor.models.enums import AuditCategory, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_UNSAFE_BUFFER = frozenset({"gets", "strcpy", "strcat", "sprintf", "vsprintf"})
_ALLOCATORS = frozenset({"malloc", "calloc"})
# İşaretçiyi sahiplenmediği bilinen standart fonksiyonlar; başka bir fonksiyona geçirilen
# işaretçi "sahiplik aktarıldı" sayılır (fonksiyonlar arası analiz yok, mimari §8.2).
NON_OWNING = frozenset(
    {
        "memset",
        "memcpy",
        "memmove",
        "memcmp",
        "strcpy",
        "strncpy",
        "strcat",
        "strncat",
        "strlen",
        "strcmp",
        "strncmp",
        "strchr",
        "strrchr",
        "strstr",
        "printf",
        "fprintf",
        "sprintf",
        "snprintf",
        "scanf",
        "sscanf",
        "fscanf",
        "fgets",
        "gets",
        "puts",
        "fputs",
        "fread",
        "fwrite",
        "qsort",
        "assert",
    }
)
_DECLARATIONS = frozenset({"declaration", "parameter_declaration"})
_VALUE_NODES = frozenset(
    {"subscript_expression", "field_expression", "sizeof_expression", "unary_expression"}
)
_COMPARISONS = frozenset({"==", "!=", "<", ">", "<=", ">=", "&&", "||"})


@register_rule
class UnsafeBufferFunction(Rule):
    """C-BUF-001: sınır denetimi yapmayan metin/tampon fonksiyonları."""

    id = "C-BUF-001"
    title = "Sınır denetimsiz tampon fonksiyonu"
    description = (
        "`gets`, `strcpy`, `strcat` ve `sprintf` hedef tamponun boyutunu bilmez; "
        "girdi tampondan uzunsa bellek taşar. Hedefin kaç bayt aldığını nereden biliyorsun?"
    )
    languages = frozenset({Language.C})
    category = AuditCategory.MEMORY_SAFETY
    default_severity = Severity.HIGH

    def check(self, ctx: RuleContext) -> list[Finding]:
        return [self.finding(ctx, c.line) for c in ctx.facts.calls if c.name in _UNSAFE_BUFFER]


def unwrap_call(node: Node | None) -> Node | None:
    """`(int *)malloc(...)`, `(malloc(...))` → çağrı düğümü."""
    while node is not None and node.type in ("cast_expression", "parenthesized_expression"):
        node = node.child_by_field_name("value") or next(iter(node.named_children), None)
    return node


def callee_name(node: Node) -> str:
    """Çağrılan fonksiyonun adı; yalın ad değilse boş (uzun ifadenin metni alınmaz)."""
    fn = node.child_by_field_name("function")
    return text(fn) if fn is not None and fn.type == "identifier" else ""


def _is_alloc(node: Node | None) -> bool:
    return node is not None and node.type == "call_expression" and callee_name(node) in _ALLOCATORS


def _value_only(node: Node) -> bool:
    """İşaretçinin kendisini değil ondan türetilen bir değeri üreten ifade (`p[0]`, `p->x`,
    `*p`, `p == NULL`, `sizeof *p`): içindeki ad dışarı kaçmış sayılmaz."""
    if node.type in _VALUE_NODES:
        return True
    if node.type == "binary_expression":
        return operator_of(node) in _COMPARISONS
    return node.type == "pointer_expression" and operator_of(node) == "*"


class _Owners:
    """Bir fonksiyondaki `malloc`/`calloc` sonuçlarının yerel değişkenlere bağlanışı.

    Ağaç açık yığınla tek geçişte gezilir (O(düğüm); iç içe `g(g(g(p)))` ya da
    `s->a = s->a = ... p` girdisinde karesel süre yok, mimari §12). Her düğüm "kaçış
    bağlamında mı" bayrağını taşır: `return`, tahsis olmayan atama/ilk değerin sağ tarafı,
    `free` ya da sahiplenmediği bilinmeyen bir fonksiyonun argümanı. Bu bağlamdaki adlar
    serbest bırakılmış/sahipliği aktarılmış sayılır (muhafazakâr: yanlış bulgu yerine kaçırma).
    """

    def __init__(self, fn: Node) -> None:
        self.locals = {
            text(name)
            for n in iter_nodes(fn)
            if n.type in _DECLARATIONS
            for d in n.children_by_field_name("declarator")
            if (name := declarator_name(d)) is not None and name.type == "identifier"
        }
        self.allocs: dict[str, list[int]] = {}  # değişken → tahsis satırları
        self.released: set[str] = set()  # free edilen, dışarı verilen ya da takma adlanan
        stack: list[tuple[Node, bool]] = [(fn, False)]
        while stack:
            node, escaping = stack.pop()
            if node.type == "identifier":
                if escaping:
                    self.released.add(text(node))
                continue
            stack.extend(reversed(self._children(node, escaping)))

    def _bind(self, target: Node | None, value: Node) -> None:
        if target is not None and target.type == "identifier" and text(target) in self.locals:
            self.allocs.setdefault(text(target), []).append(line(value))
        # alan, `*out`, dizi elemanı veya global: sahiplik başka yerde; bulgu yok

    def _children(self, node: Node, escaping: bool) -> list[tuple[Node, bool]]:
        kind = node.type
        if kind == "init_declarator":
            target = declarator_name(node.child_by_field_name("declarator"))
            return self._assign(target, node.child_by_field_name("value"), node, escaping)
        if kind == "assignment_expression" and operator_of(node) == "=":
            target = node.child_by_field_name("left")
            return self._assign(target, node.child_by_field_name("right"), node, escaping)
        if kind == "return_statement":
            return [(c, True) for c in node.named_children]
        if kind == "call_expression":
            owning = callee_name(node) not in NON_OWNING | _ALLOCATORS  # `free` dahil
            return [(c, owning and c.type == "argument_list") for c in node.named_children]
        if _value_only(node):
            return [(c, False) for c in node.named_children]
        return [(c, escaping) for c in node.named_children]

    def _assign(
        self, target: Node | None, value: Node | None, node: Node, escaping: bool
    ) -> list[tuple[Node, bool]]:
        if value is not None and _is_alloc(unwrap_call(value)):
            self._bind(target, value)
            flag = False  # tahsis argümanları (`sizeof *p`) kaçış değil
        else:
            flag = True  # `q = p`, `head = node`, `{ p, n }`: takma ad → izlenmez
        return [(c, flag if c == value else False) for c in node.named_children]

    def leaked_lines(self) -> list[int]:
        return [n for var, lines in self.allocs.items() if var not in self.released for n in lines]


@register_rule
class MallocWithoutFree(Rule):
    """C-MEM-001: fonksiyon içinde serbest bırakılmayan ve dışarı verilmeyen tahsis."""

    id = "C-MEM-001"
    title = "Serbest bırakılmayan bellek"
    description = (
        "Bu fonksiyonda `malloc`/`calloc` ile ayrılan bellek ne `free` ediliyor ne de "
        "fonksiyondan dışarı veriliyor. Fonksiyon bittiğinde bu bellek kimde kalıyor?"
    )
    languages = frozenset({Language.C})
    category = AuditCategory.RESOURCE_LEAK
    default_severity = Severity.HIGH

    def check(self, ctx: RuleContext) -> list[Finding]:
        owners = {a.function for a in ctx.facts.allocations if a.kind.value in _ALLOCATORS}
        return [
            self.finding(ctx, n)
            for fn in ctx.function_nodes
            if fn.fact.name in owners
            for n in _Owners(fn.node).leaked_lines()
        ]


_SCANF = frozenset({"scanf", "fscanf", "sscanf"})
_LOOPS = ("for_statement", "while_statement", "do_statement")
_ASSIGNING = re.compile(r"%(?!\*)")  # `%%` önceden atılır
_READERS = frozenset({"fgets", "getline", "gets", "scanf", "fscanf", "fread", "getchar", "getc"})


@register_rule
class UncheckedScanf(Rule):
    """C-IO-001: `scanf` ailesinin dönüş değeri kullanılmıyor."""

    id = "C-IO-001"
    title = "scanf dönüş değeri denetlenmiyor"
    description = (
        "`scanf` kaç alanı başarıyla okuduğunu döndürür ama bu değer kullanılmıyor. "
        "Kullanıcı sayı yerine harf girerse ya da girdi biterse değişkende ne olur?"
    )
    languages = frozenset({Language.C})
    category = AuditCategory.INPUT_HANDLING
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        if not any(c.name in _SCANF for c in ctx.facts.calls):
            return []
        # Dönüş değeri atılan çağrı: deyimin kendisi çağrı. `(void)scanf(...)` bilinçli
        # atmadır (cast_expression); koşul, atama ve karşılaştırma içindekiler denetlenmiş sayılır.
        found: list[Finding] = []
        for stmt in ctx.nodes_in(ctx.root, "expression_statement"):
            call = next(iter(stmt.named_children), None)
            while call is not None and call.type == "parenthesized_expression":
                call = next(iter(call.named_children), None)
            if (
                call is not None
                and call.type == "call_expression"
                and callee_name(call) in _SCANF
                and _assigns(call)
            ):
                found.append(self.finding(ctx, line(call)))
        return found


def _assigns(call: Node) -> bool:
    """Biçim metninde atama yapan dönüşüm var mı (`%*[^\\n]`, `%*c` yalnızca girdiyi atar).

    Biçim metin sabiti değilse (değişken) atama yaptığı varsayılır.
    """
    args = call.child_by_field_name("arguments")
    index = 0 if callee_name(call) == "scanf" else 1  # fscanf/sscanf: önce akış/kaynak
    fmt = args.named_child(index) if args is not None and args.named_child_count > index else None
    if fmt is None or fmt.type != "string_literal" or fmt.end_byte - fmt.start_byte > 200:
        return True
    return _ASSIGNING.search(text(fmt).replace("%%", "")) is not None


@register_rule
class FlushStdin(Rule):
    """C-UB-001: `fflush(stdin)`."""

    id = "C-UB-001"
    title = "fflush(stdin)"
    description = (
        "C standardı `fflush`'ı yalnızca çıkış akışları için tanımlar; `stdin` üzerinde "
        "davranış tanımsızdır ve derleyiciden derleyiciye değişir. Satırın geri kalanını "
        "atmak için girişten ne okuyabilirsin?"
    )
    languages = frozenset({Language.C})
    category = AuditCategory.UNDEFINED_BEHAVIOR
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        if not any(c.name == "fflush" for c in ctx.facts.calls):
            return []
        found: list[Finding] = []
        for call in ctx.nodes_in(ctx.root, "call_expression"):
            args = call.child_by_field_name("arguments")
            if (
                callee_name(call) == "fflush"
                and args is not None
                and args.named_child_count == 1
                and (arg := args.named_child(0)) is not None
                and arg.type == "identifier"
                and text(arg) == "stdin"
            ):
                found.append(self.finding(ctx, line(call)))
        return found


@register_rule
class StrlenInLoopCondition(Rule):
    """C-PERF-001: döngü koşulunda `strlen`."""

    id = "C-PERF-001"
    title = "Döngü koşulunda strlen"
    description = (
        "Döngü koşulu her turda yeniden değerlendirilir ve `strlen` her seferinde metni "
        "sonuna kadar tarar. n karakterlik bir metinde toplam kaç karakter okunur?"
    )
    languages = frozenset({Language.C})
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        if not any(c.name == "strlen" for c in ctx.facts.calls):
            return []
        found: list[Finding] = []
        for loop in ctx.nodes_in(ctx.root, *_LOOPS):
            condition = loop.child_by_field_name("condition")
            if condition is None:
                continue
            calls = _condition_calls(condition)
            # `fgets(line, ...) && strlen(line) > 1`: her turda yeni okunan metin ölçülüyor
            if not any(callee_name(c) in _READERS for c in calls):
                found += [self.finding(ctx, line(c)) for c in calls if callee_name(c) == "strlen"]
        return found


def _condition_calls(condition: Node) -> list[Node]:
    """Koşuldaki çağrılar; GNU deyim ifadesinin (`({ ... })`) gövdesine inilmez.

    Gövdedeki döngüler kendi koşullarıyla ayrıca gezilir; inilseydi iç içe deyim
    ifadelerinde aynı alt ağaç her seviyede yeniden gezilirdi (karesel süre, mimari §12).
    """
    calls: list[Node] = []
    stack = [condition]
    while stack:
        node = stack.pop()
        if node.type == "compound_statement":
            continue
        if node.type == "call_expression":
            calls.append(node)
        stack.extend(node.named_children)
    return calls
