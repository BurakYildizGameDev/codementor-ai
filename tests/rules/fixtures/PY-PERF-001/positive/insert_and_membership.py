# EXPECT: 6, 7
def unique_reversed(values):
    seen: list[int] = []
    out = []
    for v in values:
        if v not in seen:
            out.insert(0, v)
            seen.append(v)
    return out
