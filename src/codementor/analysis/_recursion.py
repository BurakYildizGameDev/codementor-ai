"""Özyineleme olguları için yardımcılar (mimari §5.3.1 `recursion`).

- Öz-çağrı tespiti: `f()`, `this->f()`, aynı sınıfla nitelikli `Sinif::f()`. `Super::f()`,
  `Base::f()`, `base.f()` ve başka nesnenin `x.f()` çağrısı sayılmaz (çok biçimlilikten
  ayırt edilemez). Gövdede `using std::swap;` gibi aynı adı içe alan bildirim varsa (ADL
  deyimi) çağrı özyineleme sayılmaz.
- Dallanma faktörü: tek yürütme yolundaki en çok öz-çağrı; `if/else`, `?:` ve `switch`
  dallarında toplam değil en büyük alınır (özyinelemeli ikili arama üstel görünmez).
"""

from __future__ import annotations

import re

from tree_sitter import Node

from codementor.analysis._symbols import CallName, NodeKey, key, simple_name, text

HALVING = re.compile(r"/\s*2\b|>>\s*1\b|\bmid\b|\bhalf\b", re.IGNORECASE)
# `n - 1` gibi azaltma (yarılama değişkeni `mid - 1` hariç): varsa çağrı yarılamıyor demektir
_DECREMENT = re.compile(r"^\s*(?!mid\b|half\b)[A-Za-z_]\w*\s*-\s*\d+\s*$", re.IGNORECASE)
_LOOP_DEPTH_BRANCHING = 2
_SELF_RECEIVERS = frozenset({"this"})  # `base.X()` üst sınıfın metodudur
_BRANCHES = {
    "if_statement": ("consequence", "alternative"),
    "conditional_expression": ("consequence", "alternative"),
}
_CASES = frozenset({"case_statement", "switch_section", "switch_expression_arm"})


def max_path_self_calls(node: Node, is_self: set[NodeKey]) -> int:
    """Tek yürütme yolundaki en çok öz-çağrı: `if/else`, `?:`, `switch` dalları max alınır."""
    branches = _BRANCHES.get(node.type)
    if branches is not None:
        condition = node.child_by_field_name("condition")
        head = max_path_self_calls(condition, is_self) if condition is not None else 0
        arms = [node.child_by_field_name(field) for field in branches]
        return head + max(
            (max_path_self_calls(a, is_self) for a in arms if a is not None), default=0
        )
    cases = [c for c in node.named_children if c.type in _CASES]
    if cases:
        rest = [c for c in node.named_children if c.type not in _CASES]
        return sum(max_path_self_calls(c, is_self) for c in rest) + max(
            max_path_self_calls(c, is_self) for c in cases
        )
    own = 1 if key(node) in is_self else 0
    return own + sum(max_path_self_calls(c, is_self) for c in node.named_children)


def is_self_call(call: CallName, function: str) -> bool:
    """Çağrı fonksiyonun kendisine mi: `f()`, `this->f()`, `Sinif::f()` (aynı sınıf).

    `Super::f()`, `Base::f()`, `base.f()` ve başka nesnenin `x.f()` çağrısı öz-çağrı değildir.
    """
    if call.method != simple_name(function):
        return False
    if call.qualified is not None:
        return call.qualified == function
    return call.receiver is None or call.receiver in _SELF_RECEIVERS


def halves(calls: list[Node]) -> bool:
    """Tüm öz-çağrılar yarılıyor mu: her birinde yarılama argümanı var, hiçbirinde `n - 1` yok.

    `f(n - 1, mid) + f(n - 2, mid)` yarılama değildir (üstel şüphe kapanmamalı).
    """
    for call in calls:
        args = call.child_by_field_name("arguments")
        if args is None:
            return False
        items = [text(a) for a in args.named_children]
        if not any(HALVING.search(item) for item in items):
            return False
        if any(_DECREMENT.match(item) for item in items):
            return False
    return bool(calls)


def branching_factor(node: Node, self_calls: list[Node], in_loop: bool) -> int:
    """Dallanma faktörü; döngü içindeki öz-çağrı en az 2 sayılır (permütasyon, backtracking).

    Aşırı derin ağaçta özyineleme sınırına takılırsa öz-çağrı sayısına düşer.
    """
    try:
        branching = max_path_self_calls(node, {key(call) for call in self_calls})
    except RecursionError:
        branching = len(self_calls)
    if in_loop:
        branching = max(branching, _LOOP_DEPTH_BRANCHING)
    return max(1, branching)


def imports_same_name(node: Node, function: str) -> bool:
    """Gövdede `using std::swap;` gibi aynı adı içe alan bildirim var mı (ADL deyimi)."""
    body = node.child_by_field_name("body")
    pattern = re.compile(rf"\busing\s+[\w:]+::{re.escape(simple_name(function))}\s*;")
    return body is not None and pattern.search(text(body)) is not None
