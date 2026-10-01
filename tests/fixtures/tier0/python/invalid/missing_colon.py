def average(values):
    total = 0
    for v in values  # expect-error
        total += v
    return total / len(values)
