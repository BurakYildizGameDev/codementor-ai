"""Aşama olayları (mimari §4): her aşama `StageEvent` yayınlar, süreler `stage_latency_ms` olur."""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field

import structlog

from codementor.log import get_logger
from codementor.models.pipeline import Stage, StageEvent, StageStatus

Listener = Callable[[StageEvent], None]
log = get_logger("codementor.pipeline")


@dataclass
class EventBus:
    """Abonelere `StageEvent` dağıtır; bir abonenin hatası analizi durdurmaz."""

    listeners: list[Listener] = field(default_factory=list)

    def subscribe(self, listener: Listener) -> Callable[[], None]:
        """Aboneliği ekler; dönen fonksiyon aboneliği kaldırır."""
        self.listeners.append(listener)
        return lambda: self.listeners.remove(listener)

    def publish(self, event: StageEvent) -> None:
        for listener in list(self.listeners):
            try:
                listener(event)
            except Exception as exc:  # gözlemci analizi bozamaz
                log.warning("stage_listener_failed", stage=event.stage, error=type(exc).__name__)


@dataclass
class StageTimer:
    """Bir analizin aşama süreleri ve token sayıları; olayları `bus`'a yayınlar."""

    analysis_id: str
    bus: EventBus
    latency_ms: dict[str, int] = field(default_factory=dict)
    tokens: dict[str, int] = field(default_factory=dict)
    notes: dict[str, str] = field(default_factory=dict)

    def emit(
        self,
        stage: Stage,
        status: StageStatus,
        *,
        duration_ms: int = 0,
        tokens: int = 0,
        detail: str | None = None,
    ) -> None:
        self.bus.publish(
            StageEvent(
                analysis_id=self.analysis_id,
                stage=stage,
                status=status,
                duration_ms=duration_ms,
                tokens=tokens,
                detail=detail,
            )
        )

    def skip(self, stage: Stage, detail: str | None = None) -> None:
        """Çalışmayan aşama: süresi 0 olarak kaydedilir (rapor tüm aşamaları içerir)."""
        self.latency_ms.setdefault(stage, 0)
        self.emit(stage, "skipped", detail=detail)

    def note(self, stage: Stage, detail: str) -> None:
        """Aşama tamamlandığında olayın `detail` alanına yazılır (ör. eval için şema sonucu)."""
        self.notes[stage] = detail

    def add_tokens(self, stage: Stage, count: int) -> None:
        self.tokens[stage] = self.tokens.get(stage, 0) + count

    @contextmanager
    def stage(self, stage: Stage) -> Iterator[None]:
        """`with timer.stage("tier0"):` süre ölçer, başarı/başarısızlık yayınlar."""
        self.emit(stage, "started")
        start = time.perf_counter()
        status: StageStatus = "completed"
        try:
            # bu aşamada (iş parçacığına geçenler dahil: to_thread bağlamı kopyalar) yazılan
            # log satırları `stage` taşır (mimari §13, Faz 50)
            with structlog.contextvars.bound_contextvars(stage=stage):
                yield
        except BaseException:
            status = "failed"
            raise
        finally:
            elapsed = int((time.perf_counter() - start) * 1000)
            self.latency_ms[stage] = self.latency_ms.get(stage, 0) + elapsed
            self.emit(
                stage,
                status,
                duration_ms=elapsed,
                tokens=self.tokens.get(stage, 0),
                detail=self.notes.pop(stage, None),
            )
