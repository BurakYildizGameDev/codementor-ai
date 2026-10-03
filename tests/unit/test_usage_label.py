"""Faz 33: CLI, masaüstü ve web'de ortak token/maliyet etiketi."""

from __future__ import annotations

from codementor.models.report import ReportMeta
from codementor.report.usage import usage_label


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
    assert usage_label(_meta()) == "token 1200/340"


def test_estimated_usage_and_cost() -> None:
    label = usage_label(_meta(usage_estimated=True, cost_est=0.01234))
    assert label == "token 1200/340 (tahmini) · ~$0.0123"


def test_no_llm_tokens_gives_none() -> None:
    assert usage_label(_meta(tokens_in=0, tokens_out=0)) is None


def test_cache_hit_spent_nothing() -> None:
    assert usage_label(_meta(tokens_in=0, tokens_out=0, cache_hit=True)) is None
