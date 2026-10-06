"""Faz 26: ağır senkron aşamalar (Tier 0, statik olgu/kural) olay döngüsünü kilitlemez."""

from __future__ import annotations

import asyncio
import threading
import time
from typing import Any

import pytest

from codementor.config import Settings
from codementor.models.request import AnalysisRequest
from codementor.pipeline import orchestrator as orchestrator_module
from codementor.pipeline import stages
from codementor.pipeline.events import EventBus
from codementor.pipeline.orchestrator import Orchestrator
from codementor.providers.fake import FakeProvider
from tests.integration.conftest import LINKED_LIST

pytestmark = pytest.mark.anyio

SLOW_S = 0.3


async def test_heavy_stages_run_off_event_loop(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    loop_thread = threading.get_ident()
    seen: dict[str, int] = {}
    real_tier0, real_static = orchestrator_module.check_syntax, stages.run_static

    def slow_tier0(*args: Any, **kwargs: Any) -> Any:
        seen["tier0"] = threading.get_ident()
        time.sleep(SLOW_S)
        return real_tier0(*args, **kwargs)

    def slow_static(*args: Any, **kwargs: Any) -> Any:
        seen["static"] = threading.get_ident()
        time.sleep(SLOW_S)
        return real_static(*args, **kwargs)

    monkeypatch.setattr(orchestrator_module, "check_syntax", slow_tier0)
    monkeypatch.setattr(stages, "run_static", slow_static)
    events: list[str] = []
    bus = EventBus()
    bus.subscribe(lambda event: events.append(f"{event.stage}:{event.status}"))
    orchestrator = Orchestrator(
        settings, None, provider_factory=lambda _name: FakeProvider(script=[]), bus=bus
    )

    ticks = 0

    async def ticker() -> None:
        nonlocal ticks
        while True:
            await asyncio.sleep(0.01)
            ticks += 1

    ticking = asyncio.create_task(ticker())
    request = AnalysisRequest(code=LINKED_LIST, language="c")  # type: ignore[arg-type]
    report = await orchestrator.analyze(request)
    ticking.cancel()

    assert report.findings is not None
    assert seen["tier0"] != loop_thread
    assert seen["static"] != loop_thread
    # 2 × 0,3 sn boyunca döngü serbest kaldı (kilitlenseydi ~0 tık olurdu)
    assert ticks >= 20
    assert "tier0:completed" in events
    assert "rules:completed" in events
