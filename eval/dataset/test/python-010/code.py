def bfs_order(graph, start):
    queue = [start]
    seen = {start}
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return order
