"""Veri modeli testleri (mimari §6).

Bölüm 2/2.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from codementor.models.enums import (
    AllocationKind,
    AuditCategory,
    CompilationStatus,
    Language,
    LoopBound,
    PipelineMode,
)
from codementor.models.facts import (
    AllocationFact,
    CodeFacts,
    ComplexityHint,
    LoopFact,
    RecursionFact,
)
from codementor.models.findings import Diagnostic, Finding
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMComplexity,
    LLMFinding,
    LLMSocraticOutput,
)
from codementor.models.report import (
    AnalysisReport,
    SocraticResult,
)
from codementor.models.request import AnalysisOptions, AnalysisRequest
from tests.unit.models_support import (
    _complexity,
    _finding,
    _llm_finding,
    _report,
    _socratic,
)


def test_llm_finding_boundaries_accepted() -> None:
    LLMFinding.model_validate(_llm_finding(line_start=1, evidence="x" * 200, description="y" * 400))


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


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_confidence_range(confidence: float) -> None:
    with pytest.raises(ValidationError):
        Finding.model_validate(_finding(confidence=confidence))


def test_finding_kind_defaults_to_issue() -> None:
    assert Finding.model_validate(_finding()).kind == "issue"
    assert Finding.model_validate(_finding(kind="suggestion")).kind == "suggestion"
    with pytest.raises(ValidationError):
        Finding.model_validate(_finding(kind="note"))


def test_finding_required_nullable_fields() -> None:
    data = _finding()
    del data["rule_id"]
    with pytest.raises(ValidationError):
        Finding.model_validate(data)


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


def test_report_minimal_early_exit() -> None:
    r = AnalysisReport.model_validate(_report())
    assert r.schema_version == "1.1"
    assert r.compilation.status is CompilationStatus.FAILED
    assert r.complexity is None


def test_report_schema_version_fixed() -> None:
    with pytest.raises(ValidationError):
        AnalysisReport.model_validate(_report(schema_version="2.0"))


def test_report_v1_0_json_still_loads() -> None:
    """Faz 36 öncesi rapor (geçmiş, önbellek): `kind` yok, sürüm 1.0; bulgular hata sayılır."""
    old = AnalysisReport.model_validate(_report(findings=[_finding()])).model_dump(mode="json")
    old["schema_version"] = "1.0"
    del old["findings"][0]["kind"]
    report = AnalysisReport.model_validate(old)
    assert report.schema_version == "1.0"
    assert report.findings[0].kind == "issue"


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


@pytest.mark.parametrize("field", ["question_id", "session_id", "provider"])
def test_request_identifier_limits(field: str) -> None:
    """Faz 47: kimlikler ≤ 128 karakter, `^[A-Za-z0-9_.-]+$`."""
    assert getattr(AnalysisRequest.model_validate({"code": "x", field: "a" * 128}), field)
    AnalysisRequest.model_validate({"code": "x", field: "desktop-1a2b.c_d"})
    for bad in ("a" * 129, "a/b", "a b", "", "ı"):
        with pytest.raises(ValidationError):
            AnalysisRequest.model_validate({"code": "x", field: bad})


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


# ---------------------------------------------------------------- Faz 27: biçim sınırları


@pytest.mark.parametrize(
    "bad_id",
    [
        "",
        "01J9ZK4M8Q3W6Y2T5R7N1B0C9",
        "01J9ZK4M8Q3W6Y2T5R7N1B0C9DX",
        "01J9ZK4M8Q3W6Y2T5R7N1B0C9U",
        "01j9zk4m8q3w6y2t5r7n1b0c9d",
        "../../etc/passwd000000000",
        "01J9ZK4M8Q3W6Y2T5R7N1B0CI0",
    ],
)
def test_report_rejects_non_ulid_id(bad_id: str) -> None:
    with pytest.raises(ValidationError):
        AnalysisReport.model_validate(_report(analysis_id=bad_id))


def test_new_ulid_matches_report_pattern() -> None:
    from codementor.pipeline.ids import new_ulid

    for _ in range(50):
        AnalysisReport.model_validate(_report(analysis_id=new_ulid()))


def test_guiding_question_length_limited_in_schema() -> None:
    ok = {"key_flaw_concept": "x", "guiding_questions": ["a" * 1000]}
    LLMSocraticOutput.model_validate(ok)
    with pytest.raises(ValidationError):
        LLMSocraticOutput.model_validate({**ok, "guiding_questions": ["a" * 1001]})
    items = LLMSocraticOutput.model_json_schema()["properties"]["guiding_questions"]["items"]
    assert items["maxLength"] == 1000


def test_proof_basis_accepts_scaling() -> None:
    """Faz 39: performans/GC bulgusu ölçek kanıtıyla korunabilir."""
    from codementor.models.verification import FindingCheck

    check = FindingCheck(
        finding_id="F-001",
        line_start=6,
        category=AuditCategory.PERFORMANCE,
        kept=True,
        basis="scaling",
    )
    assert check.basis == "scaling"


def test_sample_result_reads_old_files_without_checks() -> None:
    """Faz 39 öncesi sonuç dosyalarında `finding_checks` yok; boş liste okunur."""
    from codementor.models.eval import SampleResult

    old = SampleResult.model_validate({"id": "c-001", "latency_ms": 5})
    assert old.finding_checks == []
