"""Sokratik kalite kapısı kararının uygulanması (`socratic_pass.apply_gate`, tam tarama #5)."""

from __future__ import annotations

from codementor.models.report import SocraticResult
from codementor.models.verification import LeakDecision, SocraticVerification
from codementor.pipeline.socratic_pass import apply_gate
from codementor.verify.socratic_gate import SocraticGateResult

QUESTIONS = ["low değişkeni ne zaman değişir?", "mid nasıl hesaplanır?"]
NO_TOUCH = "Sokratik sorular koddaki hiçbir öğeye veya satıra temas etmiyor."


def _checked(questions: list[str] = QUESTIONS) -> SocraticVerification:
    result = SocraticResult(
        key_flaw_concept="k",
        hint_level=2,
        guiding_questions=questions,
        next_step_hint=None,
        leak_check="passed",
    )
    return SocraticVerification(
        decision=LeakDecision(action="passed", guiding_questions=questions),
        result=result,
        warnings=["önceki uyarı"],
    )


def _gate(
    questions: list[str], *, passed: bool = True, warnings: list[str] | None = None
) -> SocraticGateResult:
    return SocraticGateResult(
        passed=passed, filtered_questions=questions, next_step_hint=None, warnings=warnings or []
    )


def test_warning_kept_when_questions_unchanged() -> None:
    """Standart profilde kapı geçer ama uyarır: soru listesi aynı diye uyarı kaybolmamalı."""
    checked = _checked()
    out = apply_gate(checked, _gate(QUESTIONS, warnings=[NO_TOUCH]))
    assert out.result == checked.result
    assert out.warnings == ["önceki uyarı", NO_TOUCH]


def test_unchanged_and_silent_gate_returns_same_object() -> None:
    checked = _checked()
    assert apply_gate(checked, _gate(QUESTIONS)) is checked


def test_filtered_questions_replace_result() -> None:
    out = apply_gate(_checked(), _gate(QUESTIONS[:1], warnings=["1 adet soru elendi."]))
    assert out.result is not None
    assert out.result.guiding_questions == QUESTIONS[:1]
    assert out.warnings[-1] == "1 adet soru elendi."


def test_failed_gate_drops_result_with_warnings() -> None:
    out = apply_gate(_checked(), _gate([], passed=False, warnings=["döngüsel tekrar"]))
    assert out.result is None
    assert out.warnings == ["önceki uyarı", "döngüsel tekrar"]
