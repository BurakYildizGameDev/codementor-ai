"""Bir bölümü dengeli parçalara bölme (`eval run --part k/n`).

Canlı koşu örnek başına token harcar; dev bölümü parça parça koşulabilsin diye örnekler `n`
parçaya ayrılır. Bölme belirleyicidir (yalnız kimliklere ve etiketlere bağlı) ve her parçada dil/
motor grubu ile örnek türü (sözdizimi hatalı, injection, temiz, hatalı) orantılı kalır; böylece
her parça tüm bölümün küçük bir kopyası gibi davranır ve parçaların sonuçları birleştirilebilir.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from collections.abc import Sequence

from codementor.eval.breakdown import group_of
from codementor.models.eval import Label, RunResult, Sample

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


def _assign(samples: list[Sample], parts: int) -> dict[str, int]:
    """Örnek kimliği → parça (0..n-1); grup, tür ve boyut sayıları parçalar arasında dengeli.

    Döngüsel ilk atamadan sonra tek örnek taşıma ve iki örnek takası, her (öznitelik, parça)
    sayısının karesel toplamını küçülttüğü sürece uygulanır. Ortalama sabit olduğundan bu,
    sapmayı küçültür; dev ve test bölümlerinde olağan parça sayılarında fark en fazla 1 olur.
    """
    ordered = sorted(samples, key=lambda s: s.label.id)
    attrs = {
        s.label.id: (("group", group_of(s.label)), ("kind", sample_kind(s.label)), ("size", ""))
        for s in ordered
    }
    by_cell = sorted(ordered, key=lambda s: (group_of(s.label), sample_kind(s.label), s.label.id))
    out = {s.label.id: i % parts for i, s in enumerate(by_cell)}
    counts: Counter[tuple[tuple[str, str], int]] = Counter()
    for sample_id, part in out.items():
        for attr in attrs[sample_id]:
            counts[attr, part] += 1

    def improves(change: Counter[tuple[tuple[str, str], int]]) -> bool:
        delta = sum((counts[k] + v) ** 2 - counts[k] ** 2 for k, v in change.items() if v)
        if delta < 0:
            counts.update(change)
        return delta < 0

    def moved(sample_id: str, source: int, target: int) -> Counter[tuple[tuple[str, str], int]]:
        change: Counter[tuple[tuple[str, str], int]] = Counter()
        for attr in attrs[sample_id]:
            change[attr, source] -= 1
            change[attr, target] += 1
        return change

    ids = list(attrs)
    improved = True
    while improved:
        improved = False
        for a in ids:
            for target in range(parts):
                if target != out[a] and improves(moved(a, out[a], target)):
                    out[a], improved = target, True
        for i, a in enumerate(ids):
            for b in ids[i + 1 :]:
                pa, pb = out[a], out[b]
                if pa == pb:
                    continue
                swap = moved(a, pa, pb)
                swap.update(moved(b, pb, pa))  # `+` sıfır/negatifleri atardı; `update` korur
                if improves(swap):
                    out[a], out[b], improved = pb, pa, True
    return out


def select_part(samples: list[Sample], index: int, parts: int) -> list[Sample]:
    """`index`. parça örnekleri (kimlik sırasıyla).

    Bölme belirleyicidir ve girdi sırasından bağımsızdır; her dil/motor grubu, örnek türü ve
    parça boyutu parçalara olabildiğince eşit (hedef: en fazla 1 fark) dağılır (`_assign`).
    """
    assignment = _assign(samples, parts)
    return sorted(
        (s for s in samples if assignment[s.label.id] == index - 1), key=lambda s: s.label.id
    )


def part_signature(samples: list[Sample], parts: int) -> str:
    """Parça atamasının deterministik kimlik özeti (Faz I / İş 10)."""
    assignment = _assign(samples, parts)
    lines = [f"{s_id}:{p}" for s_id, p in sorted(assignment.items())]
    digest = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
    return f"p{parts}+{digest[:8]}"


def check_parts_coverage(
    part_results: list[RunResult],
    all_sample_ids: Sequence[str] | None = None,
) -> tuple[list[str], list[str]]:
    """Parçalı sonuçların çakışan ve eksik örnek kimliklerini denetler (Faz I / İş 10).

    Dönüş: (çakışan_kimlikler, eksik_kimlikler)
    """
    seen: set[str] = set()
    overlapping: set[str] = set()
    for r in part_results:
        for sid in r.config.sample_ids:
            if sid in seen:
                overlapping.add(sid)
            seen.add(sid)
    missing: list[str] = []
    if all_sample_ids is not None:
        expected = set(all_sample_ids)
        missing = sorted(expected - seen)
    return sorted(overlapping), missing
