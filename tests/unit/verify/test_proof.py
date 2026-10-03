"""Faz 35: bulgu doğrulama geçişinin kararlarını uygulayan saf fonksiyonlar."""

from __future__ import annotations

from typing import Any

from codementor.verify.proof import apply_verdicts, redact_reasons, verify_targets

from codementor.models.enums import AuditCategory, FindingSource, Severity
from codementor.models.findings import Finding
from codementor.models.llm_output import LLMVerifyOutput


def _finding(line: int, source: FindingSource = FindingSource.LLM) -> Finding:
    return Finding(
        id=f"F-{line:03d}",
        rule_id="C-MEM-001" if source is not FindingSource.LLM else None,
        category=AuditCategory.EDGE_CASE,
        severity=Severity.MEDIUM,
        line_start=line,
        line_end=None,
        evidence=f"satir{line}",
        description="açıklama",
        source=source,
        confidence=0.7,
    )


def _output(*verdicts: dict[str, Any]) -> LLMVerifyOutput:
    return LLMVerifyOutput.model_validate({"verdicts": list(verdicts)})


def _proven_input(index: int) -> dict[str, Any]:
    return {
        "finding": index,
        "verdict": "proven",
        "input": "n = 0",
        "expected": "0 döner",
        "actual": "sıfıra bölme",
        "reason": "Boş dizide bölen sıfır olur.",
    }


def _unproven(index: int) -> dict[str, Any]:
    return {"finding": index, "verdict": "unproven", "reason": "Somut girdi bulamadım."}


FINDINGS = [_finding(3), _finding(5, FindingSource.STATIC), _finding(8), _finding(9)]


def test_static_and_confirmed_not_sent() -> None:
    findings = [*FINDINGS, _finding(12, FindingSource.CONFIRMED)]
    assert [f.line_start for f in verify_targets(findings)] == [3, 8, 9]


def test_unproven_finding_dropped() -> None:
    result = apply_verdicts(FINDINGS, _output(_proven_input(1), _unproven(2), _proven_input(3)))
    assert [f.line_start for f in result.findings] == [3, 5, 9]
    assert result.dropped == 1
    assert [f.id for f in result.findings] == ["F-001", "F-002", "F-003"]  # yeniden numara
    assert any("8. satır" in w and "atıldı" in w for w in result.warnings)
    dropped = [c for c in result.checks if not c.kept]
    assert [(c.line_start, c.basis) for c in dropped] == [(8, "unproven")]


def test_proven_with_input_kept() -> None:
    result = apply_verdicts(FINDINGS, _output(_proven_input(1), _proven_input(2), _proven_input(3)))
    assert result.dropped == 0
    assert len(result.findings) == 4
    assert {c.basis for c in result.checks} == {"input"}
    assert result.warnings == []


def test_proven_with_requirement_kept() -> None:
    verdict = {
        "finding": 1,
        "verdict": "proven",
        "requirement": "Kısıt: boş dizi doğru ele alınmalı",
        "reason": "Boş dizi kontrolü yok.",
    }
    result = apply_verdicts(FINDINGS, _output(verdict, _proven_input(2), _proven_input(3)))
    assert result.dropped == 0
    assert result.checks[0].basis == "requirement"


def test_proven_without_demonstration_dropped() -> None:
    """`proven` dedi ama girdi/beklenen/gerçekleşen ya da gereksinim göstermedi."""
    partial = {"finding": 1, "verdict": "proven", "input": "n = 0", "expected": " ", "reason": "x"}
    result = apply_verdicts(FINDINGS, _output(partial, _proven_input(2), _proven_input(3)))
    assert result.dropped == 1
    assert result.checks[0].basis == "no_demonstration"
    assert 3 not in [f.line_start for f in result.findings if f.source is FindingSource.LLM]


def test_missing_verdict_keeps_finding_and_warns() -> None:
    result = apply_verdicts(FINDINGS, _output(_proven_input(1), _proven_input(3)))
    assert result.dropped == 0
    assert len(result.findings) == 4
    missing = [c for c in result.checks if c.basis == "no_verdict"]
    assert [(c.line_start, c.kept) for c in missing] == [(8, True)]
    assert any("8. satır" in w and "korundu" in w for w in result.warnings)


def test_unknown_index_ignored_and_first_verdict_wins() -> None:
    result = apply_verdicts(
        FINDINGS,
        _output(_proven_input(1), _unproven(1), _proven_input(2), _proven_input(3), _unproven(7)),
    )
    assert result.dropped == 0
    assert len(result.checks) == 3


def test_leaky_reason_redacted() -> None:
    result = apply_verdicts(FINDINGS, _output(_proven_input(1), _unproven(2), _proven_input(3)))
    redacted = redact_reasons(result.checks, {1})
    assert redacted[1].reason == ""
    assert redacted[0].reason == result.checks[0].reason
    assert [c.kept for c in redacted] == [c.kept for c in result.checks]
