"""Süre sınırı yardımcıları (G0): `Orchestrator._timed_out` ve `_remaining` bunları çağırır.

Adlar `Orchestrator` üzerinde yöntem olarak kalır: testler `Orchestrator._remaining`'i
`monkeypatch` ile yamalıyor (tests/integration/test_pipeline_partial.py, test_pipeline_timeout.py).
"""

from __future__ import annotations

import time

from codementor.pipeline.llm_session import LLMSession
from codementor.pipeline.passes import LLMOutcome
from codementor.pipeline.verify_pass import VERIFY_FAILED


def timed_out(llm: LLMSession, limit: float | None) -> LLMOutcome:
    """Süre sınırı: Geçiş A bittiyse doğrulanmış bulgular korunur, sorular şablondan
    (Faz B, Y4); bitmediyse rapor statik analizle."""
    if llm.checkpoint is None:
        llm.warnings.append(
            f"Analiz süre sınırı ({limit:g} sn) aşıldı; rapor statik analizle hazırlandı."
        )
        return LLMOutcome(verification=None, socratic=None)
    llm.incomplete = True
    if not llm.checkpoint_verified:
        llm.warnings.append(VERIFY_FAILED)
    llm.warnings.append(
        f"Analiz süre sınırı ({limit:g} sn) aşıldı; bulgular korundu, mentor soruları şablondan."
    )
    return LLMOutcome(verification=llm.checkpoint, socratic=None)


def remaining(started: float, limit: float | None) -> float | None:
    """Toplam süre sınırından kalan saniye (Tier 0/1 ve statik aşama düşülmüş); yoksa None."""
    if limit is None:
        return None
    return max(limit - (time.monotonic() - started), 0.0)
