"""Karmaşıklık politikası testleri (Faz I / İş 11, ADR-0031)."""

from __future__ import annotations

from codementor.models.report import ComplexityResult
from codementor.verify.complexity_policy import apply_complexity_policy


def _make_complexity(
    time: str = "n^2",
    static_hint: str | None = "n",
    agreement: str = "conflicts",
) -> ComplexityResult:
    return ComplexityResult(
        time_complexity=time,
        space_complexity="1",
        display_time=f"O({time})",
        reasoning_steps=["Model döngünün karesel olduğunu iddia ediyor."],
        is_optimal=False,
        optimal_time_target="n",
        static_hint=static_hint,
        agreement=agreement,  # type: ignore[arg-type]
        confidence=0.8,
    )


def test_standard_profile_keeps_conflicts() -> None:
    comp = _make_complexity(time="n^2", static_hint="n", agreement="conflicts")
    result, warnings = apply_complexity_policy(comp, model_profile="standard")

    assert result == comp
    assert len(warnings) == 0


def test_small_profile_prefers_static_hint_on_conflict() -> None:
    comp = _make_complexity(time="n^2", static_hint="n", agreement="conflicts")
    result, warnings = apply_complexity_policy(comp, model_profile="small")

    assert result is not None
    assert result.time_complexity == "n"
    assert result.display_time == "O(n)"
    assert result.agreement == "agrees"
    assert any("Deterministik Statik Analiz" in step for step in result.reasoning_steps)
    assert any("deterministik statik ipucu tercih edildi" in w for w in warnings)


def test_small_profile_no_hint_or_agrees_unchanged() -> None:
    # Zaten uzlaşıyorsa
    agreed = _make_complexity(time="n", static_hint="n", agreement="agrees")
    res1, warn1 = apply_complexity_policy(agreed, model_profile="small")
    assert res1 == agreed
    assert len(warn1) == 0

    # Statik ipucu yoksa
    no_hint = _make_complexity(time="n", static_hint=None, agreement="no_hint")
    res2, warn2 = apply_complexity_policy(no_hint, model_profile="small")
    assert res2 == no_hint
    assert len(warn2) == 0
