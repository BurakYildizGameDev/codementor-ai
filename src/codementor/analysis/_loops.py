"""Döngü sınır sınıfı sezgiseli (mimari §5.3.1).

| Desen                                                        | Sınıf      |
|--------------------------------------------------------------|------------|
| `i < n`, `i < arr.Length`, `i < v.size()`, `foreach`, `n--`  | `LINEAR`   |
| `i *= 2`, `i /= 2`, `i >>= 1`, `lo <= hi` + `mid` yarılama    | `LOG`      |
| `i < 10` (sabit literal)                                     | `CONSTANT` |
| diğer (ör. `i * i <= n`, `node = node->next`, `while (true)`) | `UNKNOWN`  |

Yalnızca açık desenler sınıflandırılır; emin olunamayan her durum `UNKNOWN`'dır.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass, field
from typing import Literal

from tree_sitter import Node

from codementor.analysis._symbols import text
from codementor.analysis.parsers import iter_nodes
from codementor.models.enums import LoopBound

LoopKind = Literal["for", "while", "do", "foreach"]

# Python kavramaları örtük döngüdür (ADR-0015)
COMPREHENSION_TYPES = frozenset(
    {"list_comprehension", "set_comprehension", "dictionary_comprehension", "generator_expression"}
)
LOOP_TYPES = (
    frozenset(
        {"for_statement", "for_range_loop", "foreach_statement", "while_statement", "do_statement"}
    )
    | COMPREHENSION_TYPES
)
FUNCTION_TYPES = frozenset(
    {
        "function_definition",
        "method_declaration",
        "constructor_declaration",
        "destructor_declaration",
        "local_function_statement",
        "operator_declaration",
        "lambda_expression",
        "anonymous_method_expression",
        "lambda",  # Python
    }
)
_LITERALS = frozenset(
    {
        "number_literal",
        "integer_literal",
        "real_literal",
        "char_literal",
        "character_literal",
        "true",
        "false",
        "boolean_literal",
        "integer",  # Python
        "float",
    }
)
_UNARY = frozenset({"unary_expression", "prefix_unary_expression", "unary_operator"})
_BINARY = frozenset({"binary_expression", "binary_operator"})  # C ailesi / Python
_ASSIGNMENTS = frozenset({"assignment_expression", "assignment", "augmented_assignment"})
_COMPARISONS = frozenset({"<", "<=", ">", ">=", "!="})
_ADD_OPS = frozenset({"+=", "-="})
_MUL_OPS = frozenset({"*=", "/=", "//=", "<<=", ">>="})
_ADD_BINARY = frozenset({"+", "-"})
_MUL_BINARY = frozenset({"*", "/", "//", "<<", ">>"})
_INC_DEC = frozenset({"++", "--"})
_UNARY_UPDATES = frozenset(
    {"update_expression", "postfix_unary_expression", "prefix_unary_expression"}
)


@dataclass(frozen=True)
class LoopShape:
    """Sınıflandırma sonucu: sınır ve (varsa) sayaç değişkeni."""

    bound: LoopBound
    counter: str | None = None


_KINDS: dict[str, LoopKind] = {
    "for_statement": "for",
    "while_statement": "while",
    "do_statement": "do",
    "for_range_loop": "foreach",
    "foreach_statement": "foreach",
}


def is_python_for(loop: Node) -> bool:
    """Python `for x in ...` (C `for_statement` ile aynı düğüm adı; `right` alanı ayırır)."""
    return loop.type == "for_statement" and loop.child_by_field_name("right") is not None


def kind_of(loop: Node) -> LoopKind:
    """Olgu türü: for / while / do / foreach (C++ range-for, Python for ve kavramalar dahil)."""
    if loop.type in COMPREHENSION_TYPES or is_python_for(loop):
        return "foreach"
    return _KINDS[loop.type]


def _sides(node: Node) -> tuple[Node | None, Node | None]:
    """İkili ifadenin iki yanı; Python `comparison_operator`'da alan adı yok."""
    left, right = node.child_by_field_name("left"), node.child_by_field_name("right")
    if left is None and right is None and node.named_child_count >= 2:
        return node.named_children[0], node.named_children[1]
    return left, right


def _unwrap(node: Node | None) -> Node | None:
    while node is not None:
        if node.type == "condition_clause":  # C++ `while (...)`
            node = node.child_by_field_name("value")
        elif node.type == "parenthesized_expression" and node.named_child_count:
            node = node.named_children[0]
        else:
            break
    return node


def _operator(node: Node) -> str:
    op = node.child_by_field_name("operator")
    if op is not None:
        return op.type
    return next((c.type for c in node.children if not c.is_named), "")


def is_constant(node: Node | None) -> bool:
    """Yalnızca literallerden oluşan ifade mi (`10`, `-1`, `2 * 8`). Yinelemeli."""
    stack = [node]
    while stack:
        current = _unwrap(stack.pop())
        if current is None:
            return False
        if current.type in _LITERALS:
            continue
        if current.type in _UNARY and current.named_child_count == 1:
            stack.append(current.named_children[0])
        elif current.type in _BINARY:
            stack += [current.child_by_field_name("left"), current.child_by_field_name("right")]
        else:
            return False
    return True


def _ident(node: Node | None) -> str | None:
    node = _unwrap(node)
    return text(node) if node is not None and node.type == "identifier" else None


def _mentions(node: Node | None, name: str) -> bool:
    return node is not None and any(
        n.type == "identifier" and text(n) == name for n in iter_nodes(node)
    )


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


# (değişken, add|mul|other, yön: +1 artan, -1 azalan, 0 bilinmiyor)
Update = tuple[str, str, int]
_SIGN = {"+=": 1, "-=": -1, "*=": 1, "<<=": 1, "/=": -1, "//=": -1, ">>=": -1}
_BINARY_SIGN = {"+": 1, "-": -1, "*": 1, "<<": 1, "/": -1, "//": -1, ">>": -1}


def _update(node: Node) -> Update | None:
    """Tek güncelleme ifadesi: `i++`, `i -= 2`, `i *= 2`, `i = i + 1`, `i = arr[i]` ..."""
    if node.type in _UNARY_UPDATES:
        tokens = {c.type for c in node.children if not c.is_named} & _INC_DEC
        operand = node.child_by_field_name("argument") or next(iter(node.named_children), None)
        var = _ident(operand)
        if var is None or not tokens:
            return None
        return (var, "add", 1 if "++" in tokens else -1)
    if node.type not in _ASSIGNMENTS:
        return None
    var = _ident(node.child_by_field_name("left"))
    if var is None:
        return None
    op, right = _operator(node), _unwrap(node.child_by_field_name("right"))
    if op in _ADD_OPS:
        if _mentions(right, var):
            return (var, "other", 0)
        return (var, "add", _SIGN[op] if is_constant(right) else 0)
    if op in _MUL_OPS:
        return (var, "mul", _SIGN[op]) if is_constant(right) else (var, "other", 0)
    if node.type == "assignment":  # Python `x = ...` (operatör alanı yok)
        op = "="
    if op == "=" and right is not None and right.type in _BINARY:
        left_ident = _ident(right.child_by_field_name("left"))
        binary = _operator(right)
        if left_ident == var and is_constant(right.child_by_field_name("right")):
            if binary in _ADD_BINARY:
                return (var, "add", _BINARY_SIGN[binary])
            if binary in _MUL_BINARY:
                return (var, "mul", _BINARY_SIGN[binary])
    return (var, "other", 0)


def _updates(node: Node | None) -> list[Update]:
    """Güncelleme ifadelerinden (virgülle ayrılmış olanlar dahil) güncellemeler."""
    found: list[Update] = []
    stack = [node]
    while stack:
        current = _unwrap(stack.pop())
        if current is None:
            continue
        if current.type in ("comma_expression", "sequence_expression"):
            stack += reversed(current.named_children)
            continue
        update = _update(current)
        if update is not None:
            found.append(update)
    return found


def _body_nodes(loop: Node) -> list[Node]:
    """Gövde düğümleri; iç döngü ve fonksiyonların içine inilmez.

    Her düğüm yalnızca en içteki döngüsünce taranır: iç içe döngülerde toplam süre doğrusal.
    """
    body = loop.child_by_field_name("body")
    if body is None:
        return []
    return list(
        iter_nodes(
            body, descend=lambda n: n.type not in FUNCTION_TYPES and n.type not in LOOP_TYPES
        )
    )


def _body_updates(loop: Node) -> list[Update]:
    return [
        u
        for n in _body_nodes(loop)
        if n.type in _UNARY_UPDATES or n.type in _ASSIGNMENTS
        for u in _updates(n)
    ]


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


def _assignments(n: Node) -> list[tuple[str, Node]]:
    """Tek düğümdeki `int v = X`, `v = X`, C# `var v = X` çiftleri."""
    if n.type == "init_declarator":
        var, value = _ident(n.child_by_field_name("declarator")), n.child_by_field_name("value")
        return [(var, value)] if var and value is not None else []
    if n.type == "variable_declarator":
        name = n.child_by_field_name("name")
        rest = [c for c in n.named_children if c != name]
        return [(text(name), rest[-1])] if name is not None and rest else []
    if (n.type == "assignment_expression" and _operator(n) == "=") or n.type == "assignment":
        var, value = _ident(n.child_by_field_name("left")), n.child_by_field_name("right")
        return [(var, value)] if var and value is not None else []
    return []


def _assigned_values(node: Node, var: str, *, shallow: bool = False) -> list[Node]:
    """`node` (veya alt ağacı) içinde `var`'a verilen değerler."""
    nodes = [node] if shallow else list(iter_nodes(node))
    return [value for n in nodes for name, value in _assignments(n) if name == var]


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


def resets_in_body(loop: Node) -> set[str]:
    """Döngü gövdesinde (iç döngüler hariç) değer atanan değişkenler; ebeveyn başına bir kez."""
    return {var for n in _body_nodes(loop) for var, _ in _assignments(n)}


def counter_outer(loop: Node, counter: str | None, parent_resets: set[str]) -> bool:
    """İç döngü sayacı ne kendi başlığında ne dış döngü gövdesinde sıfırlanıyor mu.

    Örn. `int j = 0; for (i ...) { while (j < n && ...) j++; }`: iç döngü toplamda n kez
    döner (two-pointer / sliding window); iç içe çarpım ipucu burada yanılır.
    `parent_resets` dış döngü için `resets_in_body` sonucudur (tekrar taranmaz).
    """
    if counter is None:
        return False
    if (
        loop.type == "for_statement"
        and not is_python_for(loop)
        and any(
            _assigned_values(init, counter) for init in loop.children_by_field_name("initializer")
        )
    ):
        return False
    return counter not in parent_resets
