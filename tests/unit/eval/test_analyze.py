"""`eval analyze`: precision analizi (Faz 22)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from typer.testing import CliRunner

from codementor.cli.main import app
from codementor.eval.analysis import analysis_markdown, analyze
from codementor.eval.metrics import audit_metrics, match_findings
from codementor.models.enums import AuditCategory, FindingSource, Severity
from codementor.models.eval import ExpectedFinding, Label, RunConfig, RunResult, SampleResult
from codementor.models.findings import Finding
from codementor.models.verification import FindingCheck
from tests.unit.eval.helpers import MEM, PERF, finding, label, report, result

DESIGN = AuditCategory.DESIGN


def _f(
    category: AuditCategory,
    line: int,
    fid: str,
    severity: Severity = Severity.MEDIUM,
    description: str = "d",
) -> Finding:
    return finding(category, line, fid).model_copy(
        update={"severity": severity, "description": description}
    )


def _run(samples: list[SampleResult]) -> RunResult:
    return RunResult.model_validate(
        {
            "config": RunConfig(
                split="dev",
                provider="fake",
                model="m",
                mode="two_pass",
                static_only=False,
                prompt_version="v1",
                rules_version="r1",
                schema_version="1.0",
                started_at=datetime(2026, 10, 2, tzinfo=UTC),
                sample_ids=[s.id for s in samples],
            ),
            "metrics": {"samples": len(samples)},
            "samples": samples,
        }
    )


def _labels(*items: Label) -> dict[str, Label]:
    return {lb.id: lb for lb in items}


def test_line_only_match_ignores_category() -> None:
    expected = [ExpectedFinding(category=MEM, line=4)]
    predicted = [finding(PERF, 5)]
    assert match_findings(expected, predicted) == []
    assert len(match_findings(expected, predicted, ignore_category=True)) == 1


def test_line_only_match_respects_distance() -> None:
    expected = [ExpectedFinding(category=MEM, line=4)]
    assert match_findings(expected, [finding(PERF, 7)], ignore_category=True) == []


def test_audit_metrics_ignore_category() -> None:
    pairs = [(label(findings=[(MEM, 4)]), result(report(findings=[finding(PERF, 4)])))]
    assert audit_metrics(pairs).precision == 0.0
    assert audit_metrics(pairs, ignore_category=True).precision == 1.0


def test_severity_filter_excludes_low() -> None:
    lb = label(findings=[(MEM, 4)])
    rep = report(findings=[_f(MEM, 4, "F-001"), _f(DESIGN, 20, "F-002", Severity.LOW)])
    analysis = analyze(_run([result(rep)]), _labels(lb))
    assert analysis.strict.precision == 0.5
    assert analysis.without_low.precision == 1.0
    assert analysis.without_low.recall == 1.0


def test_confusion_counts_wrong_category_same_line() -> None:
    lb = label(findings=[(MEM, 4), (PERF, 10)])
    rep = report(findings=[_f(DESIGN, 5, "F-001"), _f(PERF, 10, "F-002")])
    analysis = analyze(_run([result(rep)]), _labels(lb))
    assert analysis.confusion == {(MEM, DESIGN): 1}
    assert analysis.strict.f1 == 0.5
    assert analysis.line_only.precision == 1.0
    (fp,) = analysis.false_positives
    assert fp.category is DESIGN
    assert fp.confused_with is MEM


def test_fp_fn_lists_per_sample() -> None:
    first = label("c-001", findings=[(MEM, 4)])
    second = label("c-002", findings=[(PERF, 3)])
    samples = [
        result(report(findings=[_f(MEM, 4, "F-001")]), sample_id="c-001"),
        result(
            report(findings=[_f(DESIGN, 30, "F-001", Severity.LOW, "Ad | daha | iyi\nolabilir")]),
            sample_id="c-002",
        ),
    ]
    analysis = analyze(_run(samples), _labels(first, second))
    (fp,) = analysis.false_positives
    assert (fp.sample_id, fp.line, fp.category, fp.severity) == ("c-002", 30, DESIGN, Severity.LOW)
    assert fp.source is FindingSource.LLM
    assert fp.confused_with is None
    (fn,) = analysis.false_negatives
    assert (fn.sample_id, fn.line, fn.category) == ("c-002", 3, PERF)
    assert fn.severity is None
    assert analysis.fp_by("category") == {"design": 1}
    assert analysis.fp_by("severity") == {"low": 1}
    assert analysis.fp_by("source") == {"llm": 1}


def test_missing_report_counts_all_expected_as_fn() -> None:
    lb = label(findings=[(MEM, 4), (PERF, 9)])
    analysis = analyze(_run([result(None, error="boom")]), _labels(lb))
    assert len(analysis.false_negatives) == 2
    assert analysis.strict.recall == 0.0
    assert analysis.strict.precision is None


def test_unknown_sample_reported_as_missing() -> None:
    analysis = analyze(_run([result(report(), sample_id="c-404")]), {})
    assert analysis.missing == ["c-404"]
    assert analysis.false_positives == []


def test_markdown_contains_sections() -> None:
    lb = label(findings=[(MEM, 4)])
    rep = report(findings=[_f(DESIGN, 4, "F-001"), _f(PERF, 20, "F-002", description="a | b\nc")])
    text = analysis_markdown(analyze(_run([result(rep)]), _labels(lb)))
    for heading in (
        "## Özet",
        "## Yanlış pozitif dağılımı",
        "## Kategori karışıklığı",
        "## Yanlış pozitifler",
        "## Yanlış negatifler",
    ):
        assert heading in text
    assert "| Katı |" in text
    assert "| memory_safety → design | 1 |" in text
    assert "a \\| b c" in text  # tablo hücresi bozulmaz


def test_eval_analyze_cli_writes_markdown(tmp_path: Path) -> None:
    dataset = tmp_path / "dataset"
    sample = dataset / "dev" / "c-001"
    sample.mkdir(parents=True)
    (sample / "code.c").write_text("int main(void) {\n    return 0;\n}\n", encoding="utf-8")
    (sample / "label.yaml").write_text(
        "id: c-001\nlanguage: c\nengine: none\nsyntax_valid: true\n"
        "expected:\n  compilation_status: passed\n",
        encoding="utf-8",
    )
    path = tmp_path / "r.json"
    run = _run([result(report(findings=[_f(PERF, 2, "F-001")]), sample_id="c-001")])
    path.write_text(run.model_dump_json(), encoding="utf-8")
    out_file = tmp_path / "a.md"
    out = CliRunner().invoke(
        app,
        ["eval", "analyze", str(path), "--dataset", str(dataset), "--out", str(out_file)],
    )
    assert out.exit_code == 0, out.output
    assert "## Yanlış pozitifler" in out.output
    assert "| c-001 | 2 | performance |" in out_file.read_text(encoding="utf-8")


def test_eval_analyze_cli_bad_file(tmp_path: Path) -> None:
    out = CliRunner().invoke(app, ["eval", "analyze", str(tmp_path / "yok.json")])
    assert out.exit_code == 3


def test_confidence_threshold_table() -> None:
    """Faz 35: eşik altındaki LLM bulguları atılınca precision/recall; statik hep kalır."""
    lb = label(findings=[(MEM, 4), (PERF, 10)])
    sure = _f(MEM, 4, "F-001").model_copy(update={"confidence": 0.85})
    unsure = _f(DESIGN, 20, "F-002").model_copy(update={"confidence": 0.5})
    static = _f(PERF, 10, "F-003").model_copy(
        update={"confidence": 0.4, "source": FindingSource.STATIC}
    )
    analysis = analyze(_run([result(report(findings=[sure, unsure, static]))]), _labels(lb))
    table = {row.threshold: row for row in analysis.thresholds}
    assert sorted(table) == [0.5, 0.6, 0.7, 0.85]
    assert table[0.5].scores.precision == pytest.approx(2 / 3)
    assert table[0.5].kept == 3
    assert table[0.6].scores.precision == 1.0
    assert table[0.6].kept == 2
    assert table[0.85].scores.recall == 1.0
    assert "## Güven eşiği" in analysis_markdown(analysis)


def test_suggestions_excluded_from_fp_and_counted() -> None:
    """Faz 36: öneri yanlış pozitif listesine girmez, ayrı sayılır."""
    lb = label(findings=[(MEM, 4)])
    suggestion = _f(DESIGN, 20, "F-002").model_copy(update={"kind": "suggestion"})
    analysis = analyze(
        _run([result(report(findings=[_f(MEM, 4, "F-001"), suggestion]))]), _labels(lb)
    )
    assert analysis.false_positives == []
    assert analysis.predicted_total == 1
    assert analysis.suggestions_total == 1
    assert "öneri 1" in analysis_markdown(analysis)


# --- Faz 39: doğrulamanın attığı bulgular -------------------------------------------------------


def _check(line: int, category: AuditCategory, *, kept: bool = False) -> FindingCheck:
    return FindingCheck(
        finding_id=f"F-{line:03d}",
        line_start=line,
        category=category,
        kept=kept,
        basis="input" if kept else "unproven",
    )


def _dropping_run() -> tuple[RunResult, dict[str, Label]]:
    """c-001: 6. satırdaki gerçek hata düştü (FN), 9. satırdaki yanlış alarm düştü."""
    lb = label(findings=[(PERF, 6), (MEM, 3)])
    sample = result(report(findings=[finding(MEM, 3)])).model_copy(
        update={
            "finding_checks": [
                _check(3, MEM, kept=True),
                _check(6, PERF),
                _check(9, DESIGN),
            ]
        }
    )
    return _run([sample]), _labels(lb)


def test_match_findings_accepts_checks() -> None:
    expected = [ExpectedFinding(category=PERF, line=6)]
    pairs = match_findings(expected, [_check(7, PERF)])
    assert [(e.line, p.line_start) for e, p in pairs] == [(6, 7)]


def test_analyze_counts_dropped_true_and_false() -> None:
    run, labels = _dropping_run()
    analysis = analyze(run, labels)
    drops = analysis.verify_drops
    assert [(d.line, d.category, d.true_issue) for d in drops] == [
        (6, PERF, True),
        (9, DESIGN, False),
    ]
    assert all(d.basis == "unproven" for d in drops)


def test_analyze_without_checks_has_no_drops() -> None:
    """Faz 39 öncesi sonuç dosyaları: bölüm veri yok der."""
    lb = label(findings=[(MEM, 3)])
    analysis = analyze(_run([result(report(findings=[finding(MEM, 3)]))]), _labels(lb))
    assert analysis.verify_drops == []
    assert "kaydı yok" in analysis_markdown(analysis)


def test_analysis_markdown_has_verify_drop_section() -> None:
    run, labels = _dropping_run()
    text = analysis_markdown(analyze(run, labels))
    assert "## Doğrulamanın attığı bulgular" in text
    assert "gerçek hata 1" in text
    assert "yanlış alarm 1" in text


def test_two_drops_one_missed_issue_counts_once() -> None:
    """Aynı satırda iki düşürme, tek FN: yalnız biri gerçek hata; eşleşmiş beklenen sayılmaz."""
    lb = label(findings=[(PERF, 6), (MEM, 3)])
    sample = result(report(findings=[finding(MEM, 3)])).model_copy(
        update={"finding_checks": [_check(6, PERF), _check(6, PERF), _check(3, MEM)]}
    )
    drops = analyze(_run([sample]), _labels(lb)).verify_drops
    assert [d.true_issue for d in drops] == [True, False, False]
