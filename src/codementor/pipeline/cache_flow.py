"""Önbellek ve kayıt akışı (G0): anahtar/imza hesabı, Tier 1 ayarı, deneme geri alma ve kayıt.

Zorunlu sıra korunur (mimari §4): anahtar → önbellek → analiz → iptal kontrol noktası → kayıt.
`orchestrator.py` 400 satırın altında kalsın diye iş mantığı burada; `Orchestrator` yöntemleri
ince sarmalayıcıdır (testler `_validation`, `_tier1` ve `_remaining` adlarını yamalıyor).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from codementor.config import ValidationSettings
from codementor.log import get_logger
from codementor.models.prompts import MentoringProfile
from codementor.models.report import AnalysisReport
from codementor.models.request import NormalizedCode
from codementor.pipeline.signature import pipeline_signature, tier1_tool
from codementor.pipeline.versions import SCHEMA_VERSION
from codementor.providers.base import LLMProvider
from codementor.providers.cli_agent import model_label
from codementor.storage import cache, sessions
from codementor.storage.db import Database

if TYPE_CHECKING:
    from codementor.pipeline.orchestrator import Orchestrator
    from codementor.pipeline.run_state import Run

log = get_logger("codementor.pipeline")


def validation_settings(orch: Orchestrator, run: Run) -> ValidationSettings:
    """Analiz başına bir kez: önbellek imzası ve Tier 1 aynı ayarı görür."""
    if run.validation is None:
        run.validation = orch._validation(run.request)  # analiz başına bir kez, isteğe göre
    return run.validation


def run_signature(orch: Orchestrator, run: Run, code: NormalizedCode) -> str:
    """Önbellek anahtarı için çıktıyı etkileyen ayarlar (Faz 35; Faz B/O3 tamamladı)."""
    validation = validation_settings(orch, run)
    return pipeline_signature(
        orch.settings,
        mode=orch._mode(run.request),
        validation=validation,
        tool=tier1_tool(code, validation, orch.toolchain),
        question=run.question,
    )


def cache_key(
    orch: Orchestrator,
    run: Run,
    code: NormalizedCode,
    profile: MentoringProfile,
    provider: LLMProvider,
    version: str,
) -> str:
    """Önbellek anahtarı: kod, dil, motor, soru, sağlayıcı/model, ayar imzası ve sürümler."""
    config = getattr(orch.settings.providers, run.provider_name, None)
    model = getattr(config, "model", None) or getattr(provider, "model", None)
    model = model_label(model if isinstance(model, str) else None, config)
    return cache.cache_key(
        normalized_code=code.text,
        language=code.language.value,
        engine=code.engine.value,
        question_id=run.request.question_id,
        hint_level=profile.hint_level,
        provider=run.provider_name,
        model=model if isinstance(model, str) else None,
        prompt_version=version,
        rules_version=orch._rules_version(),
        schema_version=SCHEMA_VERSION,
        pipeline=run_signature(orch, run, code),
    )


def release_attempt(db: Database, run: Run) -> None:
    """Ayrılan denemeyi geri verir; bu da başarısız olursa asıl istisnayı örtmez."""
    request = run.request
    try:
        sessions.release_attempt(db, request.session_id, request.question_id, run.attempt)
    except Exception as exc:
        log.warning("attempt_release_failed", error=type(exc).__name__)


def save_report(
    db: Database,
    run: Run,
    report: AnalysisReport,
    *,
    key: str,
    profile: MentoringProfile,
    max_analyses: int | None,
) -> None:
    """Raporu önbellek anahtarıyla kaydeder; ipucu merdivenini ilerletir ya da geri verir."""
    request = run.request
    latency = sum(report.meta.stage_latency_ms.values())
    cache.save_analysis(
        db,
        report,
        key=key,
        session_id=request.session_id,
        latency_ms=latency,
        max_analyses=max_analyses,
        cacheable=run.cacheable,
    )
    run.saved = True
    if not run.advance:
        return
    counts = not report.meta.early_exit and not report.meta.degraded
    if counts:
        sessions.record_attempt(
            db,
            request.session_id,
            request.question_id,
            attempt=run.attempt,
            hint_level=profile.hint_level,
        )
    else:
        sessions.release_attempt(db, request.session_id, request.question_id, run.attempt)
