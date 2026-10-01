"""C++ kuralları (mimari §8.2)."""

from __future__ import annotations

import re
from bisect import bisect_left
from dataclasses import dataclass

from tree_sitter import Node

from codementor.analysis._symbols import declarator_name, line, simple_name, strip_templates, text
from codementor.models.enums import (
    AllocationKind,
    AuditCategory,
    DeallocationKind,
    Language,
    Severity,
)
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_RAW_NEW = frozenset({AllocationKind.NEW, AllocationKind.NEW_ARRAY})
_RAW_DELETE = frozenset({DeallocationKind.DELETE, DeallocationKind.DELETE_ARRAY})
_MAX_TYPE_BYTES = 200  # daha uzun tip metni alınmaz (mimari §12)


@register_rule
class NakedNewDelete(Rule):
    """CPP-OWN-001: akıllı işaretçi yerine çıplak `new`/`delete`."""

    id = "CPP-OWN-001"
    title = "Çıplak new/delete"
    description = (
        "Nesnenin ömrü elle yönetiliyor. Arada bir istisna ya da erken `return` olursa "
        "`delete` çalışır mı? Sahipliği kim taşıyor?"
    )
    languages = frozenset({Language.CPP})
    category = AuditCategory.MEMORY_SAFETY
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        # placement new (`new (buf) T`) bellek ayırmaz; sahiplik sorusu yok
        placement = {
            line(n)
            for n in ctx.nodes_in(ctx.root, "new_expression")
            if n.child_by_field_name("placement") is not None
        }
        lines = [
            a.line for a in ctx.facts.allocations if a.kind in _RAW_NEW and a.line not in placement
        ]
        lines += [d.line for d in ctx.facts.deallocations if d.kind in _RAW_DELETE]
        return [self.finding(ctx, n) for n in lines]


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
