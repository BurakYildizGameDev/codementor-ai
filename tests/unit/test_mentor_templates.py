"""LLM'siz mentor şablonları (mimari §5.2.4, §5.6)."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.models.enums import AuditCategory, FindingSource, Severity
from codementor.models.findings import Diagnostic, Finding
from codementor.models.prompts import QuestionContext
from codementor.models.questions import ExpectedComplexity
from codementor.pipeline.templates import (
    degraded_socratic,
    early_exit_socratic,
    fallback_description,
    load_templates,
)

TEMPLATES = load_templates(Path(__file__).resolve().parents[2] / "data" / "mentor_templates.yaml")


def _diag(message: str, line: int = 4, severity: str = "error") -> Diagnostic:
    return Diagnostic(tool="tree-sitter", severity=severity, line=line, column=1, message=message)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("Burada noktalı virgül (;) eksik görünüyor.", "`;` ile bitmiyor"),
        ("expected ';' before 'return'", "`;` ile bitmiyor"),
        ("CS1002: ; expected", "`;` ile bitmiyor"),
        (
            "Satır 2 ile başlayan blok kapanmamış görünüyor; dosyanın sonunda '}' eksik olabilir.",
            "`{` için bir `}`",
        ),
        ("Burada kapanış parantezi ()) eksik görünüyor.", "parantez"),
        ("Beklenmeyen sözdizimi: 'x y z'", "anlamsız geliyor"),
        ("use of undeclared identifier 'foo'", "derleyici şunu söylüyor"),
    ],
)
def test_early_exit_template_by_diagnostic(message: str, expected: str) -> None:
    result = early_exit_socratic(TEMPLATES, [_diag(message)], hint_level=1)
    assert expected in result.guiding_questions[0]
    assert result.leak_check == "skipped"
    assert result.next_step_hint


def test_early_exit_orders_dedupes_and_limits() -> None:
    diags = [
        _diag("expected ';'", line=9),
        _diag("expected ';'", line=2),
        _diag("expected ';'", line=2),
    ]
    diags += [_diag(f"hata {i}", line=20 + i) for i in range(5)]
    result = early_exit_socratic(TEMPLATES, diags, hint_level=2)
    assert result.guiding_questions[0].startswith("2. satırda")
    assert len(result.guiding_questions) == 3
    assert result.hint_level == 2


def test_early_exit_warnings_only_still_produces_question() -> None:
    result = early_exit_socratic(TEMPLATES, [_diag("uyarı", severity="warning")], 1)
    assert result.guiding_questions


def _finding(category: AuditCategory, severity: Severity, line: int) -> Finding:
    return Finding(
        id="F-1",
        rule_id=None,
        category=category,
        severity=severity,
        line_start=line,
        line_end=None,
        evidence="x",
        description="d",
        source=FindingSource.STATIC,
        confidence=0.9,
    )


def test_degraded_level_one_is_conceptual_and_level_two_points_to_line() -> None:
    findings = [
        _finding(AuditCategory.PERFORMANCE, Severity.LOW, 3),
        _finding(AuditCategory.GARBAGE_COLLECTION, Severity.HIGH, 12),
    ]
    level1 = degraded_socratic(TEMPLATES, findings, None, 1)
    assert "satır" not in " ".join(level1.guiding_questions)
    assert level1.key_flaw_concept == "Çöp toplayıcı baskısı"  # en önemli bulgu
    level2 = degraded_socratic(TEMPLATES, findings, None, 2)
    assert level2.guiding_questions[0].startswith("12. satır")


def test_degraded_uses_question_hint_ladder_first() -> None:
    question = QuestionContext(
        id="q",
        title="t",
        prompt="p",
        constraints=["c"],
        difficulty="medium",  # type: ignore[arg-type]
        expected=ExpectedComplexity(time={"f": "n"}, space="1"),
        hint_ladder={1: "Merdiven sorusu 1?", 2: "Merdiven 2?"},
    )
    result = degraded_socratic(TEMPLATES, [], question, 2)
    assert result.guiding_questions[0] == "Merdiven 2?"


def test_degraded_without_findings_generic() -> None:
    result = degraded_socratic(TEMPLATES, [], None, 1)
    assert result.guiding_questions == [TEMPLATES.degraded_generic]
    assert result.key_flaw_concept == TEMPLATES.degraded_concept


def test_every_category_has_template() -> None:
    assert set(TEMPLATES.categories) == set(AuditCategory)


def test_fallback_description() -> None:
    text = fallback_description(TEMPLATES, _finding(AuditCategory.EDGE_CASE, Severity.LOW, 1))
    assert "Uç durum" in text
