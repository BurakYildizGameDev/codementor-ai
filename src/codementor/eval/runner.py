"""Eval koşucusu (mimari §14.3): örnekleri pipeline'dan geçirir, metrikleri hesaplar.

Önbellek her zaman kapalı (veritabanı yok, `use_cache=False`); sonuç dosyası tüm metrikleri
ve sürümleri (prompt/kural/şema/model) içerir. `--static-only`: her çağrıda hata veren sağlayıcı
→ pipeline zarif bozulmaya düşer → rapor yalnızca statik analizdir (LLM'siz taban çizgisi).
"""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel

from codementor.config import Settings
from codementor.eval.metrics import compute_metrics
from codementor.models.enums import PipelineMode
from codementor.models.eval import PricingFile, RunConfig, RunResult, Sample, SampleResult, Split
from codementor.models.pipeline import StageEvent
from codementor.models.provider import (
    ChatMessage,
    GenerationOptions,
    ProviderCapabilities,
    ProviderResult,
)
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.pipeline.events import EventBus
from codementor.pipeline.orchestrator import Orchestrator, PipelineError, ProviderFactory
from codementor.pipeline.passes import SCHEMA_INVALID, SCHEMA_OK
from codementor.pipeline.versions import SCHEMA_VERSION, rules_version
from codementor.prompts.templates import prompt_version
from codementor.providers.base import LLMProvider, ProviderUnavailableError
from codementor.providers.factory import build_chain
from codementor.questions._loader import DataFileError, load_model

STATIC_ONLY = "static-only"
ABLATIONS = ("facts", "line_numbers", "fewshot0", "fewshot1")
_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")

Progress = Callable[[int, int, SampleResult], None]


class PricingError(DataFileError):
    """`data/pricing.yaml` okunamadı ya da geçersiz."""


@dataclass
class StaticOnlyProvider:
    """LLM'siz taban çizgisi: her çağrı hemen başarısız olur (pipeline statik rapora düşer)."""

    name: str = STATIC_ONLY
    model: str = ""
    capabilities: ProviderCapabilities = field(
        default_factory=lambda: ProviderCapabilities(native_schema=False, strict_schema=False)
    )

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> ProviderResult:
        raise ProviderUnavailableError(self.name, "LLM kapalı (taban çizgisi)")


def apply_ablations(settings: Settings, ablations: list[str]) -> Settings:
    """§14.4 ablasyonları: `facts` (olgu + ipucu yok), `line_numbers` (düz kod),
    `fewshot0`/`fewshot1` (örnek sayısı)."""
    unknown = sorted(set(ablations) - set(ABLATIONS))
    if unknown:
        raise ValueError(f"Bilinmeyen ablasyon: {', '.join(unknown)}")
    update: dict[str, object] = {}
    if "facts" in ablations:
        update["include_facts"] = False
    if "line_numbers" in ablations:
        update["numbered_code"] = False
    if "fewshot0" in ablations:
        update["max_fewshots"] = 0
    elif "fewshot1" in ablations:
        update["max_fewshots"] = 1
    return settings.model_copy(update={"prompts": settings.prompts.model_copy(update=update)})


def load_pricing(settings: Settings) -> PricingFile | None:
    """`data/pricing.yaml` (yoksa None: maliyet tahmini yapılmaz)."""
    path = settings.data.questions_dir.parent / "pricing.yaml"
    if not path.is_file():
        return None
    return load_model(path, PricingFile, PricingError)


def _schema_flags(events: list[StageEvent]) -> tuple[bool | None, bool | None]:
    """`verify_a` olaylarının notlarından (ilk yanıt, son yanıt) şema sonucu."""
    notes = [
        e.detail
        for e in events
        if e.stage == "verify_a"
        and e.status == "completed"
        and e.detail in (SCHEMA_OK, SCHEMA_INVALID)
    ]
    if not notes:
        return None, None
    return notes[0] == SCHEMA_OK, notes[-1] == SCHEMA_OK


async def run_sample(
    sample: Sample,
    settings: Settings,
    provider_factory: ProviderFactory,
    provider_name: str,
    mode: PipelineMode,
) -> SampleResult:
    """Tek örnek; önbellek kapalı, veritabanı yok."""
    events: list[StageEvent] = []
    bus = EventBus()
    bus.subscribe(events.append)
    orchestrator = Orchestrator(settings, None, provider_factory=provider_factory, bus=bus)
    label = sample.label
    request = AnalysisRequest(
        code=sample.code,
        language=label.language,
        engine=label.engine,
        question_id=label.question_id,
        provider=provider_name,
        options=AnalysisOptions(mode=mode, use_cache=False),
    )
    start = time.perf_counter()
    try:
        report = await orchestrator.analyze(request)
        error = None
    except PipelineError as exc:
        report, error = None, str(exc)
    latency = int((time.perf_counter() - start) * 1000)
    first, final = _schema_flags(events)
    called = any(e.stage == "llm_a" and e.status == "completed" for e in events)
    return SampleResult(
        id=label.id,
        report=report,
        error=error,
        latency_ms=latency,
        llm_called=called,
        schema_first_try=first,
        schema_final=final,
    )


async def run_eval(
    samples: list[Sample],
    settings: Settings,
    *,
    split: Split,
    provider: str | None,
    mode: PipelineMode,
    static_only: bool = False,
    ablations: list[str] | None = None,
    provider_factory: ProviderFactory | None = None,
    progress: Progress | None = None,
) -> RunResult:
    """Örnekleri sırayla çalıştırır (sağlayıcı kotasını zorlamamak için eşzamansız değil)."""
    ablations = ablations or []
    settings = apply_ablations(settings, ablations)
    name = STATIC_ONLY if static_only else provider or settings.providers.default
    if static_only:
        baseline = StaticOnlyProvider()

        def factory(_name: str) -> LLMProvider:
            return baseline

        provider_factory = factory
    config = getattr(settings.providers, name, None)
    model = getattr(config, "model", None) or None
    run_config = RunConfig(
        split=split,
        provider=None if static_only else name,
        model=None if static_only else model,
        mode="static" if static_only else mode.value,
        static_only=static_only,
        ablations=ablations,
        prompt_version=prompt_version(settings.prompts.dir),
        rules_version=rules_version(),
        schema_version=SCHEMA_VERSION,
        started_at=datetime.now(UTC),
        sample_ids=[s.label.id for s in samples],
        reviewed_only=all(s.label.reviewed for s in samples),
    )
    results: list[SampleResult] = []
    for index, sample in enumerate(samples, start=1):
        factory_for_run = provider_factory or _default_factory(settings)
        result = await run_sample(sample, settings, factory_for_run, name, mode)
        results.append(result)
        if progress is not None:
            progress(index, len(samples), result)
    pairs = [(s.label, r) for s, r in zip(samples, results, strict=True)]
    metrics = compute_metrics(pairs, None if static_only else load_pricing(settings))
    return RunResult(config=run_config, metrics=metrics, samples=results)


def _default_factory(settings: Settings) -> ProviderFactory:
    def factory(name: str) -> LLMProvider:
        return build_chain(settings, primary=name)

    return factory


def result_filename(config: RunConfig) -> str:
    """`{zaman}_{sağlayıcı}_{model}_{mod}[_{ablasyon}]_{bölüm}.json` (§14.3)."""
    parts = [
        config.started_at.strftime("%Y%m%dT%H%M%S"),
        config.provider or "static",
        config.model or "none",
        config.mode,
        *config.ablations,
        config.split,
    ]
    return "_".join(_UNSAFE.sub("-", p) for p in parts) + ".json"


def save_result(result: RunResult, directory: Path) -> Path:
    """Sonucu JSON olarak yazar."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / result_filename(result.config)
    path.write_text(result.model_dump_json(indent=2), encoding="utf-8", newline="\n")
    return path
