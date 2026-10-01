def two_sum(numbers: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for index, value in enumerate(numbers):
        need = target - value
        if need in seen:
            return seen[need], index
        seen[value] = index
    return None
