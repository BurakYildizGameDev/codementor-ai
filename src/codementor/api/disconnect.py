"""Senkron uçta istemci kopması (Faz 48): bağlantı kesilince analiz görevi iptal edilir.

SSE'de kopma akış üretecinin kapanmasıyla algılanır (`api/sse.py`); senkron `/v1/analyze`
yanıtı tek seferde yazdığından kopmayı ASGI `receive` kanalından dinler. Gövde FastAPI
tarafından zaten okunmuştur; sonraki `receive()` yalnızca `http.disconnect` ile döner.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Coroutine
from typing import Any

from starlette.types import Receive

from codementor.log import get_logger

log = get_logger("codementor.api")


class ClientDisconnectedError(Exception):
    """İstemci yanıt beklemeden bağlantıyı kesti; analiz iptal edildi."""


async def _wait_disconnect(receive: Receive) -> None:
    while (await receive())["type"] != "http.disconnect":
        pass


async def run_until_disconnect[T](receive: Receive, work: Coroutine[Any, Any, T]) -> T:
    """`work`'ü koşar; önce istemci koparsa görevi iptal eder ve `ClientDisconnectedError`."""
    task = asyncio.ensure_future(work)
    watcher = asyncio.ensure_future(_wait_disconnect(receive))
    try:
        await asyncio.wait({task, watcher}, return_when=asyncio.FIRST_COMPLETED)
    finally:
        for pending in (task, watcher):
            if not pending.done():
                pending.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await pending
    if task.cancelled():
        if not watcher.cancelled() and (error := watcher.exception()) is not None:
            # kanal okunamadı: bağlantı yok sayılır, istisna sessiz kalmaz (Faz 48 denetimi)
            log.warning("disconnect_watch_failed", error=type(error).__name__)
        log.info("analysis_cancelled_on_disconnect")
        raise ClientDisconnectedError
    return task.result()
