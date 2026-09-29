"""Çağrı grafiği yardımcıları (karmaşıklık ipucu için).

Güçlü bağlı bileşenler karşılıklı özyinelemeyi (a → b → a) bulur ve ipuçlarının
çağrılanlardan çağıranlara doğru, özyinelemesiz hesaplanmasını sağlar.
"""

from __future__ import annotations


def strongly_connected(nodes: list[str], edges: dict[str, list[str]]) -> list[list[str]]:
    """Güçlü bağlı bileşenler (Tarjan, yinelemeli); çağrılanlar çağıranlardan önce gelir."""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    result: list[list[str]] = []
    for root in nodes:
        if root in index:
            continue
        work = [(root, 0)]
        while work:
            node, position = work[-1]
            if position == 0 and node not in index:
                index[node] = low[node] = len(index)
                stack.append(node)
                on_stack.add(node)
            successors = edges.get(node, [])
            if position < len(successors):
                work[-1] = (node, position + 1)
                nxt = successors[position]
                if nxt not in index:
                    work.append((nxt, 0))
                elif nxt in on_stack:
                    low[node] = min(low[node], index[nxt])
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
            if low[node] == index[node]:
                component: list[str] = []
                while True:
                    member = stack.pop()
                    on_stack.discard(member)
                    component.append(member)
                    if member == node:
                        break
                result.append(component)
    return result
