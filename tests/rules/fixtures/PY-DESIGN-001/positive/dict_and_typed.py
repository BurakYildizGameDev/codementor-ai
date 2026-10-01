# EXPECT: 2, 7
def remember(key, value, cache={}):
    cache[key] = value
    return cache


def collect(x: int, seen: set[int] = set()) -> set[int]:
    seen.add(x)
    return seen
