"""Satır aralığı ve kanıt eşleşmesi (mimari §5.6, 2.-3. satırlar).

Kanıt, `line_start..line_end ± pencere` içinde boşluk-duyarsız alt dizi olarak aranır;
bulunursa satır düzeltilir, bulunamazsa bulgu atılır.
"""

from __future__ import annotations

import re

from codementor.models.verification import EvidenceMatch

MIN_EVIDENCE_CHARS = 2  # boşluksuz; ";" gibi her yerde geçen kanıt doğrulama sayılmaz
MAX_SPAN_LINES = 30  # modelin uydurduğu dev line_end tüm dosyayı pencereye katmasın
MAX_OCCURRENCES = 64
_WHITESPACE = re.compile(r"\s+")
_ELLIPSIS = re.compile(r"\.\.\.|…")
# "Line 18: ...", "satır 18 -", numaralı görünümden kopyalanmış "18 | ..."
_LINE_PREFIX = re.compile(
    r"^\s*(?:(?:line|satır|satir)\s*\d+\s*[:.)\-|]\s*|\d+\s*\|\s?)", re.IGNORECASE
)
_QUOTES = "`'\""


def check_line_range(line_start: int, line_end: int | None, line_count: int) -> bool:
    """`1 ≤ line_start ≤ line_end ≤ satır sayısı`."""
    end = line_start if line_end is None else line_end
    return 1 <= line_start <= end <= line_count


def _unwrap(evidence: str) -> str:
    text = evidence.replace("&lt;", "<").replace("&gt;", ">").strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in _QUOTES:
        text = text[1:-1]
    return text


def normalize_evidence(evidence: str) -> str:
    """Modelin eklediği süsleri atar: satır önekleri, çevreleyen tırnak, Faz 8 `&lt;` kaçışı."""
    lines = _unwrap(evidence).split("\n")
    return "\n".join(_LINE_PREFIX.sub("", line, count=1) for line in lines)


def _squash(text: str) -> str:
    return _WHITESPACE.sub("", text)


def _parts(text: str) -> list[str]:
    parts = [_squash(p) for p in _ELLIPSIS.split(text)]
    parts = [p for p in parts if p]
    if parts:
        parts[-1] = parts[-1].rstrip(";")  # satırda `;` olmayabilir (C# `x=new List<int>()`)
    return [p for p in parts if p]


def _variants(evidence: str) -> list[list[str]]:
    """Önce önekleri atılmış hal; bulunamazsa olduğu gibi (`0 | FLAG` gerçek kod olabilir)."""
    variants: list[list[str]] = []
    for text in (normalize_evidence(evidence), _unwrap(evidence)):
        parts = _parts(text)
        if parts and sum(map(len, parts)) >= MIN_EVIDENCE_CHARS and parts not in variants:
            variants.append(parts)
    return variants


def _find_in_order(haystack: str, parts: list[str], start: int) -> tuple[int, int] | None:
    """`parts` sırayla geçiyorsa (ilk başlangıç, son bitiş)."""
    first = haystack.find(parts[0], start)
    if first == -1:
        return None
    position = first + len(parts[0])
    for part in parts[1:]:
        found = haystack.find(part, position)
        if found == -1:
            return None
        position = found + len(part)
    return first, position


def _closest(
    haystack: str, owners: list[int], parts: list[str], line_start: int
) -> tuple[int, int] | None:
    """Bildirilen satıra en yakın eşleşmenin (ilk, son) satırları."""
    best: tuple[int, int] | None = None
    search_from = 0
    for _ in range(MAX_OCCURRENCES):  # tek satırlık 40 KB kodda karesel aramayı önler (§12)
        span = _find_in_order(haystack, parts, search_from)
        if span is None:
            break
        a, b = owners[span[0]], owners[span[1] - 1]
        if best is None or abs(a - line_start) < abs(best[0] - line_start):
            best = (a, b)
        if a >= line_start:  # sonraki eşleşmeler daha uzakta
            break
        search_from = span[0] + 1
    return best


def match_evidence(
    evidence: str,
    line_start: int,
    line_end: int | None,
    lines: list[str],
    window: int = 2,
) -> EvidenceMatch:
    """Kanıtı pencerede arar; birden çok eşleşmede bildirilen satıra en yakını seçilir."""
    variants = _variants(evidence)
    if not variants or not lines:
        return EvidenceMatch(found=False)
    end = line_start if line_end is None or line_end < line_start else line_end
    end = min(end, line_start + MAX_SPAN_LINES)
    first_line = max(1, line_start - window)
    last_line = min(len(lines), end + window)
    if first_line > last_line:
        return EvidenceMatch(found=False)

    # Pencerenin sıkıştırılmış metni ve her karakterin satırı
    squashed: list[str] = []
    owners: list[int] = []
    for number in range(first_line, last_line + 1):
        piece = _squash(lines[number - 1])
        squashed.append(piece)
        owners.extend([number] * len(piece))
    haystack = "".join(squashed)

    best: tuple[int, int] | None = None
    for parts in variants:
        best = _closest(haystack, owners, parts, line_start)
        if best is not None:
            break
    if best is None:
        return EvidenceMatch(found=False)
    a, b = best
    return EvidenceMatch(
        found=True,
        line_start=a,
        line_end=b if b > a else None,
        shifted=a != line_start,
    )
