"""Editör araması ve değiştirme (Ctrl+F / Ctrl+H, Faz 24 ve 33): Tk'den bağımsız mantık."""

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


def _word_char(char: str) -> bool:
    """Tanımlayıcı karakteri (Türkçe harfler dahil); tam sözcük sınırı bunun dışıdır."""
    return char.isalnum() or char == "_"


def _is_word(line: str, column: int, length: int) -> bool:
    before = line[column - 1] if column > 0 else ""
    after = line[column + length] if column + length < len(line) else ""
    return not (before and _word_char(before)) and not (after and _word_char(after))


def find_all(
    text: str, query: str, *, case_sensitive: bool = False, whole_word: bool = False
) -> list[Match]:
    """Satır içi, örtüşmeyen eşleşmeler (sorgu satır sonu içermez)."""
    if not query or "\n" in query:
        return []
    needle = query if case_sensitive else query.lower()
    matches: list[Match] = []
    for number, line in enumerate(text.split("\n"), start=1):
        haystack = line if case_sensitive else line.lower()
        column = haystack.find(needle)
        while column != -1:
            if not whole_word or _is_word(line, column, len(query)):
                matches.append(Match(number, column, len(query)))
                if len(matches) >= MAX_MATCHES:
                    return matches
                column = haystack.find(needle, column + len(needle))
            else:
                column = haystack.find(needle, column + 1)
    return matches


def replace_all(
    text: str,
    query: str,
    replacement: str,
    *,
    case_sensitive: bool = False,
    whole_word: bool = False,
) -> tuple[str, int]:
    """Tüm eşleşmeleri değiştirir; (yeni metin, değiştirme sayısı). Eşleşmeler özgün metinde
    bir kez bulunur, değiştirilen metin yeniden aranmaz (sorguyu içerse de çift değişmez)."""
    matches = find_all(text, query, case_sensitive=case_sensitive, whole_word=whole_word)
    if not matches:
        return text, 0
    lines = text.split("\n")
    by_line: dict[int, list[Match]] = {}
    for match in matches:
        by_line.setdefault(match.line, []).append(match)
    for number, found in by_line.items():
        line = lines[number - 1]
        for match in reversed(found):  # sondan başa: önceki sütunlar kaymaz
            line = line[: match.column] + replacement + line[match.column + match.length :]
        lines[number - 1] = line
    return "\n".join(lines), len(matches)


def step(current: int | None, count: int, *, forward: bool) -> int | None:
    """Sonraki/önceki eşleşmenin sırası; uçlarda başa/sona sarar."""
    if count == 0:
        return None
    if current is None:
        return 0 if forward else count - 1
    return (current + (1 if forward else -1)) % count
