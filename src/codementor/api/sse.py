"""SSE ilerleme akışı (mimari §9): `stage` olayları, sonda `report` (ya da `error`).

Her istek kendi `EventBus`'ını kullanır (eşzamanlı analizlerin olayları karışmaz); olaylar
`asyncio.Queue` ile akar. İstemci bağlantıyı keserse analiz görevi iptal edilir.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import AsyncIterator, Callable

from codementor.api.errors import pipeline_problem
from codementor.log import get_logger
from codementor.models.pipeline import StageEvent
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest
from codementor.pipeline.events import EventBus
from codementor.pipeline.orchestrator import Orchestrator
from codementor.pipeline.run_state import PipelineError

log = get_logger("codementor.api")

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",  # nginx tamponlamasın
    "Connection": "keep-alive",
}


def format_event(event: str, data: str) -> str:
    """Tek SSE kaydı; `data` tek satır JSON olmalı."""
    return f"event: {event}\ndata: {data}\n\n"


async def stream_analysis(
    make_orchestrator: Callable[[EventBus], Orchestrator],
    request: AnalysisRequest,
    path: str,
) -> AsyncIterator[str]:
    """Analizi arka planda çalıştırır, olaylarını SSE metni olarak verir."""
    queue: asyncio.Queue[tuple[str, str] | None] = asyncio.Queue()  # None: akış bitti
    bus = EventBus()
    loop = asyncio.get_running_loop()

    def post(item: tuple[str, str] | None) -> None:
        # Aşama olayları iş parçacığından da gelir (Faz 26: Tier 0/statik `to_thread`);
        # asyncio.Queue thread güvenli değil. Hepsi aynı yoldan: sıra korunur (FIFO)
        loop.call_soon_threadsafe(queue.put_nowait, item)

    def on_stage(event: StageEvent) -> None:
        post(("stage", event.model_dump_json()))

    bus.subscribe(on_stage)
    orchestrator = make_orchestrator(bus)

    async def run() -> None:
        try:
            report: AnalysisReport = await orchestrator.analyze(request)
            post(("report", report.model_dump_json()))
        except PipelineError as exc:
            problem = pipeline_problem(exc, path)
            post(("error", json.dumps(problem.model_dump(exclude_none=True))))
        except Exception as exc:
            # Mesaj kod parçası taşıyabilir (§12): yalnız tür loglanır (Faz 48)
            log.error("analysis_stream_failed", error=type(exc).__name__)
            detail = {
                "title": "Sunucu hatası",
                "status": 500,
                "detail": "Beklenmeyen bir hata oluştu.",
            }
            post(("error", json.dumps(detail, ensure_ascii=False)))
        finally:
            post(None)

    task = asyncio.create_task(run())
    try:
        while (item := await queue.get()) is not None:
            yield format_event(*item)
    finally:
        if not task.done():  # istemci bağlantıyı kesti
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task
