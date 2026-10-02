"""§14.2 metrikleri: bilinen girdi → elle hesaplanmış bilinen skor."""

from __future__ import annotations

import pytest

from codementor.eval.metrics import (
    audit_metrics,
    complexity_metrics,
    compute_metrics,
    cost_estimate,
    early_exit_metrics,
    guard_interventions,
    injection_resistance,
    leak_rate,
    match_findings,
    percentile,
    ratio,
    same_growth_class,
    schema_metrics,
)
from codementor.models.eval import ExpectedFinding, Metrics, ModelPrice, PricingFile
from codementor.models.report import AnalysisReport
from codementor.pipeline.stages import SCRUB_WARNING_COMPLEXITY, SCRUB_WARNING_FINDINGS
from tests.unit.eval.helpers import MEM, PERF, finding, label, report, result


def test_ratio_and_percentile() -> None:
    assert ratio(1, 4) == 0.25
    assert ratio(3, 0) is None
    values = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]
    assert percentile(values, 50) == 500.0  # nearest-rank: ceil(0.5·10) = 5. değer
    assert percentile(values, 95) == 1000.0  # ceil(9.5) = 10. değer
    assert percentile([], 50) is None


def test_match_same_category_within_two_lines_one_to_one() -> None:
    expected = [ExpectedFinding(category=MEM, line=10), ExpectedFinding(category=MEM, line=12)]
    predicted = [finding(MEM, 11), finding(MEM, 15), finding(PERF, 10)]
    pairs = match_findings(expected, predicted)
    assert [(e.line, p.line_start) for e, p in pairs] == [(10, 11)]  # 12↔11 alındı, 15 uzak


def test_match_prefers_closest_lines() -> None:
    expected = [ExpectedFinding(category=MEM, line=10), ExpectedFinding(category=MEM, line=12)]
    predicted = [finding(MEM, 12), finding(MEM, 10)]
    pairs = match_findings(expected, predicted)
    assert sorted((e.line, p.line_start) for e, p in pairs) == [(10, 10), (12, 12)]


def test_audit_precision_recall_f1_line_accuracy() -> None:
    # örnek 1: beklenen {MEM@10, PERF@20}, tahmin {MEM@11, MEM@30} → TP 1
    # örnek 2: beklenen {MEM@5}, tahmin {MEM@5} → TP 1 (satır birebir)
    pairs = [
        (
            label(findings=[(MEM, 10), (PERF, 20)]),
            result(report(findings=[finding(MEM, 11), finding(MEM, 30)])),
        ),
        (label("c-002", findings=[(MEM, 5)]), result(report(findings=[finding(MEM, 5)]))),
    ]
    scores = audit_metrics(pairs)
    assert scores.precision == pytest.approx(2 / 3)  # TP 2 / tahmin 3
    assert scores.recall == pytest.approx(2 / 3)  # TP 2 / beklenen 3
    assert scores.f1 == pytest.approx(2 / 3)
    assert scores.line_accuracy == pytest.approx(1 / 2)  # 11≠10, 5=5


def test_audit_missing_report_counts_expected_only() -> None:
    scores = audit_metrics([(label(findings=[(MEM, 1)]), result(None, error="x"))])
    assert scores.recall == 0.0
    assert scores.precision is None


def test_early_exit_precision_recall() -> None:
    pairs = [
        (label("c-001", syntax_valid=False), result(report(early_exit=True))),  # TP
        (label("c-002", syntax_valid=False), result(report())),  # FN
        (label("c-003"), result(report(early_exit=True))),  # FP
        (label("c-004"), result(report())),  # TN
    ]
    assert early_exit_metrics(pairs) == (0.5, 0.5)


def test_complexity_exact_and_class() -> None:
    pairs = [
        (label("c-001", time="n^2"), result(report(time="n^2"))),  # birebir + sınıf
        (label("c-002", time="n^2"), result(report(time="m*n"))),  # yalnız sınıf
        (label("c-003", time="n"), result(report(time="n log n"))),  # ikisi de yanlış
        (label("c-004", time="n"), result(report())),  # karmaşıklık yok → yanlış
        (label("c-005"), result(report(time="1"))),  # etiketsiz → sayılmaz
    ]
    assert complexity_metrics(pairs) == (0.25, 0.5)


@pytest.mark.parametrize(
    ("a", "b", "same"),
    [
        ("n^2", "m*n", True),
        ("n log n", "m log m", True),
        ("e + v", "n", True),
        ("n", "n^2", False),
        ("2^n", "n^2", False),
        ("n", "bozuk(", False),
    ],
)
def test_same_growth_class(a: str, b: str, same: bool) -> None:
    assert same_growth_class(a, b) is same


def test_leak_rate_uses_must_not_contain_case_and_space_insensitive() -> None:
    pairs = [
        (
            label("c-001", must_not_contain=["HashSet<"]),
            result(report(questions=["bir hashset<int> kullan?"])),
        ),
        (
            label("c-002", must_not_contain=["free(cur)"]),
            result(report(questions=["Ne olur?"], hint="free(cur)  sonra")),
        ),
        (
            label("c-003", must_not_contain=["x"]),
            result(report(questions=["Temiz mi?"])),
        ),  # 'x' yok
        (label("c-004", must_not_contain=["y"]), result(report())),  # Sokratik yok → paydada değil
    ]
    assert leak_rate(pairs) == pytest.approx(2 / 3)


def test_injection_resistance() -> None:
    inj = ["injection"]
    pairs = [
        (label("c-001", tags=inj), result(report(questions=["Soru?"]))),  # direnç
        (
            label("c-002", tags=inj, must_not_contain=["çözüm"]),
            result(report(questions=["çözüm şu"])),
        ),  # sızdı
        (label("c-003", tags=inj), result(report(degraded=True))),  # şema düşmüş
        (
            label("c-004", syntax_valid=False, tags=inj),
            result(report(early_exit=True)),
        ),  # erken çıkış
        (label("c-005"), result(report(degraded=True))),  # injection değil → sayılmaz
    ]
    assert injection_resistance(pairs) == 0.5


def test_schema_metrics_only_where_pass_a_ran() -> None:
    pairs = [
        (label("c-001"), result(report(), first=True, final=True)),
        (label("c-002"), result(report(), first=False, final=True)),
        (label("c-003"), result(report(), first=False, final=False)),
        (label("c-004"), result(report(early_exit=True))),  # Geçiş A yok
    ]
    first, final = schema_metrics(pairs)
    assert first == pytest.approx(1 / 3)
    assert final == pytest.approx(2 / 3)


def test_cost_estimate() -> None:
    pricing = PricingFile(
        version=1,
        prices=[ModelPrice(provider="fake", model="m", input_per_mtok=2.0, output_per_mtok=10.0)],
    )
    results = [result(report(tokens=(1_000_000, 100_000))), result(report(tokens=(0, 0)))]
    assert cost_estimate(results, pricing) == pytest.approx(2.0 + 1.0)
    assert cost_estimate(results, None) is None
    unpriced = [result(report(tokens=(10, 10), provider="claude_cli", model="x"))]
    assert cost_estimate(unpriced, pricing) is None


def test_compute_metrics_aggregates() -> None:
    pairs = [
        (
            label("c-001", time="n"),
            result(report(time="n", tokens=(100, 50)), latency=1000, llm=True),
        ),
        (label("c-002", syntax_valid=False), result(report(early_exit=True), latency=10)),
        (label("c-003"), result(None, latency=5, error="Kod çok büyük")),
    ]
    metrics = compute_metrics(pairs)
    assert metrics.samples == 3
    assert metrics.errors == 1
    assert metrics.complexity_time_exact_acc == 1.0
    assert metrics.early_exit_recall == 1.0
    assert metrics.tokens_mean == 150.0  # yalnız LLM çağrılan örnek
    assert metrics.latency_p50_ms == 10.0
    assert metrics.latency_p95_ms == 1000.0


def _guarded(leak_check: str = "passed", warnings: list[str] | None = None) -> AnalysisReport:
    rep = report(questions=["Neden?"])
    assert rep.socratic is not None
    return rep.model_copy(
        update={
            "socratic": rep.socratic.model_copy(update={"leak_check": leak_check}),
            "meta": rep.meta.model_copy(update={"warnings": warnings or []}),
        }
    )


def test_guard_interventions_counts_regenerated_and_scrub_warnings() -> None:
    reports = [
        _guarded("regenerated"),
        _guarded("dropped_questions"),
        _guarded(warnings=[SCRUB_WARNING_COMPLEXITY]),
        _guarded("regenerated", [SCRUB_WARNING_FINDINGS]),  # örnek başına bir kez
    ]
    pairs = [(label(f"c-00{i}"), result(rep, llm=True)) for i, rep in enumerate(reports)]
    assert guard_interventions(pairs) == 4
    assert compute_metrics(pairs).guard_interventions == 4


def test_guard_interventions_ignores_passed_and_skipped() -> None:
    pairs = [
        (label("c-001"), result(_guarded("passed", ["başka uyarı"]), llm=True)),
        (label("c-002"), result(_guarded("skipped"), llm=True)),
        (label("c-003"), result(None, llm=True, error="x")),
    ]
    assert guard_interventions(pairs) == 0


def test_guard_interventions_none_without_llm() -> None:
    assert guard_interventions([(label(), result(report()))]) is None


def test_old_result_without_guard_field_loads() -> None:
    assert Metrics.model_validate({"samples": 3}).guard_interventions is None
