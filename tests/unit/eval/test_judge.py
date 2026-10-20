"""LLM-as-judge ile Sokratik kalite değerlendirme testleri (Faz I / İş 10)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from typer.testing import CliRunner

from codementor.cli.main import app
from codementor.eval.judge import (
    evaluate_socratic_quality,
    judge_run_result,
    judge_summary_markdown,
    render_judge_prompt,
)
from codementor.models.enums import AuditCategory, Engine, Language
from codementor.models.eval import (
    Label,
    Metrics,
    RunConfig,
    RunResult,
    Sample,
    SampleResult,
    SocraticCriterionScore,
    SocraticJudgeReport,
)
from codementor.providers.fake import FakeProvider, FakeReply
from tests.unit.eval.helpers import report as make_report

SAMPLE_REPORT_JSON = json.dumps(
    {
        "pedagogical_value": {
            "score": 5,
            "rationale": "Öğrenciyi kendi hatasını bulmaya yönlendiriyor.",
        },
        "code_relevance": {
            "score": 4,
            "rationale": "Fonksiyon ve değişken isimlerine doğrudan değiniyor.",
        },
        "socratic_depth": {
            "score": 4,
            "rationale": "Düşündürücü Sokratik sorular içeriyor.",
        },
        "leakage_free": True,
        "overall_score": 4.3,
        "summary": "Oldukça başarılı bir Sokratik rehberlik.",
    }
)


def _sample(sample_id: str = "c-001") -> Sample:
    from codementor.models.enums import CompilationStatus
    from codementor.models.eval import Expected, ExpectedFinding

    label = Label(
        id=sample_id,
        language=Language.C,
        engine=Engine.NONE,
        syntax_valid=True,
        expected=Expected(
            compilation_status=CompilationStatus.PASSED,
            findings=[ExpectedFinding(category=AuditCategory.PERFORMANCE, line=1)],
        ),
        reviewed=True,
    )
    return Sample(
        label=label,
        code="int sum(int n) { return 0; }",
        path=f"eval/dataset/dev/{sample_id}",
    )


def _run_result(sample_id: str = "c-001") -> RunResult:
    analysis_rep = make_report(
        questions=["Döngü n elemanını nasıl toplar?", "Dönüş değeri ne olmalıdır?"],
        hint="Küçük bir n değeri için fonksiyonu elle yürütün.",
    )
    sample_res = SampleResult(id=sample_id, report=analysis_rep, latency_ms=120)
    config = RunConfig(
        split="dev",
        provider=None,
        model=None,
        mode="static",
        static_only=True,
        prompt_version="v1",
        rules_version="r3",
        schema_version="1.0.0",
        started_at=datetime.now(UTC),
        sample_ids=[sample_id],
    )
    return RunResult(config=config, metrics=Metrics(samples=1), samples=[sample_res])


def test_render_judge_prompt() -> None:
    text = render_judge_prompt(
        code="int x = 0;",
        language="c",
        flaw_concept="Değişken başlatma",
        questions=["x hangi değeri almalıdır?"],
        next_step_hint="x'i yazdırın.",
    )
    assert "int x = 0;" in text
    assert "Değişken başlatma" in text
    assert "x hangi değeri almalıdır?" in text
    assert "x'i yazdırın." in text
    assert "pedagogical_value" in text


@pytest.mark.anyio
async def test_evaluate_socratic_quality() -> None:
    provider = FakeProvider(script=[FakeReply(raw=SAMPLE_REPORT_JSON)])
    report = await evaluate_socratic_quality(
        provider=provider,
        code="int x = 0;",
        language="c",
        flaw_concept="Başlatma",
        questions=["x nedir?"],
        next_step_hint="x'e bakın.",
    )
    assert isinstance(report, SocraticJudgeReport)
    assert report.pedagogical_value.score == 5
    assert report.code_relevance.score == 4
    assert report.leakage_free is True
    assert report.overall_score == 4.3
    assert len(provider.calls) == 1


@pytest.mark.anyio
async def test_evaluate_socratic_quality_markdown_stripping() -> None:
    markdown_wrapped = f"```json\n{SAMPLE_REPORT_JSON}\n```"
    provider = FakeProvider(script=[FakeReply(raw=markdown_wrapped)])
    report = await evaluate_socratic_quality(
        provider=provider,
        code="int x = 0;",
        language="c",
        flaw_concept="Başlatma",
        questions=["x nedir?"],
        next_step_hint="x'e bakın.",
    )
    assert report.overall_score == 4.3


@pytest.mark.anyio
async def test_judge_run_result() -> None:
    run = _run_result("c-001")
    samples = {"c-001": _sample("c-001")}
    provider = FakeProvider(script=[FakeReply(raw=SAMPLE_REPORT_JSON)])
    reports = await judge_run_result(run, samples, provider)
    assert "c-001" in reports
    assert reports["c-001"].pedagogical_value.score == 5


def test_judge_summary_markdown() -> None:
    report = SocraticJudgeReport(
        pedagogical_value=SocraticCriterionScore(score=5, rationale="iyi"),
        code_relevance=SocraticCriterionScore(score=4, rationale="orta"),
        socratic_depth=SocraticCriterionScore(score=5, rationale="derin"),
        leakage_free=True,
        overall_score=4.7,
        summary="Harika yönlendirme.",
    )
    text = judge_summary_markdown({"c-001": report})
    assert "| c-001 | 5 | 4 | 5 | ✓ | 4.7 | Harika yönlendirme. |" in text
    assert "Ortalama Sokratik Kalite Puanı: **4.70 / 5.0** (1 örnek)" in text


def test_judge_summary_markdown_empty() -> None:
    assert judge_summary_markdown({}) == "Değerlendirilen örnek bulunamadı.\n"


def test_cli_eval_judge(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Sahte sağlayıcıyı varsayılan factory'ye bağlayalım
    from codementor.eval import runner

    monkeypatch.setattr(
        runner,
        "_default_factory",
        lambda _settings: lambda _name: FakeProvider(script=[FakeReply(raw=SAMPLE_REPORT_JSON)]),
    )

    dataset = tmp_path / "dataset"
    sample_dir = dataset / "dev" / "c-001"
    sample_dir.mkdir(parents=True)
    (sample_dir / "code.c").write_text("int sum(int n) { return 0; }", encoding="utf-8")
    (sample_dir / "label.yaml").write_text(
        "id: c-001\nlanguage: c\nengine: none\nsyntax_valid: true\n"
        "expected:\n  compilation_status: passed\n",
        encoding="utf-8",
    )
    run_file = tmp_path / "result.json"
    run_file.write_text(_run_result("c-001").model_dump_json(), encoding="utf-8")

    out_file = tmp_path / "judge_out.md"
    result = CliRunner().invoke(
        app,
        ["eval", "judge", str(run_file), "--dataset", str(dataset), "--out", str(out_file)],
    )
    assert result.exit_code == 0, result.output
    assert "| c-001 | 5 | 4 |" in result.output
    assert out_file.exists()
    assert "Ortalama Sokratik Kalite Puanı" in out_file.read_text(encoding="utf-8")
