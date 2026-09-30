"""SSE ilerleme akışı: olay sırası, son olay `report`, hata olayı, başlıklar, eşzamanlılık."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import pytest

from codementor.models.pipeline import ALL_STAGES
from tests.api.conftest import ClientFactory
from tests.integration.conftest import (
    BROKEN_C,
    LINKED_LIST,
    FakeFactory,
    analysis_reply,
    socratic_reply,
)

pytestmark = pytest.mark.anyio
BODY = {"code": LINKED_LIST, "question_id": "c-medium-linked-list"}


def parse_sse(text: str) -> list[tuple[str, dict[str, Any]]]:
    events = []
    for block in text.strip().split("\n\n"):
        lines = dict(line.split(": ", 1) for line in block.splitlines())
        events.append((lines["event"], json.loads(lines["data"])))
    return events


async def _stream(
    client: Any, body: dict[str, Any]
) -> tuple[Any, list[tuple[str, dict[str, Any]]]]:
    response = await client.post("/v1/analyze/stream", json=body)
    return response, parse_sse(response.text)


async def test_stage_events_in_order_then_report(
    client_for: ClientFactory, fake: FakeFactory
) -> None:
    response, events = await _stream(client_for(fake(analysis_reply(), socratic_reply())), BODY)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.headers["cache-control"] == "no-cache"
    assert response.headers["x-accel-buffering"] == "no"
    kinds = [kind for kind, _ in events]
    assert kinds[-1] == "report"  # kabul: son olay report
    assert set(kinds[:-1]) == {"stage"}
    completed = [d["stage"] for k, d in events if k == "stage" and d["status"] == "completed"]
    expected = [
        "ingest",
        "cache",
        "tier0",
        "tier1",
        "facts",
        "rules",
        "prompt_a",
        "llm_a",
        "verify_a",
        "prompt_b",
        "llm_b",
        "verify_b",
        "report",
    ]
    assert completed == expected  # kabul: doğru sıra
    seen_started: set[str] = set()
    for _kind, data in events[:-1]:
        if data["status"] == "started":
            seen_started.add(data["stage"])
        elif data["status"] == "completed":
            assert data["stage"] in seen_started, data["stage"]  # önce started, sonra completed
    report = events[-1][1]
    assert set(report["meta"]["stage_latency_ms"]) == set(ALL_STAGES)
    assert all(d["analysis_id"] == report["analysis_id"] for k, d in events if k == "stage")


async def test_early_exit_stream_has_no_llm_stages(
    client_for: ClientFactory, fake: FakeFactory
) -> None:
    provider = fake()
    _, events = await _stream(client_for(provider), {"code": BROKEN_C, "language": "c"})
    stages = {d["stage"]: d["status"] for k, d in events if k == "stage"}
    assert stages["llm_a"] == "skipped"
    assert stages["tier1"] == "skipped"
    assert events[-1][0] == "report"
    assert events[-1][1]["meta"]["early_exit"] is True
    assert provider.calls == []


async def test_error_event_is_problem(client_for: ClientFactory, fake: FakeFactory) -> None:
    response, events = await _stream(
        client_for(fake()), {"code": "int x;", "language": "c", "question_id": "yok"}
    )
    assert response.status_code == 200  # akış başladıktan sonra hata olay olarak gelir
    kind, problem = events[-1]
    assert kind == "error"
    assert problem["status"] == 404
    assert problem["instance"] == "/v1/analyze/stream"


async def test_invalid_body_rejected_before_stream(client_for: ClientFactory) -> None:
    response = await client_for().post("/v1/analyze/stream", json={"language": "c"})
    assert response.status_code == 422
    assert response.headers["content-type"] == "application/problem+json"


async def test_concurrent_streams_do_not_mix(client_for: ClientFactory, fake: FakeFactory) -> None:
    first = client_for(fake(analysis_reply(), socratic_reply()))
    second = client_for(fake())
    (_, a), (_, b) = await asyncio.gather(
        _stream(first, BODY), _stream(second, {"code": BROKEN_C, "language": "c"})
    )
    for events in (a, b):
        report_id = events[-1][1]["analysis_id"]
        assert {d["analysis_id"] for k, d in events if k == "stage"} == {report_id}
    assert a[-1][1]["analysis_id"] != b[-1][1]["analysis_id"]
