"""Veri modeli testleri (mimari §6).

Bölüm 1/2.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from codementor.models import findings, llm_output, report
from codementor.models.enums import (
    AuditCategory,
    CompilationStatus,
    Difficulty,
    Engine,
    FindingKind,
    FindingSource,
    Language,
    LoopBound,
    PipelineMode,
    Severity,
)
from codementor.models.findings import CompilationBlock, Diagnostic, Finding
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMComplexity,
    LLMFinding,
    LLMSocraticOutput,
    LLMVerifyOutput,
)
from codementor.models.report import (
    AnalysisReport,
    ComplexityResult,
    ReportMeta,
    SocraticResult,
)
from tests.unit.models_support import (
    _fields,
    _llm_finding,
)

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
        (FindingKind, {"issue", "suggestion"}),
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
            {
                "category",
                "severity",
                "line_start",
                "line_end",
                "evidence",
                "description",
                "certainty",
                "kind",  # Faz 36
            },
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
                "kind",  # Faz 36
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
                "concept_revealed",  # Faz C (Y6)
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
                "usage_estimated",  # Faz 25 (§13)
                "cost_est",
                "stage_tokens",  # Faz K
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


def test_llm_finding_valid() -> None:
    f = LLMFinding.model_validate(_llm_finding())
    assert f.category is AuditCategory.PERFORMANCE
    assert f.line_end is None


def test_llm_finding_certainty_optional() -> None:
    assert LLMFinding.model_validate(_llm_finding()).certainty is None
    assert LLMFinding.model_validate(_llm_finding(certainty="high")).certainty == "high"
    with pytest.raises(ValidationError):
        LLMFinding.model_validate(_llm_finding(certainty="kesin"))


def test_llm_finding_kind_optional() -> None:
    assert LLMFinding.model_validate(_llm_finding()).kind == "issue"
    assert LLMFinding.model_validate(_llm_finding(kind="suggestion")).kind == "suggestion"
    with pytest.raises(ValidationError):
        LLMFinding.model_validate(_llm_finding(kind="hint"))


def test_llm_verify_output_limits() -> None:
    verdict = {"finding": 1, "verdict": "proven", "requirement": "boş girdi", "reason": "x"}
    LLMVerifyOutput.model_validate({"verdicts": [verdict] * 10})
    with pytest.raises(ValidationError):
        LLMVerifyOutput.model_validate({"verdicts": [verdict] * 11})
    with pytest.raises(ValidationError):
        LLMVerifyOutput.model_validate({"verdicts": [{**verdict, "finding": 0}]})
    with pytest.raises(ValidationError):
        LLMVerifyOutput.model_validate({"verdicts": [{**verdict, "reason": "y" * 401}]})
    assert not (_fields(LLMVerifyOutput) & {"source", "confidence", "id", "rule_id"})


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
