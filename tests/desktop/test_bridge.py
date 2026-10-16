"""Arka plan köprüsü: FakeProvider'lı gerçek orkestratör, mesaj sırası, hata ve iptal."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from typing import Any

import pytest

from codementor.api.state import ApiState
from codementor.desktop.bridge import (
    AnalysisCancelledError,
    Bridge,
    Cancellation,
    Emit,
    Message,
    analysis_work,
    user_message,
)
from codementor.desktop.services import render_export
from codementor.models.pipeline import StageEvent
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest
from codementor.pipeline.run_state import PipelineError
from codementor.storage import sessions
from codementor.storage.cache import list_analyses
from tests.desktop.conftest import StallingProvider
from tests.integration.conftest import BROKEN_C, LINKED_LIST


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
    messages = run(bridge, "analyze")
    assert messages, "analiz 30 sn içinde bitmedi"
    report = messages[-1].payload
    assert isinstance(report, AnalysisReport), report
    assert render_export(report, "md").startswith("#")
    assert '"version": "2.1.0"' in render_export(report, "sarif")
    assert AnalysisReport.model_validate_json(render_export(report, "json")) == report


# --- İptal (Faz 19) ------------------------------------------------------------------------


def test_cancel_invokes_cancellation() -> None:
    calls: list[str] = []
    cancellation = Cancellation()
    cancellation.on_cancel(lambda: calls.append("iptal"))
    bridge = Bridge()
    bridge.submit("t", lambda _emit: cancellation.event.wait(5), cancellation=cancellation)
    bridge.cancel("t")
    bridge.join("t", 5)
    assert calls == ["iptal"]
    assert cancellation.cancelled
    assert bridge.drain() == []
    # iptalden sonra eklenen geri çağrı hemen çalışır (yarış: görev geç kaydolursa)
    cancellation.on_cancel(lambda: calls.append("geç"))
    assert calls == ["iptal", "geç"]


def test_analysis_work_cancel_stops_pipeline(
    stalled_core: ApiState, stalling: StallingProvider
) -> None:
    bridge = Bridge()
    cancellation = Cancellation()
    work = analysis_work(stalled_core, request(session_id="desktop-iptal"), cancellation)
    bridge.submit("analyze", work, cancellation=cancellation)
    assert stalling.started.wait(10), "LLM aşamasına gelinmedi"
    start = time.perf_counter()
    bridge.cancel("analyze")
    bridge.join("analyze", 10)
    assert not bridge.is_running("analyze")
    assert time.perf_counter() - start < 3
    assert stalling.cancelled.is_set()
    assert bridge.drain() == []  # geç mesajlar atılır
    assert list_analyses(stalled_core.database()) == []  # yarıda kalan analiz yazılmaz
    # ipucu merdiveni ilerlemez: bir sonraki gönderim yine ilk deneme
    assert sessions.next_attempt(stalled_core.database(), "desktop-iptal", None) == 1


def test_analysis_cancelled_outside_bridge_is_quiet(
    stalled_core: ApiState, stalling: StallingProvider
) -> None:
    cancellation = Cancellation()
    work = analysis_work(stalled_core, request(), cancellation)
    threading.Thread(target=lambda: (stalling.started.wait(10), cancellation.cancel())).start()
    with pytest.raises(AnalysisCancelledError):
        work(lambda _payload: None)


def test_cancel_all_cancels_running(stalled_core: ApiState, stalling: StallingProvider) -> None:
    bridge = Bridge()
    cancellation = Cancellation()
    bridge.submit(
        "analyze", analysis_work(stalled_core, request(), cancellation), cancellation=cancellation
    )
    assert stalling.started.wait(10)
    bridge.cancel_all()
    bridge.join("analyze", 10)
    assert stalling.cancelled.is_set()


def test_cancel_after_finish_is_harmless(core: ApiState) -> None:
    """Analiz bittikten sonra (ör. pencere kapanışında) gelen iptal ana thread'i bozmaz."""
    bridge = Bridge()
    cancellation = Cancellation()
    bridge.submit(
        "analyze", analysis_work(core, request(), cancellation), cancellation=cancellation
    )
    assert run(bridge, "analyze")[-1].kind == "result"
    bridge.cancel_all()  # biten işin iptal kaydı temizlendi: hiçbir şey yapmaz
    assert not cancellation.cancelled
    cancellation.cancel()  # kapanmış event loop'a çağrı RuntimeError fırlatmamalı
    assert cancellation.cancelled


def test_cancel_on_synchronous_path_not_persisted(core: ApiState) -> None:
    """Denetim O1: LLM'siz yol (sözdizimi hatası → erken çıkış) `await` içermez; iptal yine de
    kayıttan önce yakalanmalı (analiz yazılmaz, ipucu merdiveni ilerlemez)."""
    cancellation = Cancellation()
    cancellation.cancel()  # Durdur, analiz eşzamanlı aşamalardayken basıldı
    work = analysis_work(core, request(BROKEN_C, session_id="desktop-esz"), cancellation)
    with pytest.raises(AnalysisCancelledError):
        work(lambda _payload: None)
    assert list_analyses(core.database()) == []
    assert sessions.next_attempt(core.database(), "desktop-esz", None) == 1


def test_cancelled_task_not_logged_as_error(
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    """Denetim O4: iptal beklenen bir son; ERROR log'u ve 'beklenmeyen hata' metni üretmez."""
    assert user_message(AnalysisCancelledError("Analiz durduruldu.")) == "Analiz durduruldu."
    assert captured_logs() == []
    # karşılaştırma: beklenmeyen hata gerçekten log'a düşer (fikstür log'u görüyor)
    user_message(RuntimeError("x"))
    assert [e["event"] for e in captured_logs()] == ["desktop_task_failed"]


def test_resubmit_cancels_previous_cancellation() -> None:
    first, second = Cancellation(), Cancellation()
    bridge = Bridge()
    bridge.submit("t", lambda _emit: first.event.wait(5), cancellation=first)
    bridge.submit("t", lambda _emit: "yeni", cancellation=second)
    assert first.cancelled  # eski iş durdurulamaz hale gelmez
    assert not second.cancelled
    bridge.join("t", 5)
    assert [m.payload for m in bridge.drain()] == ["yeni"]
