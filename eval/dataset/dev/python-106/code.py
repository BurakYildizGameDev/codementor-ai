def prepend_all(numbers: list[int]) -> list[int]:
    result: list[int] = []
    for num in numbers:
        result.insert(0, num)
    return result
