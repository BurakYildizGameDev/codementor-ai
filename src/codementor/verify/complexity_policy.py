"""Karmaşıklık politikası (Faz I / İş 11, ADR-0031).

Küçük modeller statik analiz ipucuyla çeliştiğinde deterministik statik
ipucunu önceliklendirir.
"""

from __future__ import annotations

from codementor.models.report import ComplexityResult


def apply_complexity_policy(
    complexity: ComplexityResult | None,
    model_profile: str = "standard",
) -> tuple[ComplexityResult | None, list[str]]:
    """Model profiline göre karmaşıklık sonucunu değerlendirir ve gerekirse düzeltir.

    Küçük model profilinde (small), model statik analizle çatışırsa (conflicts)
    deterministik statik ipucu önceliklendirilir.
    """
    if complexity is None or model_profile != "small":
        return complexity, []

    # Statik ipucu var ve model onunla çelişiyorsa
    if complexity.static_hint and complexity.agreement == "conflicts":
        old_time = complexity.time_complexity
        hint = complexity.static_hint
        note = (
            f"[Deterministik Statik Analiz]: Küçük modelin tahmini (O({old_time})) "
            f"yerine doğrulanmış statik analiz sınırı (O({hint})) tercih edildi."
        )
        updated = complexity.model_copy(
            update={
                "time_complexity": hint,
                "display_time": f"O({hint})",
                "agreement": "agrees",
                "reasoning_steps": [note, *complexity.reasoning_steps],
            }
        )
        warning = (
            "Küçük model karmaşıklık analizi statik ipucuyla çeliştiği için "
            "deterministik statik ipucu tercih edildi."
        )
        return updated, [warning]

    return complexity, []
