"""Bulgu birleştirme ve önem sağlaması (mimari §5.6, 6.-7. satırlar).

Aynı kategori + satır farkı ≤ 2 olan statik ve LLM bulgusu tek bulgu olur (`confirmed`);
önem ve metin statik kuraldan gelir (statik kuralın önemi önceliklidir).
"""

from __future__ import annotations

from codementor.models.enums import FindingSource
from codementor.models.findings import Finding
from codementor.verify.confidence import CONFIRMED_CONFIDENCE

MERGE_LINE_DISTANCE = 2


def _near(a: Finding, b: Finding) -> bool:
    return a.category == b.category and abs(a.line_start - b.line_start) <= MERGE_LINE_DISTANCE


def _dedupe_llm(findings: list[Finding]) -> list[Finding]:
    """LLM'in aynı sorunu iki kez yazması: aynı kategori ve yakın satırda ilki kalır."""
    unique: list[Finding] = []
    for finding in findings:
        if not any(_near(finding, kept) for kept in unique):
            unique.append(finding)
    return unique


def number_findings(findings: list[Finding]) -> list[Finding]:
    """Satır sırasıyla `F-001…` kimlikleri (statik motorla aynı sıralama)."""
    ordered = sorted(findings, key=lambda f: (f.line_start, f.rule_id or "", f.category))
    return [f.model_copy(update={"id": f"F-{i:03d}"}) for i, f in enumerate(ordered, start=1)]


def merge_findings(static: list[Finding], llm: list[Finding]) -> list[Finding]:
    """Statik + doğrulanmış LLM bulguları → tek liste; eşleşen çift `confirmed` olur.

    Her LLM bulgusu en yakın (satır farkı en küçük) eşleşmemiş statik bulguyla birleşir;
    bir statik bulgu en fazla bir LLM bulgusunu emer.
    """
    merged = list(static)
    confirmed: set[int] = set()
    extra: list[Finding] = []
    for finding in _dedupe_llm(llm):
        candidates = [i for i, s in enumerate(static) if i not in confirmed and _near(s, finding)]
        if not candidates:
            if not any(_near(finding, static[i]) for i in confirmed):
                extra.append(finding)
            continue
        best = min(candidates, key=lambda i: abs(static[i].line_start - finding.line_start))
        confirmed.add(best)
        base = static[best]
        merged[best] = base.model_copy(
            update={
                "source": FindingSource.CONFIRMED,
                "confidence": max(base.confidence, finding.confidence, CONFIRMED_CONFIDENCE),
            }
        )
    return number_findings(merged + extra)
