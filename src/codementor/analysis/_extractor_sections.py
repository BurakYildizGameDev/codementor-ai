"""Extractör sabitleri ve modül düzeyi yardımcıları — Faz 54 bölmesi.

`extractor.py`'nin `_Extractor` sınıfının kullandığı desen tabloları, tip kısayolları
ve düğüm yardımcıları buradadır; bölüm kurucular sınıf gövdesinde kalır (durum paylaşımı).
"""

from __future__ import annotations

import re
from typing import TypeVar

from tree_sitter import Node

from codementor.analysis._symbols import CallName, operator_of, text
from codementor.models.facts import FunctionFact

T = TypeVar("T")
_Call = tuple[Node, CallName, tuple[str, str] | None]

_USING_STD = re.compile(r"\busing\s+namespace\s+std\s*;")
_USING_LINQ = re.compile(r"\busing\s+System\.Linq\s*;")
_STRING_TYPES = frozenset({"string", "String", "std::string", "FString"})
_TYPE_DECLARATIONS = frozenset(
    {
        "class_specifier",
        "struct_specifier",
        "union_specifier",
        "enum_specifier",
        "class_declaration",
        "struct_declaration",
        "interface_declaration",
        "enum_declaration",
        "record_declaration",
        "class_definition",  # Python
    }
)


def _name(fn: FunctionFact | None) -> str | None:
    return fn.name if fn is not None else None


def _start(fn: FunctionFact | None) -> int | None:
    return fn.line_start if fn is not None else None


_MAX_CHAIN = 64  # `a + b + ... ` zincirinde en soldaki işlenene kadar en fazla bu kadar adım


def _leftmost_operand(node: Node | None) -> str | None:
    """`s + a + b` → `s` (yalnız `+` zinciri); başka ifadede None."""
    for _ in range(_MAX_CHAIN):
        if node is None or node.type != "binary_expression" or operator_of(node) != "+":
            break
        node = node.child_by_field_name("left")
    else:
        return None
    if node is None or node.type not in (
        "identifier",
        "member_access_expression",
        "field_expression",
    ):
        return None
    return text(node).removeprefix("this.")


SYNTAX_WARNING = "Kodda sözdizimi hatası var; statik olgular eksik olabilir."
NO_FUNCTION_WARNING = "Fonksiyon bulunamadı; olgular dosya düzeyinde toplandı."
FAILURE_WARNING = "Statik olgular çıkarılamadı ({}); analiz olgusuz devam ediyor."
SECTION_WARNING = "{} olguları çıkarılamadı ({}); bu bölüm boş."
COSTS_WARNING = "Çağrı maliyeti tablosu okunamadı; çağrı maliyetleri bilinmiyor."
