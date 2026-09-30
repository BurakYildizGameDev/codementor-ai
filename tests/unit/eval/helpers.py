"""Eval testleri için küçük etiket / rapor kurucuları."""

from __future__ import annotations

from datetime import UTC, datetime

from codementor.models.enums import (
    AuditCategory,
    CompilationStatus,
    Engine,
    FindingSource,
    Language,
    Severity,
)
from codementor.models.eval import Expected, ExpectedFinding, Label, SampleResult
from codementor.models.findings import CompilationBlock, Finding
from codementor.models.report import AnalysisReport, ComplexityResult, ReportMeta, SocraticResult

MEM = AuditCategory.MEMORY_SAFETY
PERF = AuditCategory.PERFORMANCE


def label(
    sample_id: str = "c-001",
    *,
    syntax_valid: bool = True,
    time: str | None = None,
    findings: list[tuple[AuditCategory, int]] | None = None,
    must_not_contain: list[str] | None = None,
    tags: list[str] | None = None,
) -> Label:
    return Label(
        id=sample_id,
        language=Language.C,
        engine=Engine.NONE,
        syntax_valid=syntax_valid,
        expected=Expected(
            compilation_status=CompilationStatus.PASSED
            if syntax_valid
            else CompilationStatus.FAILED,
            time_complexity=time,
            findings=[ExpectedFinding(category=c, line=line) for c, line in findings or []],
            must_not_contain=must_not_contain or [],
        ),
        tags=tags or [],
    )


def finding(category: AuditCategory, line: int, fid: str = "F-001") -> Finding:
    return Finding(
        id=fid,
        rule_id=None,
        category=category,
        severity=Severity.MEDIUM,
        line_start=line,
        line_end=None,
        evidence="x",
        description="d",
        source=FindingSource.LLM,
        confidence=0.7,
    )


def report(
    *,
    time: str | None = None,
    findings: list[Finding] | None = None,
    questions: list[str] | None = None,
    hint: str | None = None,
    early_exit: bool = False,
    degraded: bool = False,
    tokens: tuple[int, int] = (0, 0),
    provider: str | None = "fake",
    model: str | None = "m",
) -> AnalysisReport:
    complexity = None
    if time is not None:
        complexity = ComplexityResult(
            time_complexity=time,
            space_complexity="1",
            display_time=f"O({time})",
            reasoning_steps=["adım"],
            is_optimal=None,
            optimal_time_target=None,
            static_hint=None,
            agreement="no_hint",
            confidence=0.5,
        )
    socratic = None
    if questions is not None:
        socratic = SocraticResult(
            key_flaw_concept="k",
            hint_level=1,
            guiding_questions=questions,
            next_step_hint=hint,
            leak_check="passed",
        )
    return AnalysisReport(
        analysis_id="01J0000000000000000000000A",
        created_at=datetime(2026, 9, 30, tzinfo=UTC),
        language=Language.C,
        engine=Engine.NONE,
        question_id=None,
        difficulty=None,
        compilation=CompilationBlock(
            status=CompilationStatus.FAILED if early_exit else CompilationStatus.PASSED,
            diagnostics=[],
        ),
        complexity=complexity,
        findings=findings or [],
        socratic=socratic,
        meta=ReportMeta(
            provider=provider,
            model=model,
            prompt_version="v1+x",
            rules_version="r1+y",
            schema_version="1.0",
            tokens_in=tokens[0],
            tokens_out=tokens[1],
            stage_latency_ms={},
            early_exit=early_exit,
            cache_hit=False,
            degraded=degraded,
            repair_attempts=0,
            warnings=[],
        ),
    )


def result(
    rep: AnalysisReport | None,
    *,
    sample_id: str = "c-001",
    latency: int = 1000,
    first: bool | None = None,
    final: bool | None = None,
    llm: bool = False,
    error: str | None = None,
) -> SampleResult:
    return SampleResult(
        id=sample_id,
        report=rep,
        error=error,
        latency_ms=latency,
        llm_called=llm,
        schema_first_try=first,
        schema_final=final,
    )
