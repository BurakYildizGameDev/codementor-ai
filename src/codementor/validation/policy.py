"""Erken çıkış politikası (mimari §5.2.4).

Bu fazda yalnızca Tier 0 satırı uygulanır; Tier 1 satırları Faz 4'te eklenir.

| Durum                           | Karar                                  |
|---------------------------------|----------------------------------------|
| Tier 0 `ERROR`/`MISSING` düğümü | Erken çıkış (`compilation_status = FAILED`) |
| Tier 0 temiz                    | Devam (`PASSED`; Tier 1 sonucu günceller)  |
"""

from __future__ import annotations

from codementor.models.enums import CompilationStatus
from codementor.models.validation import PolicyDecision, Tier0Result


def decide_tier0(result: Tier0Result) -> PolicyDecision:
    """Tier 0 sonucuna göre erken çıkış kararı."""
    if result.has_errors:
        return PolicyDecision(
            status=CompilationStatus.FAILED, early_exit=True, diagnostics=result.diagnostics
        )
    return PolicyDecision(
        status=CompilationStatus.PASSED, early_exit=False, diagnostics=result.diagnostics
    )
