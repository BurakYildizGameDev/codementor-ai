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
from codementor.models.pipeline import StageEvent
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest
from codementor.pipeline.events import EventBus
from codementor.pipeline.orchestrator import Orchestrator, PipelineError

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

    def on_stage(event: StageEvent) -> None:
        queue.put_nowait(("stage", event.model_dump_json()))

    bus.subscribe(on_stage)
    orchestrator = make_orchestrator(bus)

    async def run() -> None:
        try:
            report: AnalysisReport = await orchestrator.analyze(request)
            queue.put_nowait(("report", report.model_dump_json()))
        except PipelineError as exc:
            problem = pipeline_problem(exc, path)
            queue.put_nowait(("error", json.dumps(problem.model_dump(exclude_none=True))))
        except Exception:
            detail = {
                "title": "Sunucu hatası",
                "status": 500,
                "detail": "Beklenmeyen bir hata oluştu.",
            }
            queue.put_nowait(("error", json.dumps(detail, ensure_ascii=False)))
        finally:
            queue.put_nowait(None)

    task = asyncio.create_task(run())
    try:
        while (item := await queue.get()) is not None:
            yield format_event(*item)
    finally:
        if not task.done():  # istemci bağlantıyı kesti
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task
