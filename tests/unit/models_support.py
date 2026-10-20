"""`test_models.py` için ortak düzenek: sabitler, yardımcılar, fixture'lar."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel


def _fields(model: type[BaseModel]) -> set[str]:
    return set(model.model_fields)


# ---------------------------------------------------------------- LLM modelleri (§6.3)


def _llm_finding(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "category": "performance",
        "severity": "medium",
        "line_start": 3,
        "line_end": None,
        "evidence": "for (int i = 0; i < n; i++)",
        "description": "İç içe döngü.",
    }
    return base | kw


def _complexity(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "reasoning_steps": ["Dış döngü n kez döner."],
        "time_complexity": "O(n^2)",
        "space_complexity": "O(1)",
        "optimal_time_target": None,
        "agreement": "agrees",
    }
    return base | kw


# ---------------------------------------------------------------- rapor modelleri (§6.4)


def _finding(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "id": "F-001",
        "rule_id": None,
        "category": "memory_safety",
        "severity": "high",
        "line_start": 5,
        "line_end": 6,
        "evidence": "free(p);",
        "description": "Çift serbest bırakma.",
        "source": "static",
        "confidence": 1.0,
    }
    return base | kw


def _socratic(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "key_flaw_concept": "GC",
        "hint_level": 1,
        "guiding_questions": ["Neden?"],
        "next_step_hint": None,
        "leak_check": "passed",
    }
    return base | kw


def _meta() -> dict[str, Any]:
    return {
        "provider": None,
        "model": None,
        "prompt_version": "v1",
        "rules_version": "1.0.0",
        "schema_version": "1.0",
        "tokens_in": 0,
        "tokens_out": 0,
        "stage_latency_ms": {},
        "early_exit": True,
        "cache_hit": False,
        "degraded": False,
        "repair_attempts": 0,
        "warnings": [],
    }


def _report(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "analysis_id": "01J9ZK4M8Q3W6Y2T5R7N1B0C9D",
        "created_at": datetime(2026, 9, 29, tzinfo=UTC),
        "language": "c",
        "engine": "none",
        "question_id": None,
        "difficulty": None,
        "compilation": {"status": "failed", "diagnostics": []},
        "complexity": None,
        "findings": [],
        "socratic": None,
        "meta": _meta(),
    }
    return base | kw
