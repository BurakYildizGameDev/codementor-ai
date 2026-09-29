"""Düğüm bağlamı: kapsayan fonksiyon, döngü derinliği, en içteki döngü.

Tek bir `TreeCursor` geçişiyle hesaplanır (Faz 3 kuralı: büyük/hatalı ağaçlarda
`Node.children` yerine cursor). Özyineleme yoktur; süre düğüm sayısıyla doğrusaldır.
"""

from __future__ import annotations

from dataclasses import dataclass

from tree_sitter import Node

from codementor.analysis._loops import LOOP_TYPES
from codementor.analysis._symbols import NodeKey, key


@dataclass(frozen=True)
class Ctx:
    """Bir düğümün bağlamı."""

    function: NodeKey | None = None
    depth: int = 0
    loop: Node | None = None


def contexts(root: Node, wanted: set[NodeKey], functions: set[NodeKey]) -> dict[NodeKey, Ctx]:
    """İstenen düğümlerin bağlamı. `functions` sınır sayılan fonksiyon düğümleri."""
    found: dict[NodeKey, Ctx] = {}
    cursor = root.walk()
    stack = [Ctx()]  # stack[-1]: imleçteki düğümün bağlamı
    while True:
        node = cursor.node
        assert node is not None
        here = stack[-1]
        node_key = key(node)
        if node_key in wanted:
            found[node_key] = here
        if node_key in functions:
            inner = Ctx(function=node_key)
        elif node.type in LOOP_TYPES:
            inner = Ctx(function=here.function, depth=here.depth + 1, loop=node)
        else:
            inner = here
        if cursor.goto_first_child():
            stack.append(inner)
            continue
        while not cursor.goto_next_sibling():
            if not cursor.goto_parent():
                return found
            stack.pop()
