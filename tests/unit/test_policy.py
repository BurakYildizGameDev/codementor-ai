"""Erken çıkış politikası testleri (mimari §5.2.4)."""

from __future__ import annotations

from typing import Literal

import pytest

from codementor.models.enums import CompilationStatus
from codementor.models.findings import Diagnostic
from codementor.models.validation import SkipReason, Tier0Result, Tier1Result
from codementor.validation.policy import decide, decide_tier0


def _diag(line: int = 3) -> Diagnostic:
    return Diagnostic(tool="tree-sitter", severity="error", line=line, column=5, message="x")


def test_tier0_error_means_early_exit() -> None:
    decision = decide_tier0(Tier0Result(diagnostics=[_diag()]))
    assert decision.status is CompilationStatus.FAILED
    assert decision.early_exit
    assert decision.diagnostics == [_diag()]


def test_clean_tier0_continues() -> None:
    decision = decide_tier0(Tier0Result(diagnostics=[]))
    assert decision.status is CompilationStatus.PASSED
    assert not decision.early_exit
    assert decision.diagnostics == []


def test_decision_converts_to_compilation_block() -> None:
    block = decide_tier0(Tier0Result(diagnostics=[_diag(7)])).to_block()
    assert block.status is CompilationStatus.FAILED
    assert block.diagnostics[0].line == 7


# ------------------------------------------------------------------ §5.2.4 tam tablo (Tier 1)


def _t1(
    status: CompilationStatus,
    diagnostics: list[Diagnostic] | None = None,
    skip: SkipReason | None = None,
    warnings: list[str] | None = None,
) -> Tier1Result:
    return Tier1Result(
        status=status,
        tool="gcc",
        diagnostics=diagnostics or [],
        skip_reason=skip,
        warnings=warnings or [],
    )


def _gcc(severity: Literal["error", "warning", "note"]) -> Diagnostic:
    return Diagnostic(tool="gcc", severity=severity, line=4, column=2, message="m")


def test_tier0_error_wins_over_tier1() -> None:
    decision = decide(Tier0Result(diagnostics=[_diag()]), _t1(CompilationStatus.PASSED))
    assert decision.status is CompilationStatus.FAILED
    assert decision.early_exit
    assert decision.diagnostics == [_diag()]


def test_tier1_hard_error_early_exit() -> None:
    decision = decide(Tier0Result(diagnostics=[]), _t1(CompilationStatus.FAILED, [_gcc("error")]))
    assert decision.status is CompilationStatus.FAILED
    assert decision.early_exit
    assert decision.diagnostics == [_gcc("error")]


def test_tier1_warnings_continue_with_warning() -> None:
    tier1 = _t1(CompilationStatus.WARNING, [_gcc("warning")], warnings=["not"])
    decision = decide(Tier0Result(diagnostics=[]), tier1)
    assert decision.status is CompilationStatus.WARNING
    assert not decision.early_exit
    assert decision.diagnostics == [_gcc("warning")]
    assert decision.warnings == ["not"]


@pytest.mark.parametrize(
    "reason",
    [
        SkipReason.TIMEOUT,
        SkipReason.TOOL_MISSING,
        SkipReason.INCLUDE_GUARD,
        SkipReason.DISABLED,
        SkipReason.TOOL_ERROR,
        SkipReason.STUB_MISSING,
    ],
)
def test_tier1_skipped_continues(reason: SkipReason) -> None:
    decision = decide(
        Tier0Result(diagnostics=[]), _t1(CompilationStatus.SKIPPED, skip=reason, warnings=["w"])
    )
    assert decision.status is CompilationStatus.SKIPPED
    assert not decision.early_exit
    assert decision.warnings == ["w"]


def test_tier1_clean_passes() -> None:
    decision = decide(Tier0Result(diagnostics=[]), _t1(CompilationStatus.PASSED))
    assert decision.status is CompilationStatus.PASSED
    assert not decision.early_exit


def test_no_tier1_result_falls_back_to_tier0() -> None:
    assert decide(Tier0Result(diagnostics=[]), None) == decide_tier0(Tier0Result(diagnostics=[]))
