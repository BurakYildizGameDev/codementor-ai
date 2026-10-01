"""Arka plan işleri ile Tk ana thread'i arasındaki köprü.

Tk widget'larına yalnızca ana thread dokunabilir. Uzun işler (analiz, sağlayıcı denetimi)
kendi thread'lerinde koşar ve sonuçlarını yalnızca bir `queue.Queue`'ya yazar; ana pencere
`after()` ile `drain()` çağırıp mesajları işler. Her görev adının bir "kuşağı" vardır: aynı
görev yeniden başlatılır ya da iptal edilirse eski thread'in geç gelen mesajları atılır.
"""

from __future__ import annotations

import asyncio
import queue
import threading
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from codementor.api.state import ApiState
from codementor.log import get_logger
from codementor.models.pipeline import StageEvent
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest
from codementor.pipeline.events import EventBus
from codementor.pipeline.orchestrator import PipelineError

MessageKind = Literal["event", "result", "error"]
Emit = Callable[[object], None]
Work = Callable[[Emit], object]

log = get_logger("codementor.desktop")


@dataclass(frozen=True)
class Message:
    task: str
    kind: MessageKind
    payload: object
    generation: int


class Bridge:
    """Adlandırılmış arka plan görevleri; mesajlar `drain()` ile ana thread'de okunur."""

    def __init__(self) -> None:
        self._queue: queue.Queue[Message] = queue.Queue()
        self._generation: dict[str, int] = {}
        self._threads: dict[str, threading.Thread] = {}
        self._lock = threading.Lock()

    def submit(self, task: str, work: Work) -> None:
        """`work(emit)` yeni bir thread'de koşar; dönüş değeri `result`, istisna `error` olur."""
        with self._lock:
            generation = self._generation.get(task, 0) + 1
            self._generation[task] = generation

        def emit(payload: object) -> None:
            self._queue.put(Message(task, "event", payload, generation))

        def run() -> None:
            try:
                result = work(emit)
            except Exception as exc:
                self._queue.put(Message(task, "error", user_message(exc), generation))
            else:
                self._queue.put(Message(task, "result", result, generation))

        thread = threading.Thread(target=run, name=f"codementor-{task}", daemon=True)
        self._threads[task] = thread
        thread.start()

    def cancel(self, task: str) -> None:
        """Görevin sonucunu yok sayar (thread kendi kendine biter; çıktısı atılır)."""
        with self._lock:
            self._generation[task] = self._generation.get(task, 0) + 1
        self._threads.pop(task, None)

    def is_running(self, task: str) -> bool:
        thread = self._threads.get(task)
        return thread is not None and thread.is_alive()

    def drain(self) -> list[Message]:
        """Bekleyen güncel mesajlar (iptal edilmiş/eskimiş kuşaklarınki atılır)."""
        messages: list[Message] = []
        while True:
            try:
                message = self._queue.get_nowait()
            except queue.Empty:
                return messages
            with self._lock:
                current = self._generation.get(message.task)
            if message.generation == current:
                messages.append(message)

    def join(self, task: str, timeout: float | None = None) -> None:
        """Testler ve kapanış için: görevin thread'inin bitmesini bekler."""
        thread = self._threads.get(task)
        if thread is not None:
            thread.join(timeout)


def user_message(exc: Exception) -> str:
    """Kullanıcıya gösterilecek Türkçe hata metni; beklenmeyen hatanın ayrıntısı log'a gider."""
    if isinstance(exc, PipelineError):
        return str(exc)
    log.error("desktop_task_failed", error=type(exc).__name__, detail=str(exc)[:300])
    return f"Beklenmeyen bir hata oluştu ({type(exc).__name__}). Ayrıntı log dosyasında."


def analysis_work(state: ApiState, request: AnalysisRequest) -> Work:
    """Analizi kendi olay yolu ve event loop'uyla koşan iş; aşama olaylarını `emit` eder."""

    def work(emit: Emit) -> AnalysisReport:
        bus = EventBus()

        def forward(event: StageEvent) -> None:
            emit(event)

        bus.subscribe(forward)
        return asyncio.run(state.orchestrator(bus).analyze(request))

    return work
