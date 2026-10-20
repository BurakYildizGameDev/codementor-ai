"""Karmaşıklık politikası (Faz I / İş 11, ADR-0031).

Küçük modeller statik analiz ipucuyla çeliştiğinde deterministik statik
ipucunu önceliklendirir.
"""

from __future__ import annotations

from codementor.models.bigo import parse_bigo
from codementor.models.questions import ExpectedComplexity
from codementor.models.report import ComplexityResult
from codementor.verify.complexity import is_optimal


def apply_complexity_policy(
    complexity: ComplexityResult | None,
    model_profile: str = "standard",
    expected: ExpectedComplexity | None = None,
) -> tuple[ComplexityResult | None, list[str]]:
    """Model profiline göre karmaşıklık sonucunu değerlendirir ve gerekirse düzeltir.

    Küçük model profilinde (small), model statik analizle çatışırsa (conflicts)
    deterministik statik ipucu önceliklendirilir; gösterim ve optimallik ipucundan
    normal yolla aynı biçimde yeniden hesaplanır (`expected`: sorunun beklenen karmaşıklığı).
    """
    if complexity is None or model_profile != "small":
        return complexity, []

    # Statik ipucu var ve model onunla çelişiyorsa
    if complexity.static_hint and complexity.agreement == "conflicts":
        old = parse_bigo(complexity.time_complexity)
        hint = parse_bigo(complexity.static_hint)
        note = (
            f"[Deterministik Statik Analiz]: Küçük modelin tahmini ({old.display}) "
            f"yerine doğrulanmış statik analiz sınırı ({hint.display}) tercih edildi."
        )
        # agreement "agrees": zaman artık ipucunun kendisi; çatışma bilgisi not ve uyarıda kalır.
        # confidence analiz geneli skordur (verification.confidence ile aynı), değişmez.
        updated = complexity.model_copy(
            update={
                "time_complexity": hint.canonical,
                "display_time": hint.display,
                "is_optimal": is_optimal(hint, expected),
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
