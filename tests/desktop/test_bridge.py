"""Arka plan köprüsü: FakeProvider'lı gerçek orkestratör, mesaj sırası, hata ve iptal."""

from __future__ import annotations

import threading

from codementor.api.state import ApiState
from codementor.desktop.bridge import Bridge, Emit, Message, analysis_work, user_message
from codementor.desktop.services import render_export
from codementor.models.pipeline import StageEvent
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest
from codementor.pipeline.orchestrator import PipelineError
from codementor.storage.cache import list_analyses
from tests.integration.conftest import LINKED_LIST


def run(bridge: Bridge, task: str) -> list[Message]:
    bridge.join(task, timeout=30)
    return bridge.drain()


def request(code: str = LINKED_LIST, **kwargs: object) -> AnalysisRequest:
    return AnalysisRequest(code=code, language="c", engine="none", **kwargs)  # type: ignore[arg-type]


def test_analysis_streams_events_then_result(core: ApiState) -> None:
    bridge = Bridge()
    bridge.submit("analyze", analysis_work(core, request()))
    messages = run(bridge, "analyze")

    assert [m.kind for m in messages[:-1]] == ["event"] * (len(messages) - 1)
    events = [m.payload for m in messages[:-1]]
    assert all(isinstance(e, StageEvent) for e in events)
    assert {e.stage for e in events if isinstance(e, StageEvent)} >= {"ingest", "llm_b", "report"}
    final = messages[-1]
    assert final.kind == "result"
    assert isinstance(final.payload, AnalysisReport)
    assert final.payload.socratic is not None
    assert [row.id for row in list_analyses(core.database())] == [final.payload.analysis_id]


def test_hint_level_rises_with_same_session(core: ApiState) -> None:
    levels = []
    for _ in range(2):
        bridge = Bridge()
        bridge.submit("analyze", analysis_work(core, request(session_id="desktop-test")))
        report = run(bridge, "analyze")[-1].payload
        assert isinstance(report, AnalysisReport)
        assert report.socratic is not None
        levels.append(report.socratic.hint_level)
    assert levels[1] == levels[0] + 1


def test_pipeline_error_becomes_turkish_message(core: ApiState) -> None:
    too_long = "int x;\n" * (core.settings.limits.max_lines + 5)
    bridge = Bridge()
    bridge.submit("analyze", analysis_work(core, request(too_long)))
    final = run(bridge, "analyze")[-1]
    assert final.kind == "error"
    assert "satır" in str(final.payload).lower()


def test_unexpected_error_hides_details() -> None:
    def boom(_emit: Emit) -> object:
        raise RuntimeError("iç ayrıntı")

    bridge = Bridge()
    bridge.submit("t", boom)
    (message,) = run(bridge, "t")
    assert message.kind == "error"
    assert "RuntimeError" in str(message.payload)
    assert "iç ayrıntı" not in str(message.payload)
    assert user_message(PipelineError("Kod çok büyük", "too_large")) == "Kod çok büyük"


def test_cancel_discards_late_messages() -> None:
    release = threading.Event()

    def slow(emit: Emit) -> str:
        emit("ilk")
        release.wait(5)
        return "geç sonuç"

    bridge = Bridge()
    bridge.submit("t", slow)
    bridge.cancel("t")
    release.set()
    assert run(bridge, "t") == []
    assert not bridge.is_running("t")


def test_resubmit_keeps_only_newest_generation() -> None:
    gate = threading.Event()

    def first(_emit: Emit) -> str:
        gate.wait(5)
        return "eski"

    bridge = Bridge()
    bridge.submit("t", first)
    old = bridge._threads["t"]
    bridge.submit("t", lambda _emit: "yeni")
    gate.set()
    old.join(5)
    messages = run(bridge, "t")
    assert [m.payload for m in messages] == ["yeni"]


def test_render_export_formats(core: ApiState) -> None:
    bridge = Bridge()
    bridge.submit("analyze", analysis_work(core, request()))
    report = run(bridge, "analyze")[-1].payload
    assert isinstance(report, AnalysisReport)
    assert render_export(report, "md").startswith("#")
    assert '"version": "2.1.0"' in render_export(report, "sarif")
    assert AnalysisReport.model_validate_json(render_export(report, "json")) == report
