"""Karmaşıklık politikası testleri (Faz I / İş 11, ADR-0031)."""

from __future__ import annotations

import pytest

from codementor.models.questions import ExpectedComplexity
from codementor.models.report import ComplexityResult
from codementor.verify.complexity_policy import apply_complexity_policy


def _make_complexity(
    time: str = "n^2",
    static_hint: str | None = "n",
    agreement: str = "conflicts",
    is_optimal: bool | None = False,
) -> ComplexityResult:
    return ComplexityResult(
        time_complexity=time,
        space_complexity="1",
        display_time=f"O({time})",
        reasoning_steps=["Model döngünün karesel olduğunu iddia ediyor."],
        is_optimal=is_optimal,
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
    assert result.confidence == comp.confidence
    assert any("Deterministik Statik Analiz" in step for step in result.reasoning_steps)
    assert any("deterministik statik ipucu tercih edildi" in w for w in warnings)


def test_small_profile_display_matches_parse_bigo() -> None:
    """Tam tarama #4: gösterim normal yolla aynı (`O(n²)`), ham `O(n^2)` değil."""
    comp = _make_complexity(time="n", static_hint="n^2", agreement="conflicts")
    result, _ = apply_complexity_policy(comp, model_profile="small")

    assert result is not None
    assert result.time_complexity == "n^2"
    assert result.display_time == "O(n²)"
    note = result.reasoning_steps[0]
    assert "O(n)" in note
    assert "O(n²)" in note
    assert "O(n^2)" not in note


@pytest.mark.parametrize(
    ("model_time", "hint", "target", "was_optimal", "now_optimal"),
    [
        # Model "n" dedi (optimal sanıldı), statik ipucu n^2 → artık optimal değil
        ("n", "n^2", "n", True, False),
        # Model "n^2" dedi (optimal değil sanıldı), statik ipucu n → hedef n^2 ise optimal
        ("n^2", "n", "n^2", False, True),
    ],
)
def test_small_profile_recomputes_is_optimal_from_hint(
    model_time: str, hint: str, target: str, was_optimal: bool, now_optimal: bool
) -> None:
    comp = _make_complexity(time=model_time, static_hint=hint, is_optimal=was_optimal)
    expected = ExpectedComplexity(time={"f": target}, space="1")
    result, _ = apply_complexity_policy(comp, model_profile="small", expected=expected)

    assert result is not None
    assert result.is_optimal is now_optimal


def test_small_profile_without_question_has_no_optimality() -> None:
    comp = _make_complexity(time="n", static_hint="n^2", is_optimal=None)
    result, _ = apply_complexity_policy(comp, model_profile="small", expected=None)

    assert result is not None
    assert result.is_optimal is None


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
