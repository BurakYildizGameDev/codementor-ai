"""Veri modeli testleri (mimari §6)."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from codementor.models import findings, llm_output, report
from codementor.models.enums import (
    AllocationKind,
    AuditCategory,
    CompilationStatus,
    Difficulty,
    Engine,
    FindingSource,
    Language,
    LoopBound,
    PipelineMode,
    Severity,
)
from codementor.models.facts import (
    AllocationFact,
    CodeFacts,
    ComplexityHint,
    LoopFact,
    RecursionFact,
)
from codementor.models.findings import CompilationBlock, Diagnostic, Finding
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMComplexity,
    LLMFinding,
    LLMSocraticOutput,
)
from codementor.models.report import (
    AnalysisReport,
    ComplexityResult,
    ReportMeta,
    SocraticResult,
)
from codementor.models.request import AnalysisOptions, AnalysisRequest


def _fields(model: type[BaseModel]) -> set[str]:
    return set(model.model_fields)


# ---------------------------------------------------------------- enum'lar (§6.2)


@pytest.mark.parametrize(
    ("enum", "values"),
    [
        (Language, {"c", "cpp", "csharp", "python", "html", "css"}),
        (Engine, {"none", "unity", "unreal"}),
        (Difficulty, {"very_easy", "easy", "medium", "hard"}),
        (Severity, {"high", "medium", "low"}),
        (CompilationStatus, {"passed", "warning", "failed", "skipped"}),
        (FindingSource, {"static", "llm", "confirmed"}),
        (
            AuditCategory,
            {
                "memory_safety",
                "resource_leak",
                "undefined_behavior",
                "garbage_collection",
                "performance",
                "engine_best_practice",
                "edge_case",
                "input_handling",
                "design",
                "accessibility",
                "maintainability",
            },
        ),
        (LoopBound, {"linear", "log", "constant", "unknown"}),
        (PipelineMode, {"two_pass", "single_pass"}),
    ],
)
def test_enum_values(enum: type[StrEnum], values: set[str]) -> None:
    assert {m.value for m in enum} == values


def test_enums_are_str() -> None:
    assert Language.CSHARP == "csharp"
    assert f"{Severity.HIGH}" == "high"


# ---------------------------------------------------------------- modül ayrımı (§6.1)


def test_llm_and_report_models_in_separate_modules() -> None:
    assert LLMFinding.__module__ == llm_output.__name__
    assert LLMAnalysisOutput.__module__ == llm_output.__name__
    assert LLMSocraticOutput.__module__ == llm_output.__name__
    assert AnalysisReport.__module__ == report.__name__
    assert Finding.__module__ == findings.__name__
    # LLM modülü rapor modüllerini içe aktarmamalı.
    assert not hasattr(llm_output, "AnalysisReport")
    assert not hasattr(llm_output, "Finding")


def test_llm_schemas_have_no_system_fields() -> None:
    system_fields = {"source", "confidence", "id", "rule_id", "meta", "compilation"}
    assert not (_fields(LLMFinding) & system_fields)
    assert not (_fields(LLMAnalysisOutput) & system_fields)
    assert not (_fields(LLMSocraticOutput) & system_fields)


# ---------------------------------------------------------------- alan eşleşmesi


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        (
            LLMFinding,
            {"category", "severity", "line_start", "line_end", "evidence", "description"},
        ),
        (
            LLMComplexity,
            {
                "reasoning_steps",
                "time_complexity",
                "space_complexity",
                "optimal_time_target",
                "agreement",
            },
        ),
        (LLMAnalysisOutput, {"complexity", "additional_findings"}),
        (LLMSocraticOutput, {"key_flaw_concept", "guiding_questions", "next_step_hint"}),
        (Diagnostic, {"tool", "severity", "line", "column", "message"}),
        (
            Finding,
            {
                "id",
                "rule_id",
                "category",
                "severity",
                "line_start",
                "line_end",
                "evidence",
                "description",
                "source",
                "confidence",
            },
        ),
        (
            ComplexityResult,
            {
                "time_complexity",
                "space_complexity",
                "display_time",
                "reasoning_steps",
                "is_optimal",
                "optimal_time_target",
                "static_hint",
                "agreement",
                "confidence",
            },
        ),
        (
            SocraticResult,
            {
                "key_flaw_concept",
                "hint_level",
                "guiding_questions",
                "next_step_hint",
                "leak_check",
            },
        ),
        (
            ReportMeta,
            {
                "provider",
                "model",
                "prompt_version",
                "rules_version",
                "schema_version",
                "tokens_in",
                "tokens_out",
                "stage_latency_ms",
                "early_exit",
                "cache_hit",
                "degraded",
                "repair_attempts",
                "warnings",
            },
        ),
        (
            AnalysisReport,
            {
                "schema_version",
                "analysis_id",
                "created_at",
                "language",
                "engine",
                "question_id",
                "difficulty",
                "compilation",
                "complexity",
                "findings",
                "socratic",
                "meta",
            },
        ),
        (CompilationBlock, {"status", "diagnostics"}),
    ],
)
def test_fields_match_spec(model: type[BaseModel], expected: set[str]) -> None:
    assert _fields(model) == expected


# ---------------------------------------------------------------- LLM modelleri (§6.3)


def _llm_finding(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "category": "performance",
        "severity": "medium",
        "line_start": 3,
        "line_end": None,
        "evidence": "for (int i = 0; i < n; i++)",
        "description": "İç içe döngü.",
    }
    return base | kw


def test_llm_finding_valid() -> None:
    f = LLMFinding.model_validate(_llm_finding())
    assert f.category is AuditCategory.PERFORMANCE
    assert f.line_end is None


def test_llm_finding_line_end_defaults_to_none() -> None:
    data = _llm_finding()
    del data["line_end"]
    assert LLMFinding.model_validate(data).line_end is None


@pytest.mark.parametrize(
    "override",
    [
        {"line_start": 0},
        {"evidence": "x" * 201},
        {"description": "x" * 401},
        {"category": "style"},
        {"severity": "critical"},
    ],
)
def test_llm_finding_limits(override: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        LLMFinding.model_validate(_llm_finding(**override))


def test_llm_finding_boundaries_accepted() -> None:
    LLMFinding.model_validate(_llm_finding(line_start=1, evidence="x" * 200, description="y" * 400))


def _complexity(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "reasoning_steps": ["Dış döngü n kez döner."],
        "time_complexity": "O(n^2)",
        "space_complexity": "O(1)",
        "optimal_time_target": None,
        "agreement": "agrees",
    }
    return base | kw


@pytest.mark.parametrize("steps", [[], ["a"] * 9])
def test_llm_complexity_steps_bounds(steps: list[str]) -> None:
    with pytest.raises(ValidationError):
        LLMComplexity.model_validate(_complexity(reasoning_steps=steps))


def test_llm_complexity_optimal_target_required_but_nullable() -> None:
    data = _complexity()
    del data["optimal_time_target"]
    with pytest.raises(ValidationError):
        LLMComplexity.model_validate(data)


def test_llm_complexity_agreement_literal() -> None:
    with pytest.raises(ValidationError):
        LLMComplexity.model_validate(_complexity(agreement="maybe"))


def test_llm_analysis_max_findings() -> None:
    ok = {"complexity": _complexity(), "additional_findings": [_llm_finding()] * 10}
    assert len(LLMAnalysisOutput.model_validate(ok).additional_findings) == 10
    with pytest.raises(ValidationError):
        LLMAnalysisOutput.model_validate(ok | {"additional_findings": [_llm_finding()] * 11})


@pytest.mark.parametrize("questions", [[], ["?"] * 5])
def test_socratic_questions_bounds(questions: list[str]) -> None:
    with pytest.raises(ValidationError):
        LLMSocraticOutput.model_validate({"key_flaw_concept": "GC", "guiding_questions": questions})


def test_socratic_limits() -> None:
    with pytest.raises(ValidationError):
        LLMSocraticOutput.model_validate({"key_flaw_concept": "x" * 81, "guiding_questions": ["?"]})
    with pytest.raises(ValidationError):
        LLMSocraticOutput.model_validate(
            {"key_flaw_concept": "GC", "guiding_questions": ["?"], "next_step_hint": "x" * 301}
        )
    out = LLMSocraticOutput.model_validate({"key_flaw_concept": "GC", "guiding_questions": ["?"]})
    assert out.next_step_hint is None


@pytest.mark.parametrize(
    ("model", "data"),
    [
        (LLMFinding, _llm_finding(source="llm")),
        (LLMComplexity, _complexity(confidence=0.9)),
        (LLMSocraticOutput, {"key_flaw_concept": "GC", "guiding_questions": ["?"], "x": 1}),
    ],
)
def test_extra_fields_forbidden(model: type[BaseModel], data: dict[str, Any]) -> None:
    with pytest.raises(ValidationError, match="extra"):
        model.model_validate(data)


def test_llm_json_schema_disallows_additional_properties() -> None:
    schema = LLMAnalysisOutput.model_json_schema()
    assert schema["additionalProperties"] is False
    for definition in schema["$defs"].values():
        if definition.get("type") == "object":
            assert definition["additionalProperties"] is False


# ---------------------------------------------------------------- rapor modelleri (§6.4)


def _finding(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "id": "F-001",
        "rule_id": None,
        "category": "memory_safety",
        "severity": "high",
        "line_start": 5,
        "line_end": 6,
        "evidence": "free(p);",
        "description": "Çift serbest bırakma.",
        "source": "static",
        "confidence": 1.0,
    }
    return base | kw


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_confidence_range(confidence: float) -> None:
    with pytest.raises(ValidationError):
        Finding.model_validate(_finding(confidence=confidence))


def test_finding_required_nullable_fields() -> None:
    data = _finding()
    del data["rule_id"]
    with pytest.raises(ValidationError):
        Finding.model_validate(data)


def _socratic(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "key_flaw_concept": "GC",
        "hint_level": 1,
        "guiding_questions": ["Neden?"],
        "next_step_hint": None,
        "leak_check": "passed",
    }
    return base | kw


@pytest.mark.parametrize("level", [0, 4])
def test_hint_level_range(level: int) -> None:
    with pytest.raises(ValidationError):
        SocraticResult.model_validate(_socratic(hint_level=level))


def test_leak_check_literal() -> None:
    for value in ("passed", "regenerated", "dropped_questions", "skipped"):
        SocraticResult.model_validate(_socratic(leak_check=value))
    with pytest.raises(ValidationError):
        SocraticResult.model_validate(_socratic(leak_check="failed"))


def test_diagnostic_tool_literal() -> None:
    d = {"tool": "gcc", "severity": "error", "line": 1, "column": None, "message": "x"}
    assert Diagnostic.model_validate(d).tool == "gcc"
    with pytest.raises(ValidationError):
        Diagnostic.model_validate(d | {"tool": "msvc"})


def _meta() -> dict[str, Any]:
    return {
        "provider": None,
        "model": None,
        "prompt_version": "v1",
        "rules_version": "1.0.0",
        "schema_version": "1.0",
        "tokens_in": 0,
        "tokens_out": 0,
        "stage_latency_ms": {},
        "early_exit": True,
        "cache_hit": False,
        "degraded": False,
        "repair_attempts": 0,
        "warnings": [],
    }


def _report(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "analysis_id": "01J9ZK4M8Q3W6Y2T5R7N1B0C9D",
        "created_at": datetime(2026, 9, 29, tzinfo=UTC),
        "language": "c",
        "engine": "none",
        "question_id": None,
        "difficulty": None,
        "compilation": {"status": "failed", "diagnostics": []},
        "complexity": None,
        "findings": [],
        "socratic": None,
        "meta": _meta(),
    }
    return base | kw


def test_report_minimal_early_exit() -> None:
    r = AnalysisReport.model_validate(_report())
    assert r.schema_version == "1.0"
    assert r.compilation.status is CompilationStatus.FAILED
    assert r.complexity is None


def test_report_schema_version_fixed() -> None:
    with pytest.raises(ValidationError):
        AnalysisReport.model_validate(_report(schema_version="2.0"))


def test_report_json_roundtrip() -> None:
    r = AnalysisReport.model_validate(_report(findings=[_finding()]))
    again = AnalysisReport.model_validate_json(r.model_dump_json())
    assert again == r


# ---------------------------------------------------------------- istek


def test_request_defaults() -> None:
    req = AnalysisRequest.model_validate({"code": "int main(){}"})
    assert req.language is None
    assert req.engine is None
    assert req.options == AnalysisOptions()
    assert req.options.mode is None  # None → config'deki pipeline.mode


def test_request_api_example() -> None:
    req = AnalysisRequest.model_validate(
        {
            "code": "#include <stdio.h>\nint main(){ return 0; }",
            "language": "c",
            "engine": "none",
            "question_id": "c-veryeasy-calculator",
            "session_id": "local-user-1",
            "provider": "ollama",
            "options": {"mode": "two_pass", "tier1": True, "use_cache": True},
        }
    )
    assert req.language is Language.C
    assert req.options.mode is PipelineMode.TWO_PASS


def test_request_rejects_empty_code_and_extras() -> None:
    with pytest.raises(ValidationError):
        AnalysisRequest.model_validate({"code": ""})
    with pytest.raises(ValidationError):
        AnalysisRequest.model_validate({"code": "x", "hint_level": 2})


# ---------------------------------------------------------------- olgular (§5.3.1)


def test_code_facts_defaults_empty() -> None:
    facts = CodeFacts()
    assert facts.functions == []
    assert facts.loops == []
    assert facts.engine_symbols.uproperty_fields == []
    assert facts.engine_symbols.has_on_enable is False


def test_loop_fact_validation() -> None:
    loop = LoopFact(kind="foreach", line=31, depth=1, bound=LoopBound.LINEAR, function="RefreshUI")
    assert loop.bound is LoopBound.LINEAR
    with pytest.raises(ValidationError):
        LoopFact.model_validate(
            {"kind": "loop", "line": 1, "depth": 1, "bound": "linear", "function": None}
        )
    with pytest.raises(ValidationError):
        LoopFact.model_validate(
            {"kind": "for", "line": 1, "depth": 0, "bound": "linear", "function": None}
        )


def test_recursion_and_allocation_facts() -> None:
    rec = RecursionFact(function="fib", self_call_count=2, branching_factor=2, lines=[4, 4])
    assert rec.branching_factor == 2
    alloc = AllocationFact(
        kind=AllocationKind.CSHARP_NEW, line=14, loop_depth=0, in_hot_path=True, function="Update"
    )
    assert alloc.in_hot_path


def test_complexity_hint_normalizes_value() -> None:
    hint = ComplexityHint(value="O(N*N)", confidence="medium", basis=["satır 3: iç içe döngü"])
    assert hint.value == "n^2"
    assert hint.exponential_suspect is False


def test_complexity_hint_rejects_unparseable_value() -> None:
    with pytest.raises(ValidationError, match="ayrıştırılamadı"):
        ComplexityHint(value="çok yavaş", confidence="low", basis=[])
