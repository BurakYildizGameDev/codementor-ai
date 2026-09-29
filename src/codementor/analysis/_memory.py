"""Tahsis ve serbest bırakma sınıflandırması (mimari §5.3.1 `allocations`, `deallocations`).

Düğümler `queries/{dil}/memory.scm` ile bulunur; burada türe çevrilir. C#'ta `new` yalnızca
referans tipleri için sayılır: tip bilgisi olmadığından bilinen değer tipleri
(`Vector3`, `Quaternion`, ilkel tipler ...) hariç tutulur.
"""

from __future__ import annotations

from collections.abc import Iterator

from tree_sitter import Node

from codementor.analysis._symbols import NodeKey, key, operator_of, strip_templates, text
from codementor.models.enums import AllocationKind, DeallocationKind, Language

CSHARP_VALUE_TYPES = frozenset(
    {
        "Vector2",
        "Vector3",
        "Vector4",
        "Vector2Int",
        "Vector3Int",
        "Quaternion",
        "Color",
        "Color32",
        "Rect",
        "Bounds",
        "Ray",
        "RaycastHit",
        "Matrix4x4",
        "LayerMask",
        "int",
        "uint",
        "long",
        "ulong",
        "short",
        "ushort",
        "byte",
        "sbyte",
        "float",
        "double",
        "decimal",
        "bool",
        "char",
        "DateTime",
        "TimeSpan",
        "Guid",
        "KeyValuePair",
        "ValueTuple",
        "Span",
        "ReadOnlySpan",
    }
)
_STRINGS = frozenset(
    {
        "string_literal",
        "raw_string_literal",
        "concatenated_string",
        "verbatim_string_literal",
        "interpolated_string_expression",
    }
)
_C_ALLOC = {
    "malloc": AllocationKind.MALLOC,
    "calloc": AllocationKind.CALLOC,
    "realloc": AllocationKind.REALLOC,
    "make_unique": AllocationKind.MAKE_UNIQUE,
    "make_shared": AllocationKind.MAKE_SHARED,
}


def _is_string_concat(node: Node) -> bool:
    """`+` zincirinde bir metin sabiti var mı (yinelemeli; derin zincirde de güvenli)."""
    stack = [node]
    while stack:
        current = stack.pop()
        if current.type != "binary_expression" or operator_of(current) != "+":
            continue  # yalnızca `+` zinciri: `a + (b == "x")` metin birleştirme değil
        for side in ("left", "right"):
            operand = current.child_by_field_name(side)
            if operand is None:
                continue
            if operand.type in _STRINGS:
                return True
            stack.append(operand)
    return False


def _csharp_new(node: Node) -> bool:
    if node.type != "object_creation_expression":
        return True  # new(), diziler
    return strip_templates(text(node.child_by_field_name("type"))) not in CSHARP_VALUE_TYPES


def allocations(
    language: Language, found: dict[str, list[Node]], string_vars: set[str]
) -> Iterator[tuple[AllocationKind, Node]]:
    """`memory.scm` yakalamalarından (tür, düğüm) çiftleri; kaynak sırasıyla değil tür sırasıyla."""
    for node in found.get("alloc", []):
        fn = node.child_by_field_name("function")
        name = text(fn)
        for alloc_name, kind in _C_ALLOC.items():
            if name.split("<")[0].split("::")[-1] == alloc_name:
                yield kind, node
                break
    for node in found.get("new", []):
        if language is Language.CSHARP:
            if _csharp_new(node):
                yield AllocationKind.CSHARP_NEW, node
        else:
            array = node.child_by_field_name("declarator") is not None
            yield (AllocationKind.NEW_ARRAY if array else AllocationKind.NEW), node
    for node in found.get("closure", []):
        yield AllocationKind.CLOSURE, node
    # `+` zincirinin yalnızca en dış düğümü sayılır. `node.parent` tree-sitter'da O(derinlik)
    # olduğundan kullanılmaz; işlenen düğümler kümesi tek geçişte kurulur (doğrusal süre).
    concats = [n for n in found.get("concat", []) if operator_of(n) == "+"]
    operands = {
        key(child)
        for node in concats
        for child in (node.child_by_field_name("left"), node.child_by_field_name("right"))
        if child is not None
    }
    for node in concats:
        if key(node) not in operands and _is_string_concat(node):
            yield AllocationKind.STRING_CONCAT, node
    assigned: set[NodeKey] = set()
    for node in found.get("concat_assign", []):
        if operator_of(node) != "+=":
            continue
        right = node.child_by_field_name("right")
        target = text(node.child_by_field_name("left")).removeprefix("this.")
        if right is not None:
            assigned.add(key(right))
        if (right is not None and right.type in _STRINGS) or target in string_vars:
            yield AllocationKind.STRING_CONCAT, node
    for node in found.get("interpolation", []):
        if key(node) not in operands and key(node) not in assigned:
            yield AllocationKind.STRING_CONCAT, node


def deallocations(found: dict[str, list[Node]]) -> Iterator[tuple[DeallocationKind, Node]]:
    """`free`, `delete`, `delete[]`."""
    for node in found.get("free", []):
        yield DeallocationKind.FREE, node
    for node in found.get("delete", []):
        array = any(c.type == "[" for c in node.children)
        yield (DeallocationKind.DELETE_ARRAY if array else DeallocationKind.DELETE), node
