"""Bulgu sağduyu denetimi (Faz I / İş 11, ADR-0031).

Küçük modellerin ürettiği çelişkili bulguları (ör. kanıt satırı if kontrolü iken
"kontrol edilmiyor" iddiası) ve küçük model profilinde aşırı bulgu üretimini denetler.
"""

from __future__ import annotations

import re

from codementor.models.enums import FindingSource, Severity
from codementor.models.findings import Finding

# Kanıt satırında bir koşullu kontrol/guard olduğuna işaret eden kalıplar
_GUARD_EVIDENCE_RE = re.compile(
    r"\b(if\s*\(|if\s+|switch\s*\(|assert\b|guard\b|\bnull\b|\bnullptr\b|\bNone\b|[!=]=|[<>]=?)",
    re.IGNORECASE,
)

# Açıklamada "kontrol edilmiyor / eksik" iddiasına işaret eden kalıplar
_MISSING_CHECK_RE = re.compile(
    r"(kontrol\s*(edilmiyor|edilmemiş|yok|eksik)|denetlenmiyor|denetlenmemiş|"
    r"not\s*checked|missing\s*check|no\s*check|unhandled)",
    re.IGNORECASE,
)

_SEVERITY_ORDER: dict[Severity, int] = {
    Severity.HIGH: 3,
    Severity.MEDIUM: 2,
    Severity.LOW: 1,
}

MAX_SMALL_PROFILE_FINDINGS = 3


def is_guard_hallucination(description: str, evidence: str) -> bool:
    """Kanıt satırı bizzat bir kontrol iken 'kontrol edilmiyor' iddiası var mı denetler."""
    if not description or not evidence:
        return False
    return bool(_MISSING_CHECK_RE.search(description) and _GUARD_EVIDENCE_RE.search(evidence))


def apply_sanity_checks(
    findings: list[Finding],
    model_profile: str = "standard",
) -> tuple[list[Finding], list[str]]:
    """Bulgulara sağduyu denetimleri uygular.

    1. Ters kontrol çelişkisi olan LLM bulguları düşürülür.
    2. 'small' profilinde LLM bulgularına tavan (en fazla 3 bulgu) konur; statik bulgular
       her zaman korunur.
    """
    valid: list[Finding] = []
    warnings: list[str] = []

    for f in findings:
        # Statik bulgular sağduyu elemesine girmez
        if f.source == FindingSource.STATIC:
            valid.append(f)
            continue

        if is_guard_hallucination(f.description, f.evidence):
            warnings.append(
                f"Model bulgusu ({f.id}) kanıt satırındaki kontrolle çeliştiği için düşürüldü: "
                f"{f.evidence.strip()}"
            )
            continue
        valid.append(f)

    if model_profile == "small":
        static_findings = [f for f in valid if f.source == FindingSource.STATIC]
        llm_findings = [f for f in valid if f.source != FindingSource.STATIC]

        if len(llm_findings) > MAX_SMALL_PROFILE_FINDINGS:
            # Önem sırasına göre sıralayıp ilk 3'ü tut
            sorted_llm = sorted(
                llm_findings,
                key=lambda item: _SEVERITY_ORDER.get(item.severity, 0),
                reverse=True,
            )
            kept_llm = sorted_llm[:MAX_SMALL_PROFILE_FINDINGS]
            dropped_count = len(llm_findings) - MAX_SMALL_PROFILE_FINDINGS
            warnings.append(
                f"Küçük model profilinde {dropped_count} adet düşük öncelikli bulgu sınırlandı "
                f"(tavan: {MAX_SMALL_PROFILE_FINDINGS})."
            )
            # Orijinal satır sırasını koru
            valid = sorted(
                [*static_findings, *kept_llm],
                key=lambda item: (item.line_start, item.id),
            )

    return valid, warnings
