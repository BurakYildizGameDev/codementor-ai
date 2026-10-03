"""CLI ilerleme satırı (Faz 33): aşama adı, canlı geçen süre ve harcanan token."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field

from codementor.models.pipeline import Stage, StageEvent

STAGE_LABELS: dict[Stage, str] = {
    "cache": "Önbellek",
    "ingest": "Giriş",
    "tier0": "Sözdizimi",
    "tier1": "Derleyici",
    "facts": "Olgular",
    "rules": "Kurallar",
    "prompt_a": "Prompt A",
    "llm_a": "LLM analiz",
    "verify_a": "Doğrulama A",
    "prompt_v": "Prompt V",
    "llm_v": "LLM bulgu doğrulama",
    "verify_v": "Doğrulama V",
    "prompt_b": "Prompt B",
    "llm_b": "LLM mentorluk",
    "verify_b": "Doğrulama B",
    "report": "Rapor",
}
_START_LABEL = "Analiz başlıyor…"


@dataclass
class ProgressLine:
    """Olaylardan durum metni. Olaylar iş parçacıklarından da gelebilir (Faz 26); kilitli."""

    started: float
    stage: Stage | None = None
    tokens: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def on_event(self, event: StageEvent) -> None:
        with self._lock:
            if event.status == "started":
                self.stage = event.stage
            elif event.status in ("completed", "failed"):
                self.tokens += event.tokens

    def text(self, now: float) -> str:
        """`LLM analiz · 12,3 sn · 4512 token` (token yoksa son kısım yok)."""
        with self._lock:
            label = STAGE_LABELS[self.stage] if self.stage is not None else _START_LABEL
            seconds = f"{max(0.0, now - self.started):.1f}".replace(".", ",")
            parts = [label, f"{seconds} sn"]
            if self.tokens:
                parts.append(f"{self.tokens} token")
            return " · ".join(parts)
