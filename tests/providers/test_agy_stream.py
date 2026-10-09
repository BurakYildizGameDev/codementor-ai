"""agy stream-json çıktısının ayrıştırılması (Faz 28, Faz 63).

Fixture, agy 1.3.1'in 2026-10-09'daki gerçek çıktısıdır (kimlikler ve yol maskelendi): agy
yanıttan sonra kendiliğinden ikinci bir tur açıp araç izi yazıyor.
"""

from __future__ import annotations

import json
from pathlib import Path

from codementor.providers.agy_stream import first_json_object, first_response_text, result_event

FIXTURE = Path(__file__).parent / "fixtures" / "agy_stream_result.ndjson"


def _fixture() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_fixture_result_has_trailing_tool_trace() -> None:
    result = result_event(_fixture())
    assert result is not None
    assert result["structured_output"] == {"ok": True}
    assert "toolAction" in result["response"]  # tek json.loads ile çözülemeyen metin


def test_first_json_object_skips_trailing_tool_trace() -> None:
    result = result_event(_fixture())
    assert result is not None
    assert first_json_object(result["response"]) == {"ok": True}


def test_first_json_object_accepts_fenced_and_leading_text() -> None:
    assert first_json_object('```json\n{"a": 1}\n```') == {"a": 1}
    assert first_json_object('İşte yanıt: {"a": 1} ve {"b": 2}') == {"a": 1}


def test_first_json_object_ignores_non_dict_and_garbage() -> None:
    assert first_json_object('[1, 2] {"a": 1}') == {"a": 1}
    assert first_json_object("{bozuk") is None
    assert first_json_object("") is None
    assert first_json_object("[1, 2]") is None


def test_first_json_object_survives_deep_nesting() -> None:
    assert first_json_object("[" * 100_000) is None


def test_text_deltas_of_first_agent_response_joined_in_order() -> None:
    # ikinci tur (adım 3: araç izi) kurtarılan metne karışmamalı
    assert first_response_text(_fixture()) == '{"ok": true}\n'


def test_first_response_text_without_deltas_is_empty() -> None:
    result = json.dumps({"event": "result", "result": {"status": "SUCCESS", "response": ""}})
    assert first_response_text("[agy] bilgi\n" + result) == ""
