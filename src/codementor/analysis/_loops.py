"""Döngü türleri ve ilkel düğüm yardımcıları; sınır sınıflandırması `_loop_bounds.py`'de."""

from __future__ import annotations

from typing import Literal

from tree_sitter import Node

from codementor.analysis._symbols import text
from codementor.analysis.parsers import iter_nodes

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
_ADD_OPS = frozenset({"+=", "-="})
_MUL_OPS = frozenset({"*=", "/=", "//=", "<<=", ">>="})
_ADD_BINARY = frozenset({"+", "-"})
_MUL_BINARY = frozenset({"*", "/", "//", "<<", ">>"})
_INC_DEC = frozenset({"++", "--"})
_UNARY_UPDATES = frozenset(
    {"update_expression", "postfix_unary_expression", "prefix_unary_expression"}
)


# LoopShape `_loop_bounds.py`'de (Faz 54)


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


# AssignmentIndex/_initial_value `_loop_bounds.py`'de (Faz 54)


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


# _has_halving/_binary_search/_from_counter `_loop_bounds.py`'de (Faz 54)


# classify/_python_iteration/_classify `_loop_bounds.py`'de (Faz 54)


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
