"""Rapor biçimleri (mimari §5.7): SARIF resmi 2.1.0 şemasına karşı, Markdown, Rich."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from jsonschema import Draft4Validator
from rich.console import Console

from codementor.models.enums import (
    AuditCategory,
    CompilationStatus,
    Engine,
    FindingSource,
    Language,
    Severity,
)
from codementor.models.findings import CompilationBlock, Diagnostic, Finding
from codementor.models.report import AnalysisReport, ComplexityResult, ReportMeta, SocraticResult
from codementor.report.cli_render import print_report
from codementor.report.markdown import to_markdown
from codementor.report.sarif import rule_id, to_sarif

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[1] / "fixtures" / "sarif-schema-2.1.0.json").read_text(
        encoding="utf-8"
    )
)
CODE = (
    "int f(int *a, int n) {\n    int s = 0;\n"
    "    for (int i = 0; i <= n; i++) s += a[i];\n    return s;\n}\n"
)


def _finding(fid: str, rule: str | None, source: FindingSource, severity: Severity) -> Finding:
    return Finding(
        id=fid,
        rule_id=rule,
        category=AuditCategory.MEMORY_SAFETY,
        severity=severity,
        line_start=3,
        line_end=None,
        evidence="i <= n",
        description="Döngünün son turunda i = n olur; dizi sınırı | aşılıyor mu?",
        source=source,
        confidence=0.9,
    )


def _report(
    *,
    early: bool = False,
    hint_level: int = 1,
    diagnostics: list[Diagnostic] | None = None,
) -> AnalysisReport:
    return AnalysisReport(
        analysis_id="01J0000000000000000000000A",
        created_at=datetime(2026, 9, 30, tzinfo=UTC),
        language=Language.C,
        engine=Engine.NONE,
        question_id=None,
        difficulty=None,
        compilation=CompilationBlock(
            status=CompilationStatus.FAILED if early else CompilationStatus.PASSED,
            diagnostics=diagnostics or [],
        ),
        complexity=None
        if early
        else ComplexityResult(
            time_complexity="n",
            space_complexity="1",
            display_time="O(n)",
            reasoning_steps=["Tek döngü."],
            is_optimal=True,
            optimal_time_target="n",
            static_hint="n",
            agreement="agrees",
            confidence=1.0,
        ),
        findings=[]
        if early
        else [
            _finding("F-001", "C-BUF-001", FindingSource.CONFIRMED, Severity.HIGH),
            _finding("F-002", None, FindingSource.LLM, Severity.LOW),
        ],
        socratic=SocraticResult(
            key_flaw_concept="Sınır dışı erişim",
            hint_level=hint_level,
            guiding_questions=["n elemanlı dizide son indis kaçtır?"],
            next_step_hint="Döngüyü n = 2 için izle.",
            leak_check="passed",
        ),
        meta=ReportMeta(
            provider="fake",
            model="m",
            prompt_version="v1+abc",
            rules_version="r1+def",
            schema_version="1.0",
            tokens_in=10,
            tokens_out=5,
            stage_latency_ms={"tier0": 1},
            early_exit=early,
            cache_hit=False,
            degraded=False,
            repair_attempts=0,
            warnings=["Bir not."],
        ),
    )


DIAG = [Diagnostic(tool="gcc", severity="error", line=2, column=14, message="expected ';'")]


@pytest.mark.parametrize("report", [_report(), _report(early=True, diagnostics=DIAG)])
def test_sarif_validates_against_official_schema(report: AnalysisReport) -> None:
    log = to_sarif(report, "src\\ornek.c")
    Draft4Validator(SCHEMA).validate(log)  # kabul: resmi SARIF 2.1.0 şeması
    assert log["version"] == "2.1.0"


def test_sarif_results_map_findings() -> None:
    log = to_sarif(_report(), "src\\ornek.c")
    run = log["runs"][0]
    ids = [r["ruleId"] for r in run["results"]]
    assert ids == ["C-BUF-001", "CM-LLM-MEMORY-SAFETY"]
    assert [r["level"] for r in run["results"]] == ["error", "note"]
    location = run["results"][0]["locations"][0]["physicalLocation"]
    assert location["artifactLocation"]["uri"] == "src/ornek.c"
    assert location["region"] == {"startLine": 3, "snippet": {"text": "i <= n"}}
    assert {r["id"] for r in run["tool"]["driver"]["rules"]} == set(ids)


def test_sarif_compile_diagnostics() -> None:
    log = to_sarif(_report(early=True, diagnostics=DIAG), "a.c")
    (result,) = log["runs"][0]["results"]
    assert result["ruleId"] == "CM-COMPILE"
    assert result["locations"][0]["physicalLocation"]["region"]["startColumn"] == 14


def test_rule_id_for_llm_finding() -> None:
    assert rule_id(_finding("F", None, FindingSource.LLM, Severity.LOW)) == "CM-LLM-MEMORY-SAFETY"


def test_markdown_sections_and_escaping() -> None:
    md = to_markdown(_report())
    assert "## Karmaşıklık" in md
    assert "O(n)" in md
    assert "| F-001 | 3 |" in md
    assert "sınırı \\| aşılıyor" in md  # tablo hücresinde | kaçışlanır
    assert "## Mentor soruları" in md
    assert "Sınır dışı erişim" not in md  # seviye 1: kavram adı gösterilmez
    assert "**Kavram:** Sınır dışı erişim" in to_markdown(_report(hint_level=3))


def test_markdown_early_exit() -> None:
    md = to_markdown(_report(early=True, diagnostics=DIAG))
    assert "derleme aşamasında durdu" in md
    assert "2. satır (error): expected ';'" in md


def _rich(report: AnalysisReport, code: str | None = CODE) -> str:
    console = Console(record=True, width=100, color_system=None)
    print_report(report, console, code)
    return console.export_text()


def test_rich_shows_code_snippet_with_line_numbers() -> None:
    text = _rich(_report())
    assert "F-001" in text
    assert "YÜKSEK" in text
    assert "for (int i = 0; i <= n; i++)" in text  # vurgulanan satır
    assert "3 " in text
    assert "Mentor soruları (ipucu seviyesi 1)" in text
    assert "Sınır dışı erişim" not in text


def test_rich_without_code_and_level_three() -> None:
    text = _rich(_report(hint_level=3), code=None)
    assert "Sınır dışı erişim" in text
    assert "for (int i" not in text


def test_rich_footer_marks_estimated_usage_and_cost() -> None:
    """Faz 25 (§13): tahmini token ve maliyet alt satırda işaretlenir."""
    plain = _rich(_report())
    assert "15 token (giriş 10 · çıkış 5)" in plain
    assert "tahmini" not in plain
    assert "~$" not in plain
    report = _report()
    report.meta.usage_estimated = True
    report.meta.cost_est = 0.00123
    text = _rich(report)
    assert "15 token (giriş 10 · çıkış 5) · tahmini" in text
    assert "~$0.0012" in text


def test_rich_footer_shows_stage_breakdown_and_zero_usage() -> None:
    """Faz K: aşama dağılımı ayrı satırda; token harcanmadıysa nedeni yazılır."""
    from codementor.models.report import TokenSplit

    report = _report()
    report.meta.stage_tokens = {
        "llm_a": TokenSplit(input=6, output=3),
        "llm_b": TokenSplit(input=4, output=2),
    }
    text = _rich(report)
    assert "Giriş/çıkış: Analiz 6/3 · Mentor soruları 4/2" in text
    cached = _report()
    cached.meta.tokens_in = cached.meta.tokens_out = 0
    cached.meta.cache_hit = True
    assert "token 0 (önbellekten)" in _rich(cached)


def _with_suggestion() -> AnalysisReport:
    """Faz 36: bir hata (yüksek) + bir öneri (düşük)."""
    report = _report()
    suggestion = _finding("F-002", None, FindingSource.LLM, Severity.LOW).model_copy(
        update={"kind": "suggestion", "line_start": 2, "description": "Ara toplam adı öneri."}
    )
    report.findings = [report.findings[0], suggestion]
    return report


def test_markdown_splits_issues_and_suggestions() -> None:
    md = to_markdown(_with_suggestion())
    errors, rest = md.split("<details>")
    assert "## Hatalar" in errors
    assert "| F-001 | 3 |" in errors
    assert "Ara toplam" not in errors
    assert "<summary>Öneriler (1)</summary>" in rest
    assert "| F-002 | 2 |" in rest
    assert "## Bulgular" not in md


def test_markdown_only_suggestions_says_no_errors() -> None:
    report = _with_suggestion()
    report.findings = report.findings[1:]
    md = to_markdown(report)
    assert "Hata bulunmadı." in md
    assert "<summary>Öneriler (1)</summary>" in md


def test_sarif_suggestion_level_note() -> None:
    report = _with_suggestion()
    report.findings[0] = report.findings[0].model_copy(update={"severity": Severity.MEDIUM})
    report.findings[1] = report.findings[1].model_copy(update={"severity": Severity.LOW})
    log = to_sarif(report, "a.c")
    Draft4Validator(SCHEMA).validate(log)
    results = log["runs"][0]["results"]
    assert [r["level"] for r in results] == ["warning", "note"]
    assert [r["properties"]["kind"] for r in results] == ["issue", "suggestion"]


def test_cli_render_suggestions() -> None:
    text = _rich(_with_suggestion())
    assert "Öneriler (1)" in text
    assert text.index("F-001") < text.index("Öneriler (1)") < text.index("Ara toplam adı öneri.")
