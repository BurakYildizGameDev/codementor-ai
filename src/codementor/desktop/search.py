"""Editör araması (Ctrl+F, Faz 24): Tk'den bağımsız eşleşme mantığı."""

from __future__ import annotations

from dataclasses import dataclass

MAX_MATCHES = 2000  # boyama maliyetini sınırlar (600 satırlık girdide pratikte erişilmez)


@dataclass(frozen=True)
class Match:
    """Bir eşleşme: Tk satırı (1'den), sütun (0'dan) ve uzunluk."""

    line: int
    column: int
    length: int

    @property
    def start(self) -> str:
        return f"{self.line}.{self.column}"

    @property
    def end(self) -> str:
        return f"{self.line}.{self.column + self.length}"


def find_all(text: str, query: str, *, case_sensitive: bool = False) -> list[Match]:
    """Satır içi, örtüşmeyen eşleşmeler (sorgu satır sonu içermez)."""
    if not query or "\n" in query:
        return []
    needle = query if case_sensitive else query.lower()
    matches: list[Match] = []
    for number, line in enumerate(text.split("\n"), start=1):
        haystack = line if case_sensitive else line.lower()
        column = haystack.find(needle)
        while column != -1:
            matches.append(Match(number, column, len(query)))
            if len(matches) >= MAX_MATCHES:
                return matches
            column = haystack.find(needle, column + len(needle))
    return matches


def step(current: int | None, count: int, *, forward: bool) -> int | None:
    """Sonraki/önceki eşleşmenin sırası; uçlarda başa/sona sarar."""
    if count == 0:
        return None
    if current is None:
        return 0 if forward else count - 1
    return (current + (1 if forward else -1)) % count
