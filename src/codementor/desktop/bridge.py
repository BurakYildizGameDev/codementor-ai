"""Arka plan işleri ile Tk ana thread'i arasındaki köprü.

Tk widget'larına yalnızca ana thread dokunabilir. Uzun işler (analiz, sağlayıcı denetimi)
kendi thread'lerinde koşar ve sonuçlarını yalnızca bir `queue.Queue`'ya yazar; ana pencere
`after()` ile `drain()` çağırıp mesajları işler. Her görev adının bir "kuşağı" vardır: aynı
görev yeniden başlatılır ya da iptal edilirse eski thread'in geç gelen mesajları atılır.
İptal edilebilir görevler bir `Cancellation` taşır: `cancel()` asyncio görevini iptal eder,
CLI ajanının süreç ağacı da böylece öldürülür (Faz 19).
"""

from __future__ import annotations

import asyncio
import contextlib
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


class AnalysisCancelledError(Exception):
    """Analiz kullanıcı tarafından durduruldu (köprü sonucu kuşak sayacıyla atar)."""


class Cancellation:
    """Thread güvenli iptal işareti; geri çağrılar iptal anında (ya da sonradan eklenirse
    hemen) bir kez çalışır."""

    def __init__(self) -> None:
        self.event = threading.Event()
        self._callbacks: list[Callable[[], None]] = []
        self._lock = threading.Lock()

    @property
    def cancelled(self) -> bool:
        return self.event.is_set()

    def on_cancel(self, callback: Callable[[], None]) -> None:
        """İptalde çağrılacak işlev; zaten iptal edildiyse hemen çağrılır."""
        with self._lock:
            if not self.event.is_set():
                self._callbacks.append(callback)
                return
        callback()

    def cancel(self) -> None:
        with self._lock:
            if self.event.is_set():
                return
            self.event.set()
            callbacks, self._callbacks = self._callbacks, []
        for callback in callbacks:
            callback()


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
        self._cancellations: dict[str, Cancellation] = {}
        self._lock = threading.Lock()

    def submit(self, task: str, work: Work, *, cancellation: Cancellation | None = None) -> None:
        """`work(emit)` yeni bir thread'de koşar; dönüş değeri `result`, istisna `error` olur.

        `cancellation` verilirse `cancel(task)` işi gerçekten durdurur (yalnız sonucu atmaz).
        """
        with self._lock:
            generation = self._generation.get(task, 0) + 1
            self._generation[task] = generation
            previous = self._cancellations.pop(task, None)
            if cancellation is not None:
                self._cancellations[task] = cancellation
        if previous is not None:
            previous.cancel()  # yeniden başlatma: eski iş durdurulamaz hale gelmesin

        def emit(payload: object) -> None:
            self._queue.put(Message(task, "event", payload, generation))

        def run() -> None:
            try:
                result = work(emit)
            except Exception as exc:
                self._queue.put(Message(task, "error", user_message(exc), generation))
            else:
                self._queue.put(Message(task, "result", result, generation))
            finally:
                # biten işin iptal kaydı (kapanmış loop, kullanıcı kodu) tutulmaz
                with self._lock:
                    if cancellation is not None and self._cancellations.get(task) is cancellation:
                        del self._cancellations[task]

        thread = threading.Thread(target=run, name=f"codementor-{task}", daemon=True)
        self._threads[task] = thread
        thread.start()

    def cancel(self, task: str) -> None:
        """Görevin sonucunu yok sayar; iptal edilebilir görevse işi de durdurur."""
        with self._lock:
            self._generation[task] = self._generation.get(task, 0) + 1
            cancellation = self._cancellations.pop(task, None)
        if cancellation is not None:
            cancellation.cancel()

    def cancel_all(self) -> None:
        """Kapanışta: tüm görevlerin sonuçlarını yok sayar, iptal edilebilenleri durdurur."""
        for task in list(self._threads):
            self.cancel(task)

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
    if isinstance(exc, PipelineError | AnalysisCancelledError):
        return str(exc)  # iptal beklenen bir son: ERROR log'u üretmez
    log.error("desktop_task_failed", error=type(exc).__name__, detail=str(exc)[:300])
    return f"Beklenmeyen bir hata oluştu ({type(exc).__name__}). Ayrıntı log dosyasında."


def analysis_work(
    state: ApiState, request: AnalysisRequest, cancellation: Cancellation | None = None
) -> Work:
    """Analizi kendi olay yolu ve event loop'uyla koşan iş; aşama olaylarını `emit` eder.

    `cancellation` iptal edilince asyncio görevi iptal edilir (CLI süreci de öldürülür) ve iş
    `AnalysisCancelledError` ile biter; yarıda kalan analiz kaydedilmez.
    """

    def work(emit: Emit) -> AnalysisReport:
        bus = EventBus()

        def forward(event: StageEvent) -> None:
            emit(event)

        bus.subscribe(forward)

        async def main() -> AnalysisReport:
            if cancellation is not None:
                loop = asyncio.get_running_loop()
                task = asyncio.current_task()
                assert task is not None

                def stop() -> None:
                    # Analiz bittikten sonra gelen iptalde döngü kapanmış olabilir
                    with contextlib.suppress(RuntimeError):
                        loop.call_soon_threadsafe(task.cancel)

                cancellation.on_cancel(stop)
            return await state.orchestrator(bus).analyze(request)

        try:
            return asyncio.run(main())
        except asyncio.CancelledError as exc:
            raise AnalysisCancelledError("Analiz durduruldu.") from exc

    return work
