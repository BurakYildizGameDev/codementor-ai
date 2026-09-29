"""Erken çıkış politikası (mimari §5.2.4).

| Durum                                             | Karar                                  |
|---------------------------------------------------|----------------------------------------|
| Tier 0 `ERROR`/`MISSING` düğümü                   | Erken çıkış (`FAILED`)                 |
| Tier 1 kesin hata (C/C++/C#)                      | Erken çıkış (`FAILED`)                 |
| Tier 1 Unreal stub hatası / eksik başlık          | Devam, `WARNING` (Tier 1 uyarıya düşürür) |
| Yalnızca derleyici uyarıları                      | Devam, `WARNING`; uyarılar tanılarda   |
| Tier 1 zaman aşımı / derleyici yok / include kor. | Devam, `SKIPPED`                       |
| Tier 1 temiz                                      | Devam, `PASSED`                        |

Erken çıkış raporunun Sokratik şablon mesajları rapor katmanındadır (Faz 10).
"""

from __future__ import annotations

from codementor.models.enums import CompilationStatus
from codementor.models.validation import PolicyDecision, Tier0Result, Tier1Result


def decide_tier0(result: Tier0Result) -> PolicyDecision:
    """Yalnızca Tier 0 sonucuna göre karar (Tier 1 henüz çalışmadıysa)."""
    if result.has_errors:
        return PolicyDecision(
            status=CompilationStatus.FAILED, early_exit=True, diagnostics=result.diagnostics
        )
    return PolicyDecision(
        status=CompilationStatus.PASSED, early_exit=False, diagnostics=result.diagnostics
    )


def decide(tier0: Tier0Result, tier1: Tier1Result | None) -> PolicyDecision:
    """§5.2.4 tablosunun tamamı. Tier 0 hatası varsa Tier 1 sonucu yok sayılır."""
    if tier0.has_errors or tier1 is None:
        return decide_tier0(tier0)
    return PolicyDecision(
        status=tier1.status,
        early_exit=tier1.status is CompilationStatus.FAILED,
        diagnostics=[*tier0.diagnostics, *tier1.diagnostics],
        warnings=list(tier1.warnings),
    )
