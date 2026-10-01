class Stack:
    def __init__(self) -> None:
        self._items: list[int] = []

    def push(self, value: int) -> None:
        self._items.append(value)

    def pop(self) -> int:
        if not self._items:
            raise IndexError("yığın boş")
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)
