"""Halüsinasyon fixture'ları: `tests/fixtures/llm_responses/*.json` uçtan uca doğrulayıcıdan geçer.

`live_*` dosyaları gerçek claude_cli yanıtlarıdır; diğerleri onlardan türetilmiş sentetik hata
türleridir (yanlış satır, var olmayan kanıt, çatışma, sızıntı ...). Her dosyada `expect` var.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from codementor.analysis.complexity_hint import compute_hint
from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, FindingSource, Language
from codementor.models.llm_output import LLMAnalysisOutput, LLMSocraticOutput
from codementor.models.request import LanguageHint
from codementor.rules import all_rules
from codementor.rules.engine import run_rules
from codementor.verify.analysis import verify_analysis, verify_socratic
from codementor.verify.schema_check import check_schema

REPO = Path(__file__).resolve().parents[3]
FIXTURES = REPO / "tests" / "fixtures" / "llm_responses"
CASES = sorted(FIXTURES.glob("*.json"))
RULES = {r.id: r for r in all_rules()}


def _load(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return data


def _run_analysis(case: dict[str, Any]) -> Any:
    code = normalize(
        (REPO / case["code"]).read_bytes(),
        LanguageHint(language=Language(case["language"]), engine=Engine(case["engine"])),
    )
    facts = extract_facts(code)
    static = run_rules(code, facts, disabled=[]).findings
    output, schema = check_schema(
        LLMAnalysisOutput,
        parsed=case["response"]["parsed"],
        raw_text=case["response"]["raw_text"],
    )
    assert schema.ok, schema.errors
    assert output is not None
    return verify_analysis(
        output,
        code=code,
        static_findings=static,
        hint=compute_hint(facts),
        expected=None,
        schema_first_try=True,
    )


def _run_socratic(case: dict[str, Any]) -> Any:
    code = normalize(
        (REPO / case["code"]).read_bytes(),
        LanguageHint(language=Language(case["language"]), engine=Engine(case["engine"])),
    )
    output = LLMSocraticOutput.model_validate(case["response"]["parsed"])
    reference = (REPO / case["reference"]).read_text(encoding="utf-8")
    return verify_socratic(
        output,
        code=code,
        hint_level=1,
        question=None,
        reference=reference,
        regenerated=case["regenerated"],
    )


def test_fixture_set_is_complete() -> None:
    names = {p.stem for p in CASES}
    required = {
        "live_claude_analysis",
        "live_claude_socratic",
        "wrong_line",
        "missing_evidence",
        "conflict_unjustified",
        "conflict_justified",
        "leak_forbidden_identifier",
        "leak_code_block_after_regeneration",
    }
    assert required <= names
    assert all(_load(p)["expect"] for p in CASES)


@pytest.mark.parametrize(
    "path", [p for p in CASES if _load(p)["pass"] == "analysis"], ids=lambda p: p.stem
)
def test_analysis_fixture(path: Path) -> None:
    case = _load(path)
    expect = case["expect"]
    result = _run_analysis(case)
    reasons = result.repair.reasons if result.repair else []
    assert reasons == expect["repair"]
    if "complexity" in expect:
        assert result.complexity is expect["complexity"]
    if "time" in expect:
        assert result.complexity is not None
        assert result.complexity.time_complexity == expect["time"]
        assert result.complexity.agreement == expect["agreement"]
    if "confidence" in expect:
        assert result.confidence == pytest.approx(expect["confidence"])
    if "dropped" in expect:
        assert len(result.warnings) == expect["dropped"]
    llm = [f for f in result.findings if f.source == FindingSource.LLM]
    if "llm_lines" in expect:
        assert sorted(f.line_start for f in llm) == expect["llm_lines"]
    if "shifted_lines" in expect:
        shifted = sorted(f.line_start for f in llm if f.confidence < 0.7)
        assert shifted == expect["shifted_lines"]
    for rule, line in expect.get("confirmed", []):
        (merged,) = [f for f in result.findings if f.rule_id == rule and f.line_start == line]
        assert merged.source == FindingSource.CONFIRMED
        assert merged.severity == RULES[rule].default_severity  # statik önem öncelikli


@pytest.mark.parametrize(
    "path", [p for p in CASES if _load(p)["pass"] == "socratic"], ids=lambda p: p.stem
)
def test_socratic_fixture(path: Path) -> None:
    case = _load(path)
    expect = case["expect"]
    result = _run_socratic(case)
    assert result.decision.action == expect["action"]
    assert sorted(v.kind for v in result.decision.violations) == sorted(expect["violations"])
    if "leak_check" in expect:
        assert result.result is not None
        assert result.result.leak_check == expect["leak_check"]
    if "kept_questions" in expect:
        assert len(result.decision.guiding_questions) == expect["kept_questions"]
