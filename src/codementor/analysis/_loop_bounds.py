"""Döngü sınırı sınıflandırması (bound/derinlik çıkarımı) — Faz 54 bölmesi.

Sınıflandırma desenleri (mimari §5.3.1):

| Desen                                                        | Sınıf      |
|--------------------------------------------------------------|------------|
| `i < n`, `i < arr.Length`, `i < v.size()`, `foreach`, `n--`  | `LINEAR`   |
| `i *= 2`, `i /= 2`, `i >>= 1`, `lo <= hi` + `mid` yarılama    | `LOG`      |
| `i < 10` (sabit literal)                                     | `CONSTANT` |
| diğer (ör. `i * i <= n`, `node = node->next`, `while (true)`) | `UNKNOWN`  |

Yalnızca açık desenler sınıflandırılır; emin olunamayan her durum `UNKNOWN`'dır.
Tür sabitleri, ilkel düğüm yardımcıları ve güncelleme çözümlemesi `_loops.py`'dedir.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass, field

from tree_sitter import Node

from codementor.analysis._loops import (
    _BINARY,
    COMPREHENSION_TYPES,
    Update,
    _assignments,
    _body_nodes,
    _body_updates,
    _ident,
    _mentions,
    _operator,
    _sides,
    _unwrap,
    _updates,
    is_constant,
    is_python_for,
)
from codementor.analysis._symbols import text
from codementor.analysis.parsers import iter_nodes
from codementor.models.enums import LoopBound

_COMPARISONS = frozenset({"<", "<=", ">", ">=", "!="})


@dataclass(frozen=True)
class LoopShape:
    """Sınıflandırma sonucu: sınır ve (varsa) sayaç değişkeni."""

    bound: LoopBound
    counter: str | None = None


def _comparisons(cond: Node | None) -> list[Node]:
    """`a < b && c != d` → karşılaştırmalar (yalnızca `&&` zinciri açılır; yinelemeli)."""
    found: list[Node] = []
    stack = [cond]
    while stack:
        current = _unwrap(stack.pop())
        if current is None:
            continue
        op = _operator(current)
        if current.type in ("binary_expression", "boolean_operator") and op in ("&&", "and"):
            stack += [current.child_by_field_name("right"), current.child_by_field_name("left")]
        elif (
            current.type in ("binary_expression", "comparison_operator")
            and op in _COMPARISONS
            # Python zincirli karşılaştırma (`a < b < c`) sınıflandırılmaz
            and (current.type == "binary_expression" or current.named_child_count == 2)
        ):
            found.append(current)
    return found


@dataclass
class AssignmentIndex:
    """Kapsam başına bir kez kurulan dizin: değişken → (bitiş baytı, değer) listesi.

    Sayaç başlangıcı her döngü için kapsamı yeniden taramadan bulunur (doğrusal toplam süre).
    """

    by_var: dict[str, tuple[list[int], list[Node]]] = field(default_factory=dict)

    @classmethod
    def build(cls, scope: Node) -> AssignmentIndex:
        index = cls()
        pairs: dict[str, list[tuple[int, Node]]] = {}
        for node in iter_nodes(scope):
            for var, value in _assignments(node):
                pairs.setdefault(var, []).append((node.end_byte, value))
        for var, items in pairs.items():
            items.sort(key=lambda item: item[0])
            index.by_var[var] = ([end for end, _ in items], [value for _, value in items])
        return index

    def last_before(self, var: str, offset: int) -> Node | None:
        """`offset`ten önce biten son bildirim/atama değeri."""
        ends, values = self.by_var.get(var, ([], []))
        position = bisect_right(ends, offset)
        return values[position - 1] if position else None


def _initial_value(var: str, loop: Node, index: AssignmentIndex) -> Node | None:
    """Sayacın başlangıç değeri: for başlığı, yoksa döngüden önceki son bildirim/atama."""
    if loop.type == "for_statement":
        header = [
            value
            for init in loop.children_by_field_name("initializer")
            for n in iter_nodes(init)
            for name, value in _assignments(n)
            if name == var
        ]
        if header:
            return header[-1]
    return index.last_before(var, loop.start_byte)


def _has_halving(node: Node | None) -> bool:
    """İfadede `x / 2`, `x >> 1` gibi sabitle bölme/kaydırma var mı."""
    return node is not None and any(
        n.type in _BINARY
        and _operator(n) in ("/", "//", ">>")
        and is_constant(n.child_by_field_name("right"))
        for n in iter_nodes(node)
    )


def _binary_search(loop: Node, comparisons: list[Node]) -> str | None:
    """`lo <= hi` + `mid = (lo + hi) / 2` + `lo = mid + 1` / `hi = mid` deseni.

    Gövdedeki herhangi bir `/ 2` yetmez: karşılaştırılan uçlardan biri, yarılanmış bir
    değerden (ya da doğrudan yarılamadan) türetilen bir atama almalıdır.
    """
    assignments = [pair for n in _body_nodes(loop) for pair in _assignments(n)]
    halved = {var for var, value in assignments if _has_halving(value)}
    for cmp in comparisons:
        left, right = _sides(cmp)
        lo, hi = _ident(left), _ident(right)
        if not (lo and hi and lo != hi):
            continue
        for var, value in assignments:
            derived = _has_halving(value) or any(_mentions(value, h) for h in halved)
            if var in (lo, hi) and derived:
                return lo
    return None


def _from_counter(
    loop: Node, comparisons: list[Node], updates: list[Update], index: AssignmentIndex
) -> LoopShape:
    """Sayaç deseni: yön güncellemenin işaretinden gelir; CONSTANT için iki uç da sabit olmalı."""
    updated = {var for var, _, _ in updates}
    for cmp in comparisons:
        sides = _sides(cmp)
        for counter_side, other in (sides, sides[::-1]):
            var = _ident(counter_side)
            if var is None or var not in updated or _mentions(other, var):
                continue
            kinds = {kind for v, kind, _ in updates if v == var}
            signs = {sign for v, _, sign in updates if v == var}
            if "other" in kinds or {"mul", "add"} <= kinds or {1, -1} <= signs:
                return LoopShape(LoopBound.UNKNOWN, var)  # sayaç tutarsız değişiyor
            if is_constant(other) and is_constant(_initial_value(var, loop, index)):
                return LoopShape(LoopBound.CONSTANT, var)
            return LoopShape(LoopBound.LOG if "mul" in kinds else LoopBound.LINEAR, var)
    return LoopShape(LoopBound.UNKNOWN)


def classify(loop: Node, index: AssignmentIndex) -> LoopShape:
    """Döngünün sınır sınıfı; `index` kapsayan fonksiyonun atama dizini.

    Aşırı derin ifadelerde sınıflandırma yapılamazsa `UNKNOWN` (olgular kaybolmaz).
    """
    try:
        return _classify(loop, index)
    except RecursionError:
        return LoopShape(LoopBound.UNKNOWN)


def _python_iteration(loop: Node) -> LoopShape:
    """`for i in range(10)` → CONSTANT; diğer `range(...)` ve koleksiyon gezintisi → LINEAR."""
    iterable = _unwrap(loop.child_by_field_name("right"))
    if (
        iterable is not None
        and iterable.type == "call"
        and text(iterable.child_by_field_name("function")) == "range"
    ):
        args = iterable.child_by_field_name("arguments")
        values = list(args.named_children) if args is not None else []
        counter = _ident(loop.child_by_field_name("left"))
        if values and all(is_constant(v) for v in values[:2]):
            return LoopShape(LoopBound.CONSTANT, counter)
        return LoopShape(LoopBound.LINEAR, counter)
    return LoopShape(LoopBound.LINEAR)


def _classify(loop: Node, index: AssignmentIndex) -> LoopShape:
    if loop.type in ("for_range_loop", "foreach_statement") or loop.type in COMPREHENSION_TYPES:
        return LoopShape(LoopBound.LINEAR)
    if is_python_for(loop):
        return _python_iteration(loop)
    condition = _unwrap(loop.child_by_field_name("condition"))
    if condition is None or is_constant(condition):
        return LoopShape(LoopBound.UNKNOWN)
    comparisons = _comparisons(condition)
    if not comparisons:
        return LoopShape(LoopBound.UNKNOWN)
    header = [u for n in loop.children_by_field_name("update") for u in _updates(n)]
    if loop.type != "for_statement" or not header:
        counter = _binary_search(loop, comparisons)
        if counter is not None:
            return LoopShape(LoopBound.LOG, counter)
    # başlıkta güncelleme olsa da gövdedeki sayaç değişikliği hesaba katılır
    return _from_counter(loop, comparisons, header + _body_updates(loop), index)
