from collections import deque


def drain(items):
    queue = deque(items)
    seen = set()
    while queue:
        x = queue.popleft()
        if x in seen:
            continue
        seen.add(x)
