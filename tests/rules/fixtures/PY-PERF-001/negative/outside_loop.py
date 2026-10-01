def first(items):
    head = items.pop(0)
    items.insert(0, head)
    return head in items
