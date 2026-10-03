"""Bir bölümü dengeli parçalara bölme (`eval run --part k/n`).

Canlı koşu örnek başına token harcar; dev bölümü parça parça koşulabilsin diye örnekler `n`
parçaya ayrılır. Bölme belirleyicidir (yalnız kimliklere ve etiketlere bağlı) ve her parçada dil/
motor grubu ile örnek türü (sözdizimi hatalı, injection, temiz, hatalı) orantılı kalır; böylece
her parça tüm bölümün küçük bir kopyası gibi davranır ve parçaların sonuçları birleştirilebilir.
"""

from __future__ import annotations

import re
from collections import Counter

from codementor.eval.breakdown import group_of
from codementor.models.eval import Label, Sample

_PART = re.compile(r"^(\d+)/(\d+)$")


def parse_part(spec: str) -> tuple[int, int]:
    """`"2/4"` → `(2, 4)`; parça numarası 1..n."""
    match = _PART.match(spec.strip())
    if match is None:
        raise ValueError(f"Geçersiz parça: {spec!r} (ör. 1/4)")
    index, parts = int(match[1]), int(match[2])
    if parts < 1 or not 1 <= index <= parts:
        raise ValueError(f"Geçersiz parça: {spec!r} (parça numarası 1 ile {parts} arasında)")
    return index, parts


def sample_kind(label: Label) -> str:
    """Örnek türü: dengelemede grup ile birlikte kullanılır."""
    if not label.syntax_valid:
        return "syntax"
    if label.injection:
        return "injection"
    return "clean" if not label.expected.findings else "flawed"


def select_part(samples: list[Sample], index: int, parts: int) -> list[Sample]:
    """`index`. parçanın örnekleri (kimlik sırasıyla).

    Açgözlü atama: her örnek, kendi grubundan ve türünden en az örneği olan, eşitlikte en küçük
    parçaya gider. Girdi sırası sonucu etkilemez.
    """
    ordered = sorted(samples, key=lambda s: (group_of(s.label), sample_kind(s.label), s.label.id))
    groups: list[Counter[str]] = [Counter() for _ in range(parts)]
    kinds: list[Counter[str]] = [Counter() for _ in range(parts)]
    sizes = [0] * parts
    chosen: list[Sample] = []
    for sample in ordered:
        group, kind = group_of(sample.label), sample_kind(sample.label)
        target = min(range(parts), key=lambda p: (groups[p][group], kinds[p][kind], sizes[p], p))
        groups[target][group] += 1
        kinds[target][kind] += 1
        sizes[target] += 1
        if target == index - 1:
            chosen.append(sample)
    return sorted(chosen, key=lambda s: s.label.id)
