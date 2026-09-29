"""§6.5 örnek raporunun `AnalysisReport` ile doğrulanması."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from codementor.models.bigo import parse_bigo
from codementor.models.enums import Engine, FindingSource, Language
from codementor.models.report import AnalysisReport

EXAMPLE = Path(__file__).parent / "report_example.json"


@pytest.fixture
def raw() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    return data


def test_example_validates(raw: dict[str, Any]) -> None:
    report = AnalysisReport.model_validate(raw)
    assert report.language is Language.CSHARP
    assert report.engine is Engine.UNITY
    assert report.findings[0].source is FindingSource.CONFIRMED
    assert report.socratic is not None
    assert report.socratic.hint_level == 1
    assert report.meta.stage_latency_ms["llm_a"] == 9120


def test_example_roundtrip(raw: dict[str, Any]) -> None:
    report = AnalysisReport.model_validate(raw)
    assert report.model_dump(mode="json") == raw


def test_example_validates_from_json_text() -> None:
    AnalysisReport.model_validate_json(EXAMPLE.read_text(encoding="utf-8"))


def test_example_complexity_is_canonical(raw: dict[str, Any]) -> None:
    complexity = AnalysisReport.model_validate(raw).complexity
    assert complexity is not None
    parsed = parse_bigo(complexity.time_complexity)
    assert parsed.canonical == complexity.time_complexity
    assert parsed.display == complexity.display_time
    assert complexity.static_hint is not None
    assert parse_bigo(complexity.static_hint).same_class(parsed)
