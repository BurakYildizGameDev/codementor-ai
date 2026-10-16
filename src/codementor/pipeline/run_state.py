"""Analiz durumu ve işlem hataları (G0 bölmesinin devamı).

`Run` tek analizin taşıdığı durum, `AnalysisTrace` çağırana dönen iç kayıtlar, `PipelineError`
kullanıcıya dönük hata sınıfıdır. G0'da `orchestrator.py` aşamaları yan modüllere (cache_flow,
deadline, llm_session, verify_pass) taşındı; bu modüller `Run`'ı kullanabilmek için `orchestrator`'ı
içe aktarmak zorundaydı. Veri sözleşmesi buraya alınınca bağımlılık yönü tek yönlü olur
(`cache_flow`, `deadline` → `run_state`) ve `orchestrator.py` 400 satırın altında kalır.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

from codementor.config import ValidationSettings
from codementor.models.prompts import QuestionContext
from codementor.models.questions import Question
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest
from codementor.models.verification import FindingCheck
from codementor.pipeline.events import StageTimer
from codementor.providers.base import LLMProvider

ProviderFactory = Callable[[str], LLMProvider]

PipelineErrorKind = Literal["too_large", "invalid", "not_found", "provider", "unavailable"]

BANK_UNREADABLE = "Soru bankası okunamadı; ayrıntı sunucu log'unda."


class PipelineError(Exception):
    """Analiz hiç yapılamadı (CLI çıkış kodu 3, API 413/422/404/503); mesaj Türkçe."""

    def __init__(self, message: str, kind: PipelineErrorKind) -> None:
        super().__init__(message)
        self.kind: PipelineErrorKind = kind


@dataclass
class Run:
    """Tek analizin durumu."""

    request: AnalysisRequest
    timer: StageTimer
    provider_name: str
    attempt: int = 1
    started: float = field(default_factory=time.monotonic)
    question: Question | None = None
    context: QuestionContext | None = None
    warnings: list[str] = field(default_factory=list)
    finding_checks: list[FindingCheck] = field(default_factory=list)
    saved: bool = False  # analiz kaydedildi: deneme artık geri alınmaz (Faz 49)
    advance: bool = True  # Faz 61: advance_hint=False iken ayırma/kayıt yapılmaz
    cacheable: bool = True  # Faz B (Y5): fallback ya da yarım LLM sonucu önbelleğe girmez
    validation: ValidationSettings | None = None  # isteğe göre Tier 1 ayarı (bir kez)

    @property
    def analysis_id(self) -> str:
        return self.timer.analysis_id


@dataclass(frozen=True)
class AnalysisTrace:
    """Rapor ve öğrenciye gösterilmeyen iç kayıtlar (eval için; Faz 39)."""

    report: AnalysisReport
    finding_checks: list[FindingCheck]
