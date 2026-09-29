"""Erken çıkış politikası testleri (mimari §5.2.4, yalnızca Tier 0 satırları)."""

from __future__ import annotations

from codementor.models.validation import Tier0Result
from codementor.validation.policy import decide_tier0

from codementor.models.enums import CompilationStatus
from codementor.models.findings import Diagnostic


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
