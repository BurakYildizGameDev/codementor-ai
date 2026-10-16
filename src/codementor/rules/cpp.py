"""C++ kuralları (mimari §8.2)."""

from __future__ import annotations

import re
from bisect import bisect_left, bisect_right
from dataclasses import dataclass

from tree_sitter import Node

from codementor.analysis._symbols import (
    declarator_name,
    line,
    operator_of,
    simple_name,
    strip_templates,
    text,
)
from codementor.models.enums import (
    AuditCategory,
    FindingKind,
    Language,
    Severity,
)
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_MAX_TYPE_BYTES = 200  # daha uzun tip metni alınmaz (mimari §12)


@register_rule
class NakedNewDelete(Rule):
    """CPP-OWN-001: akıllı işaretçi yerine çıplak `new`/`delete`.

    Aynı kapsamda aynı ada atanan tahsis ile o adın serbest bırakılması eşleşiyorsa (Faz 52)
    ömür en azından tutarlı yönetiliyor demektir → bulgu `suggestion`; eşleşmeyen tahsis ya da
    serbest bırakma `issue` kalır (başka bir işaretçinin `delete`'i sızıntıyı örtmez). Kurucu ve
    yıkıcı farklı kapsamdır (tek başına yıkıcı doğru anlamına gelmez). Eşleşse bile `new` ile
    `delete` arasında aynı kapsamda erken çıkış (`return`, `throw`, `goto`, `break`, `continue`)
    varsa `delete` atlanabilir: bulgu yine `issue` olur (Faz H2).
    """

    id = "CPP-OWN-001"
    title = "Çıplak new/delete"
    description = (
        "Nesnenin ömrü elle yönetiliyor. Arada bir istisna ya da erken `return` olursa "
        "`delete` çalışır mı? Sahipliği kim taşıyor?"
    )
    languages = frozenset({Language.CPP})
    category = AuditCategory.MEMORY_SAFETY
    default_severity = Severity.MEDIUM
    catalog_note = (
        "Aynı kapsamda aynı ada atanan tahsis ile `delete` eşleşirse öneri, eşleşmezse hata. "
        "Eşleşse bile arada aynı kapsamda erken çıkış (`return`/`throw`/`goto`/`break`/"
        "`continue`) varsa `delete` atlanabilir sayıldığı için hata verilir; lambda gövdesindeki "
        "atlamalar dışarıdan çıkış sayılmaz."
    )

    def check(self, ctx: RuleContext) -> list[Finding]:
        owners: dict[int, str] = {}  # new_expression başlangıç baytı → atandığı ad
        news: list[Node] = []
        deletes: list[Node] = []
        for n in ctx.nodes_in(
            ctx.root,
            "new_expression",
            "delete_expression",
            "init_declarator",
            "assignment_expression",
            "field_initializer",
        ):
            if n.type == "new_expression":
                # placement new (`new (buf) T`) bellek ayırmaz; sahiplik sorusu yok
                if n.child_by_field_name("placement") is None:
                    news.append(n)
            elif n.type == "delete_expression":
                deletes.append(n)
            elif (target := _new_target(n)) is not None:
                owners[target[0].start_byte] = target[1]
        # Eşleşme anahtarı (kapsam, aile, ad); aileler new↔delete ve new[]↔delete[]
        allocated: dict[int, tuple[str, bool, str | None]] = {
            n.start_byte: (ctx.scope_key(line(n)), _is_array_new(n), owners.get(n.start_byte))
            for n in news
        }
        freed: dict[int, tuple[str, bool, str | None]] = {
            n.start_byte: (ctx.scope_key(line(n)), _is_array_delete(n), _owner(_deleted(n)))
            for n in deletes
        }
        alloc_keys = {key for key in allocated.values() if key[2]}
        free_keys = {key for key in freed.values() if key[2]}
        skipped = _skipped_deletes(ctx, news, deletes, allocated, freed)
        found: list[Finding] = []
        for node in sorted(news + deletes, key=lambda n: n.start_byte):
            key = allocated.get(node.start_byte) or freed[node.start_byte]
            paired = key in (free_keys if node.type == "new_expression" else alloc_keys)
            kind = (
                FindingKind.SUGGESTION
                if paired and node.start_byte not in skipped
                else FindingKind.ISSUE
            )
            found.append(self.finding(ctx, line(node), kind=kind))
        return found


_JUMPS = (
    "return_statement",
    "throw_statement",
    "goto_statement",
    "break_statement",
    "continue_statement",
)


def _jump_positions(ctx: RuleContext) -> dict[str, list[int]]:
    """Kapsam kimliği → o kapsamdan çıkabilecek atlamaların başlangıç baytları (sıralı).

    Lambda gövdesindeki atlamalar dışarıdan çıkış değildir; sayılmaz (lambda aralıkları
    iç içe ya da ayrık olduğundan en içteki aralık ikili aramayla bulunur).
    """
    lambdas = sorted(
        (n.start_byte, n.end_byte) for n in ctx.nodes_in(ctx.root, "lambda_expression")
    )
    starts = [start for start, _ in lambdas]
    positions: dict[str, list[int]] = {}
    for node in ctx.nodes_in(ctx.root, *_JUMPS):
        index = bisect_right(starts, node.start_byte) - 1
        if index >= 0 and node.start_byte < lambdas[index][1]:
            continue
        positions.setdefault(ctx.scope_key(line(node)), []).append(node.start_byte)
    return {scope: sorted(offsets) for scope, offsets in positions.items()}


def _matched_pairs(
    news: list[Node],
    deletes: list[Node],
    allocated: dict[int, tuple[str, bool, str | None]],
    freed: dict[int, tuple[str, bool, str | None]],
) -> list[tuple[Node, Node]]:
    """Sahibi belli ve anahtarı eşleşen `new`/`delete` çiftleri (belge sırasıyla)."""
    by_key: dict[tuple[str, bool, str | None], list[Node]] = {}
    for node in deletes:
        key = freed[node.start_byte]
        if key[2]:
            by_key.setdefault(key, []).append(node)
    pairs: list[tuple[Node, Node]] = []
    taken: dict[tuple[str, bool, str | None], int] = {}
    for node in news:
        key = allocated[node.start_byte]
        bucket = by_key.get(key)
        if bucket is None:
            continue
        index = taken.get(key, 0)
        while index < len(bucket) and bucket[index].start_byte < node.start_byte:
            index += 1
        if index < len(bucket):
            pairs.append((node, bucket[index]))
            taken[key] = index + 1
    return pairs


def _skips_delete(positions: list[int], new: Node, delete: Node) -> bool:
    """`new` ile `delete` arasında aynı kapsamda erken çıkış var mı (çift başına O(log n))."""
    return bisect_left(positions, delete.start_byte) > bisect_right(positions, new.start_byte)


def _skipped_deletes(
    ctx: RuleContext,
    news: list[Node],
    deletes: list[Node],
    allocated: dict[int, tuple[str, bool, str | None]],
    freed: dict[int, tuple[str, bool, str | None]],
) -> set[int]:
    """Erken çıkış yüzünden serbest bırakması atlanabilen `new`/`delete` bayt konakları.

    Eşleşen çiftin iki ucu da işaretlenir; bulgu türü ikisinde de `issue` olur (Faz H2).
    """
    positions = _jump_positions(ctx)
    skipped: set[int] = set()
    for new, delete in _matched_pairs(news, deletes, allocated, freed):
        if _skips_delete(positions.get(ctx.scope_key(line(new)), []), new, delete):
            skipped.update({new.start_byte, delete.start_byte})
    return skipped


def _owner(raw: str) -> str:
    """Sahip ifadesinin karşılaştırma biçimi: `(this->data_)` → `data_`."""
    raw = raw.replace(" ", "")
    while raw.startswith("(") and raw.endswith(")"):
        raw = raw[1:-1]
    return raw.removeprefix("this->")


def _new_target(node: Node) -> tuple[Node, str] | None:
    """`T* p = new T`, `p = new T`, `: p(new T)` → (new düğümü, sahip adı)."""
    if node.type == "init_declarator":
        value = node.child_by_field_name("value")
        name = declarator_name(node.child_by_field_name("declarator"))
    elif node.type == "assignment_expression":
        value = node.child_by_field_name("right")
        name = node.child_by_field_name("left") if operator_of(node) == "=" else None
    else:  # field_initializer: `: data_(new char[n])`
        args = next((c for c in node.named_children if c.type == "argument_list"), None)
        value = args.named_children[0] if args is not None and args.named_child_count == 1 else None
        name = next((c for c in node.named_children if c.type == "field_identifier"), None)
    if value is None or value.type != "new_expression" or name is None:
        return None
    return value, _owner(text(name))


def _deleted(node: Node) -> str:
    """`delete[] p` → `p` (son adlandırılmış çocuk)."""
    return text(node.named_children[-1]) if node.named_child_count else ""


def _is_array_new(node: Node) -> bool:
    return node.child_by_field_name("declarator") is not None


def _is_array_delete(node: Node) -> bool:
    return any(c.type == "[" for c in node.children)


_SHARED_PTR = re.compile(r"(?<![\w])shared_ptr\s*<\s*(?:const\s+)?((?:\w+\s*::\s*)*\w+)")
_BACK_POINTER = frozenset({"parent", "prev", "previous", "owner", "back"})
_WORDS = re.compile(r"[a-z]+|[A-Z][a-z]*")  # `m_parent`, `parentNode`, `backPtr` → sözcükler
# `std::function<void(std::shared_ptr<A>)>` gibi işlev tiplerindeki shared_ptr sahiplik değil
_CALLABLE = re.compile(r"(?<![\w])function\s*<|\(")
_CLASSES = ("class_specifier", "struct_specifier")


@dataclass(frozen=True)
class _Edge:
    source: str
    target: str
    field: str
    line: int


def _shared_edges(ctx: RuleContext) -> list[_Edge]:
    """Sınıf alanlarındaki `shared_ptr<T>` bağları (kapsayıcı içindekiler dahil)."""
    edges: list[_Edge] = []
    for cls in ctx.nodes_in(ctx.root, *_CLASSES):
        name, body = cls.child_by_field_name("name"), cls.child_by_field_name("body")
        if name is None or body is None:
            continue  # ileri bildirim ya da adsız yapı
        source = simple_name(text(name))
        for field in body.named_children:
            kind = field.child_by_field_name("type") if field.type == "field_declaration" else None
            if kind is None or kind.end_byte - kind.start_byte > _MAX_TYPE_BYTES:
                continue
            if _CALLABLE.search(text(kind)):
                continue
            targets = {simple_name("".join(t.split())) for t in _SHARED_PTR.findall(text(kind))}
            for declarator in field.children_by_field_name("declarator"):
                field_name = text(declarator_name(declarator) or declarator)
                edges += [_Edge(source, t, field_name, line(field)) for t in targets]
    return edges


def _components(edges: list[_Edge]) -> dict[str, int]:
    """Güçlü bağlı bileşenler (yinelemeli Tarjan; uzun zincirde özyineleme derinliği yok)."""
    graph: dict[str, list[str]] = {}
    for e in edges:
        graph.setdefault(e.source, []).append(e.target)
        graph.setdefault(e.target, [])
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    component: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    for root in graph:
        if root in index:
            continue
        work = [(root, 0)]
        while work:
            node, i = work.pop()
            if i == 0:
                index[node] = low[node] = len(index)
                stack.append(node)
                on_stack.add(node)
            neighbours = graph[node]
            if i < len(neighbours):
                work.append((node, i + 1))
                nxt = neighbours[i]
                if nxt not in index:
                    work.append((nxt, 0))
                elif nxt in on_stack:
                    low[node] = min(low[node], index[nxt])
                continue
            if low[node] == index[node]:
                while True:
                    member = stack.pop()
                    on_stack.discard(member)
                    component[member] = index[node]
                    if member == node:
                        break
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
    return component


@register_rule
class SharedPtrCycle(Rule):
    """CPP-SP-001: birbirini `shared_ptr` ile tutan sınıflar (döngüsel referans şüphesi)."""

    id = "CPP-SP-001"
    title = "Döngüsel shared_ptr şüphesi"
    description = (
        "Bu alan, kendisini de `shared_ptr` ile tutan bir nesneyi gösteriyor. İki nesne "
        "birbirini tutarsa sayaçları hiç sıfıra iner mi? Bağlardan biri sahiplik "
        "gerektirmiyorsa hangi tür daha uygun olur?"
    )
    languages = frozenset({Language.CPP})
    category = AuditCategory.RESOURCE_LEAK
    default_severity = Severity.HIGH
    confidence = 0.7  # şüphe: döngünün çalışma zamanında kurulup kurulmadığı bilinmez

    def check(self, ctx: RuleContext) -> list[Finding]:
        edges = _shared_edges(ctx)
        if not edges:
            return []
        component = _components(edges)
        found: list[Finding] = []
        for e in edges:
            if e.source == e.target:
                # öz-referans: yalnızca geri işaretçi (`parent`, `prev`) ileri bağla döngü kurar;
                # `left`/`right`/`next` tek yönlü ağaç ve listelerdir
                words = {w.lower() for w in _WORDS.findall(e.field)}
                if words & _BACK_POINTER:  # `fallback`, `preview` tek sözcük: eşleşmez
                    found.append(self.finding(ctx, e.line))
            elif component[e.source] == component[e.target]:
                found.append(self.finding(ctx, e.line))
        return found


_LARGE_TYPES = frozenset(
    {
        "vector",
        "string",
        "wstring",
        "basic_string",
        "map",
        "multimap",
        "unordered_map",
        "set",
        "multiset",
        "unordered_set",
        "list",
        "deque",
        # Unreal kapsayıcıları (motordan bağımsız C++ kuralı)
        "TArray",
        "TMap",
        "TSet",
        "FString",
    }
)
_PARAMETERS = frozenset({"parameter_declaration", "optional_parameter_declaration"})
_MOVES = frozenset({"std::move", "move"})


def _function_declarator(node: Node) -> Node | None:
    """`function_definition`'ın `function_declarator`'ı (`T* f(...)`, `T& f(...)` dahil)."""
    current = node.child_by_field_name("declarator")
    while current is not None and current.type != "function_declarator":
        current = current.child_by_field_name("declarator")
    return current


class _Kept:
    """Değerle alınmasının gerekçeli olduğu adlar: `std::move(ad)` ile taşınan ya da
    `return ad;` ile döndürülen (kopyala-değiştir-döndür) parametreler.

    Kök bir kez gezilir; fonksiyon başına bayt aralığında ikili arama yapılır (iç içe
    yerel sınıf metotlarında gövde yeniden gezilmez, mimari §12).
    """

    def __init__(self, ctx: RuleContext) -> None:
        self.positions: dict[str, list[int]] = {}
        for node in ctx.nodes_in(ctx.root, "call_expression", "return_statement"):
            arg = _kept_argument(node)
            if arg is not None:
                self.positions.setdefault(text(arg), []).append(node.start_byte)

    def within(self, name: str, fn: Node) -> bool:
        spots = self.positions.get(name, [])
        i = bisect_left(spots, fn.start_byte)
        return i < len(spots) and spots[i] < fn.end_byte


def _kept_argument(node: Node) -> Node | None:
    if node.type == "return_statement":
        value = next(iter(node.named_children), None)
        return value if value is not None and value.type == "identifier" else None
    callee, args = node.child_by_field_name("function"), node.child_by_field_name("arguments")
    if (
        callee is not None
        and callee.end_byte - callee.start_byte <= len("std::move")
        and text(callee) in _MOVES
        and args is not None
        and args.named_child_count == 1
        and (arg := args.named_child(0)) is not None
        and arg.type == "identifier"
    ):
        return arg
    return None


def _is_large(kind: Node | None) -> bool:
    if kind is None or kind.end_byte - kind.start_byte > _MAX_TYPE_BYTES:
        return False
    return strip_templates(text(kind)).removeprefix("std::").strip() in _LARGE_TYPES


@register_rule
class LargeByValueParameter(Rule):
    """CPP-PERF-001: büyük kapsayıcı/metin parametresinin değerle geçirilmesi."""

    id = "CPP-PERF-001"
    title = "Büyük nesne değerle geçiriliyor"
    description = (
        "Bu parametre değerle geçiriliyor; her çağrıda kapsayıcının tamamı kopyalanır. "
        "Fonksiyon bu kopyayı değiştirmeye ya da saklamaya ihtiyaç duyuyor mu?"
    )
    languages = frozenset({Language.CPP})
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        found: list[Finding] = []
        kept: _Kept | None = None
        for fn in ctx.nodes_in(ctx.root, "function_definition"):
            declarator = _function_declarator(fn)
            params = declarator.child_by_field_name("parameters") if declarator else None
            if params is None:
                continue
            candidates = [
                (p, text(name))
                for p in params.named_children
                if p.type in _PARAMETERS
                and (name := p.child_by_field_name("declarator")) is not None
                and name.type == "identifier"  # `&`, `&&`, `*` bildirimleri değil
                and _is_large(p.child_by_field_name("type"))
            ]
            if candidates:
                kept = kept or _Kept(ctx)
                found += [
                    self.finding(ctx, line(p))
                    for p, name in candidates
                    if not kept.within(name, fn)
                ]
        return found
