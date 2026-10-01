"""Analiz iptali Tier 1 derleyici sürecini de durdurur (Faz 24; Faz 19'un devamı)."""

from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

import pytest

from codementor.config import Settings
from codementor.models.request import AnalysisRequest
from codementor.models.validation import CompilerTool, Toolchain
from codementor.pipeline.orchestrator import Orchestrator
from codementor.providers.fake import FakeProvider
from codementor.validation.runner import ProcessLimits, ProcessResult
from tests.integration.conftest import LINKED_LIST

pytestmark = pytest.mark.anyio

GCC = Toolchain(c=CompilerTool(name="gcc", kind="gcc", command=["/usr/bin/gcc"]))


@dataclass
class BlockingRunner:
    """Derleyici gibi takılır; iptal olayı gelince `cancelled` sonucu döner."""

    started: threading.Event = field(default_factory=threading.Event)
    cancel_seen: threading.Event = field(default_factory=threading.Event)
    got_cancel: list[threading.Event | None] = field(default_factory=list)

    def __call__(
        self,
        argv: Sequence[str],
        stdin: str,
        limits: ProcessLimits,
        *,
        extra_env: Mapping[str, str] | None = None,
        cancel: threading.Event | None = None,
    ) -> ProcessResult:
        self.got_cancel.append(cancel)
        self.started.set()
        if cancel is not None and cancel.wait(10):
            self.cancel_seen.set()
            return ProcessResult(None, "", "", cancelled=True)
        return ProcessResult(0, "", "")


def _orchestrator(settings: Settings, runner: BlockingRunner) -> Orchestrator:
    enabled = settings.model_copy(
        update={"validation": settings.validation.model_copy(update={"tier1_enabled": True})}
    )
    return Orchestrator(
        enabled,
        None,
        provider_factory=lambda _name: FakeProvider(script=[]),
        toolchain=GCC,
        tier1_runner=runner,
    )


async def test_cancelled_analysis_kills_tier1(settings: Settings) -> None:
    runner = BlockingRunner()
    request = AnalysisRequest(code=LINKED_LIST, language="c")  # type: ignore[arg-type]
    task = asyncio.create_task(_orchestrator(settings, runner).analyze(request))
    assert await asyncio.to_thread(runner.started.wait, 10), "Tier 1'e gelinmedi"
    # Tier 1 olay döngüsünü kilitlemez: derleyici beklerken döngü başka işi yürütür
    await asyncio.sleep(0)
    start = time.perf_counter()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert await asyncio.to_thread(runner.cancel_seen.wait, 5)
    assert time.perf_counter() - start < 2
    assert runner.got_cancel[0] is not None
