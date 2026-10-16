"""Faz 33 / Faz K: CLI, masaüstü ve web'de ortak token/maliyet etiketleri."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.models.report import ReportMeta, TokenSplit
from codementor.models.usage import UsageTotals
from codementor.report import usage
from codementor.report.usage import (
    format_count,
    usage_breakdown,
    usage_breakdown_label,
    usage_label,
    usage_totals_label,
)
from codementor.storage import cache


def _meta(**kw: object) -> ReportMeta:
    base: dict[str, object] = {
        "provider": "fake",
        "model": "m",
        "prompt_version": "v1",
        "rules_version": "r1",
        "schema_version": "1.0",
        "tokens_in": 1200,
        "tokens_out": 340,
        "stage_latency_ms": {},
        "early_exit": False,
        "cache_hit": False,
        "degraded": False,
        "repair_attempts": 0,
        "warnings": [],
    }
    return ReportMeta.model_validate(base | kw)


def test_plain_usage() -> None:
    assert usage_label(_meta()) == "1.540 token (giriş 1.200 · çıkış 340)"


def test_estimated_usage_and_cost() -> None:
    label = usage_label(_meta(usage_estimated=True, cost_est=0.01234))
    assert label == "1.540 token (giriş 1.200 · çıkış 340) · tahmini · ~$0.0123"


@pytest.mark.parametrize(
    ("flags", "reason"),
    [
        ({}, "model çağrılmadı"),
        ({"cache_hit": True}, "önbellekten"),
        ({"early_exit": True}, "derleme hatası; model çağrılmadı"),
        ({"degraded": True}, "model yanıt vermedi"),
        ({"cache_hit": True, "degraded": True}, "önbellekten"),
    ],
)
def test_zero_tokens_always_visible_with_reason(flags: dict[str, bool], reason: str) -> None:
    """Faz K: token harcanmadıysa etiket gizlenmez, nedeni yazılır."""
    assert usage_label(_meta(tokens_in=0, tokens_out=0, **flags)) == f"token 0 ({reason})"


def test_breakdown_in_fixed_order_with_repairs() -> None:
    meta = _meta(
        repair_attempts=2,
        stage_tokens={
            "llm_b": TokenSplit(input=300, output=100),
            "llm_v": TokenSplit(input=0, output=0),
            "llm_a": TokenSplit(input=900, output=240),
        },
    )
    assert usage_breakdown(meta) == ["Analiz 900/240", "Mentor soruları 300/100", "2 onarım"]
    assert usage_breakdown_label(meta) == (
        "Giriş/çıkış: Analiz 900/240 · Mentor soruları 300/100 · 2 onarım"
    )


def test_breakdown_empty_without_llm() -> None:
    assert usage_breakdown_label(_meta(tokens_in=0, tokens_out=0)) is None


def test_totals_label() -> None:
    totals = UsageTotals(analyses=12, tokens_in=15000, tokens_out=3400, cost=0.0812)
    assert usage_totals_label(totals) == (
        "Toplam: 12 analiz · 18.400 token (giriş 15.000 · çıkış 3.400) · ~$0.0812"
    )
    no_price = UsageTotals(analyses=0, tokens_in=0, tokens_out=0, cost=None)
    assert usage_totals_label(no_price) == "Toplam: 0 analiz · 0 token (giriş 0 · çıkış 0)"


@pytest.mark.parametrize(
    ("value", "text"), [(0, "0"), (999, "999"), (1000, "1.000"), (1234567, "1.234.567")]
)
def test_format_count(value: int, text: str) -> None:
    assert format_count(value) == text


# --- Faz G6: `UsageTotals` `models/` katmanında; rapor katmanı depoyu bilmiyor --------------------


def test_usage_totals_defined_in_models_layer() -> None:
    """Tek tanım yeri `models.usage`; `storage.cache` ve `report.usage` onu oradan dışa aktarır."""
    assert UsageTotals.__module__ == "codementor.models.usage"
    assert cache.UsageTotals is UsageTotals
    assert usage.UsageTotals is UsageTotals


def test_report_layer_does_not_import_storage() -> None:
    """Kabul ölçütü (G6): `rg -n "from codementor.storage" src/codementor/report` boş kalmalı."""
    report_dir = Path(usage.__file__).parent
    offenders = sorted(
        path.name
        for path in report_dir.rglob("*.py")
        if "codementor.storage" in path.read_text(encoding="utf-8")
    )
    assert offenders == []
