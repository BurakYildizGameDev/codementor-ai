"""Kayıtlı eval sonucunun dil/motor grubuna göre dökümü (Faz 18)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from typer.testing import CliRunner

from codementor.cli.main import app
from codementor.eval.breakdown import breakdown, breakdown_table
from codementor.eval.metrics import compute_metrics
from codementor.models.enums import AuditCategory, Engine, Language
from codementor.models.eval import Label, RunConfig, RunResult, SampleResult
from tests.unit.eval.helpers import MEM, PERF, finding, label, report, result


def _labelled(
    sample_id: str,
    language: Language,
    engine: Engine = Engine.NONE,
    *,
    time: str | None = None,
    findings: list[tuple[AuditCategory, int]] | None = None,
) -> Label:
    base = label(sample_id, time=time, findings=findings)
    return base.model_copy(update={"language": language, "engine": engine})


LABELS = [
    _labelled("c-001", Language.C, findings=[(MEM, 4)]),
    _labelled("c-002", Language.C, findings=[(PERF, 7)]),
    _labelled("unity-001", Language.CSHARP, Engine.UNITY, findings=[(PERF, 3)]),
    _labelled("python-001", Language.PYTHON, time="n", findings=[(PERF, 2)]),
]
RESULTS = [
    result(report(findings=[finding(MEM, 4)]), sample_id="c-001"),
    result(report(findings=[]), sample_id="c-002"),
    result(report(findings=[finding(PERF, 3)]), sample_id="unity-001"),
    result(report(time="n", findings=[finding(PERF, 9)]), sample_id="python-001"),
]


def _run(samples: list[SampleResult]) -> RunResult:
    pairs = list(zip(LABELS, samples, strict=False))
    return RunResult(
        config=RunConfig(
            split="dev",
            provider=None,
            model=None,
            mode="static",
            static_only=True,
            prompt_version="v1",
            rules_version="r1",
            schema_version="1.0",
            started_at=datetime(2026, 10, 1, tzinfo=UTC),
            sample_ids=[s.id for s in samples],
        ),
        metrics=compute_metrics(pairs),
        samples=samples,
    )


def test_breakdown_per_language_matches_subset_metrics() -> None:
    groups, missing = breakdown(_run(RESULTS), {lb.id: lb for lb in LABELS})
    assert missing == []
    assert list(groups) == ["c", "unity", "python"]  # ilk görülme sırası
    assert groups["c"] == compute_metrics(list(zip(LABELS[:2], RESULTS[:2], strict=True)))
    assert groups["c"].audit_recall == 0.5
    assert groups["unity"].audit_f1 == 1.0
    assert groups["python"].complexity_time_exact_acc == 1.0
    assert groups["python"].audit_recall == 0.0  # 9. satır, beklenen 2 (fark > 2)


def test_breakdown_unknown_sample_id_reported() -> None:
    extra = result(report(), sample_id="css-009")
    groups, missing = breakdown(_run([*RESULTS, extra]), {lb.id: lb for lb in LABELS})
    assert missing == ["css-009"]
    assert sum(m.samples for m in groups.values()) == 4


def test_breakdown_table_has_group_rows() -> None:
    groups, _ = breakdown(_run(RESULTS), {lb.id: lb for lb in LABELS})
    table = breakdown_table(groups)
    assert table.splitlines()[0].startswith("| Grup | n |")
    assert "| python | 1 |" in table
    assert "| c | 2 |" in table


def test_eval_breakdown_cli(tmp_path: Path) -> None:
    dataset = tmp_path / "dataset"
    sample = dataset / "dev" / "c-001"
    sample.mkdir(parents=True)
    (sample / "code.c").write_text("int main(void) {\n    return 0;\n}\n", encoding="utf-8")
    (sample / "label.yaml").write_text(
        "id: c-001\nlanguage: c\nengine: none\nsyntax_valid: true\n"
        "expected:\n  compilation_status: passed\n",
        encoding="utf-8",
    )
    run = _run([result(report(), sample_id="c-001")])
    path = tmp_path / "r.json"
    path.write_text(run.model_dump_json(), encoding="utf-8")
    out = CliRunner().invoke(app, ["eval", "breakdown", str(path), "--dataset", str(dataset)])
    assert out.exit_code == 0, out.output
    assert "| c | 1 |" in out.output
    orphan = _run([result(report(), sample_id="c-001"), result(report(), sample_id="c-999")])
    path.write_text(orphan.model_dump_json(), encoding="utf-8")
    warned = CliRunner().invoke(app, ["eval", "breakdown", str(path), "--dataset", str(dataset)])
    assert warned.exit_code == 0
    assert "etiketi bulunamayan örnekler: c-999" in warned.output
