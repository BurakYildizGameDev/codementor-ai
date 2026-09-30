"""Düğüm bağlamı: kapsayan fonksiyon, döngü derinliği, en içteki döngü.

Tek bir `TreeCursor` geçişiyle hesaplanır (Faz 3 kuralı: büyük/hatalı ağaçlarda
`Node.children` yerine cursor). Özyineleme yoktur; süre düğüm sayısıyla doğrusaldır.

Döngü başlığında yalnızca bir kez değerlendirilen kısımlar (`for` başlatıcısı,
`foreach`/range-for koleksiyon ifadesi) döngünün içinde sayılmaz: dış bağlamı alır.
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


# Döngü başlığında bir kez değerlendirilen alanlar (C/C++/C# gramerlerinde aynı ad)
_ONCE_FIELDS = frozenset({"initializer", "right"})


@dataclass(frozen=True)
class _Frame:
    """Bir düğümün çocuklarının bağlamı; döngüdeyse bir kez çalışan alanlar için dış bağlam."""

    inner: Ctx
    outer: Ctx | None = None


def contexts(root: Node, wanted: set[NodeKey], functions: set[NodeKey]) -> dict[NodeKey, Ctx]:
    """İstenen düğümlerin bağlamı. `functions` sınır sayılan fonksiyon düğümleri."""
    found: dict[NodeKey, Ctx] = {}
    cursor = root.walk()
    stack = [_Frame(Ctx())]  # stack[-1]: imleçteki düğümün ebeveyninin çerçevesi
    here = Ctx()  # imleçteki düğümün bağlamı
    while True:
        node = cursor.node
        assert node is not None
        node_key = key(node)
        if node_key in wanted:
            found[node_key] = here
        if node_key in functions:
            frame = _Frame(Ctx(function=node_key))
        elif node.type in LOOP_TYPES:
            frame = _Frame(Ctx(function=here.function, depth=here.depth + 1, loop=node), here)
        else:
            frame = _Frame(here)
        if cursor.goto_first_child():
            stack.append(frame)
        else:
            while not cursor.goto_next_sibling():
                if not cursor.goto_parent():
                    return found
                stack.pop()
        top = stack[-1]
        once = cursor.field_name in _ONCE_FIELDS
        here = top.outer if top.outer is not None and once else top.inner
