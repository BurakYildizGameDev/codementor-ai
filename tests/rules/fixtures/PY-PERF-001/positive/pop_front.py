# EXPECT: 5
def drain(items):
    total = 0
    while items:
        total += items.pop(0)
    return total
