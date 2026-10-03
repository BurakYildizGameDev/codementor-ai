"""Güven skoru (mimari §5.6).

confidence = 0.4·şema_ilk_denemede_geçti
           + 0.3·statik_ipucu_ile_uyum (uyum = 1, gerekçeli çatışma = 0.5, ipucu yok = 0.6)
           + 0.3·kanıt_eşleşme_oranı
"""

from __future__ import annotations

from codementor.models.llm_output import Certainty
from codementor.models.verification import AgreementState

SCHEMA_WEIGHT = 0.4
AGREEMENT_WEIGHT = 0.3
EVIDENCE_WEIGHT = 0.3
AGREEMENT_SCORES: dict[AgreementState, float] = {
    "agrees": 1.0,
    "justified_conflict": 0.5,
    "no_hint": 0.6,
    "unjustified_conflict": 0.0,  # onarım da başarısız olduysa (zarif bozulma)
}

# Bulgu başına güven
LLM_EXACT_CONFIDENCE = 0.7  # kanıt bildirilen satırda bulundu
LLM_SHIFTED_CONFIDENCE = 0.6  # kanıt bulundu, satır düzeltildi
CONFIRMED_CONFIDENCE = 0.95  # statik kural + LLM aynı sorunu bağımsız buldu
# Modelin kendi beyanı (Faz 35): kanıt bildirilen satırda bulunduysa; satır düzeltildiyse eksi
CERTAINTY_CONFIDENCE: dict[Certainty, float] = {"high": 0.85, "medium": 0.7, "low": 0.5}
SHIFTED_PENALTY = 0.1


def finding_confidence(certainty: Certainty | None, *, shifted: bool) -> float:
    """LLM bulgusunun rapordaki güveni; model beyan etmediyse eski sabitler (Faz 9)."""
    if certainty is None:
        return LLM_SHIFTED_CONFIDENCE if shifted else LLM_EXACT_CONFIDENCE
    score = CERTAINTY_CONFIDENCE[certainty] - (SHIFTED_PENALTY if shifted else 0.0)
    return round(score, 4)


def evidence_ratio(matched: int, total: int) -> float:
    """Kanıtı doğrulanan LLM bulgusu oranı; LLM bulgu vermediyse doğrulanmamış iddia yok: 1."""
    if total <= 0:
        return 1.0
    return max(0.0, min(1.0, matched / total))


def analysis_confidence(
    schema_first_try: bool, agreement: AgreementState, evidence: float
) -> float:
    """§5.6 formülü; sonuç her zaman [0, 1]."""
    score = (
        SCHEMA_WEIGHT * float(schema_first_try)
        + AGREEMENT_WEIGHT * AGREEMENT_SCORES[agreement]
        + EVIDENCE_WEIGHT * max(0.0, min(1.0, evidence))
    )
    return round(max(0.0, min(1.0, score)), 4)
