"""K0-K6 orkestratörü (mimari §4): katmanları sırayla çağırır; iş mantığı katman modüllerinde,
aşamalar `stages.py` / `passes.py`, rapor montajı `assemble.py`'de."""

from __future__ import annotations

import asyncio
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

from codementor.config import Settings, ValidationSettings
from codementor.ingest.errors import CodeTooLargeError, IngestError
from codementor.ingest.normalize import normalize
from codementor.models.enums import PipelineMode
from codementor.models.prompts import MentoringProfile, QuestionContext
from codementor.models.questions import Question
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest, LanguageHint, NormalizedCode
from codementor.models.validation import Tier1Result, Toolchain
from codementor.pipeline import stages
from codementor.pipeline.assemble import ReportParts, assemble_report, from_cache
from codementor.pipeline.cost import estimate_cost, load_pricing
from codementor.pipeline.events import EventBus, StageTimer
from codementor.pipeline.ids import new_ulid
from codementor.pipeline.passes import LLMOutcome, LLMSession, run_llm_passes
from codementor.pipeline.templates import degraded_socratic, early_exit_socratic, load_templates
from codementor.pipeline.versions import SCHEMA_VERSION, rules_version
from codementor.prompts.budget import PromptBudgetError, PromptConfigError
from codementor.prompts.mentoring import mentoring_profile
from codementor.prompts.templates import prompt_version
from codementor.providers.base import LLMProvider, ProviderError
from codementor.providers.factory import build_chain
from codementor.questions.bank import QuestionBank, QuestionNotFoundError
from codementor.storage import cache, sessions
from codementor.storage.db import Database
from codementor.validation.policy import decide
from codementor.validation.runner import Runner, run_process
from codementor.validation.tier0 import run_tier0
from codementor.validation.tier1 import run_tier1

ProviderFactory = Callable[[str], LLMProvider]


PipelineErrorKind = Literal["too_large", "invalid", "not_found", "provider"]


class PipelineError(Exception):
    """Analiz hiç yapılamadı (CLI çıkış kodu 3, API 413/422/404/503); mesaj Türkçe."""

    def __init__(self, message: str, kind: PipelineErrorKind) -> None:
        super().__init__(message)
        self.kind: PipelineErrorKind = kind


@dataclass
class _Run:
    """Tek analizin durumu."""

    request: AnalysisRequest
    timer: StageTimer
    provider_name: str
    attempt: int = 1
    question: Question | None = None
    context: QuestionContext | None = None
    warnings: list[str] = field(default_factory=list)

    @property
    def analysis_id(self) -> str:
        return self.timer.analysis_id


@dataclass
class Orchestrator:
    """`await Orchestrator(settings, db).analyze(request)`; `db` yoksa önbellek/oturum kapalı."""

    settings: Settings
    db: Database | None = None
    provider_factory: ProviderFactory | None = None
    bus: EventBus = field(default_factory=EventBus)
    toolchain: Toolchain | None = None
    tier1_runner: Runner = run_process

    async def analyze(self, request: AnalysisRequest) -> AnalysisReport:
        """§4 yaşam döngüsü. Kullanıcı hatasında `PipelineError`; sağlayıcı hatası bozulmadır."""
        name = request.provider or self.settings.providers.default
        run = _Run(request, StageTimer(new_ulid(), self.bus), name)
        code = self._ingest(run)
        if self.db is not None:
            run.attempt = sessions.next_attempt(self.db, request.session_id, request.question_id)
        profile = mentoring_profile(run.context.difficulty if run.context else None, run.attempt)
        try:
            provider = (self.provider_factory or self._build_provider)(name)
        except ProviderError as exc:
            raise PipelineError(f"Sağlayıcı kullanılamıyor: {exc}", "provider") from exc
        version = prompt_version(self.settings.prompts.dir)
        key = self._cache_key(run, code, profile, provider, version)

        cached = None
        with run.timer.stage("cache"):
            if self.db is not None and self._use_cache(request):
                cached = cache.find_cached(self.db, key)
        if cached is not None:
            report = from_cache(cached, run.analysis_id, run.timer)
        else:
            report = await self._analyze(run, code, provider, version, profile)
        # İptal kontrol noktası: Tier 0/1, önbellek ve erken çıkış yolları `await` içermez;
        # bekleyen bir iptal (masaüstü "Durdur", kopan SSE) kayıttan önce burada yükselir,
        # böylece yarıda kalan analiz yazılmaz ve ipucu merdiveni ilerlemez (Faz 19)
        await asyncio.sleep(0)
        if self.db is not None:
            latency = sum(report.meta.stage_latency_ms.values())
            cache.save_analysis(
                self.db, report, key=key, session_id=request.session_id, latency_ms=latency
            )
            sessions.record_attempt(
                self.db,
                request.session_id,
                request.question_id,
                attempt=run.attempt,
                hint_level=profile.hint_level,
            )
        return report

    def _build_provider(self, name: str) -> LLMProvider:
        return build_chain(self.settings, primary=name)

    def _use_cache(self, request: AnalysisRequest) -> bool:
        use = request.options.use_cache
        return self.settings.pipeline.use_cache if use is None else use

    def _ingest(self, run: _Run) -> NormalizedCode:
        request = run.request
        try:
            if request.question_id:
                bank = QuestionBank.load(self.settings.data.questions_dir)
                run.question = bank.get(request.question_id)
                run.context = QuestionContext.from_question(run.question)
            with run.timer.stage("ingest"):
                hint = LanguageHint(
                    language=request.language or (run.question.language if run.question else None),
                    engine=request.engine or (run.question.engine if run.question else None),
                )
                return normalize(request.code, hint, limits=self.settings.limits)
        except QuestionNotFoundError as exc:
            raise PipelineError(str(exc).strip("'\""), "not_found") from exc
        except CodeTooLargeError as exc:
            raise PipelineError(str(exc), "too_large") from exc
        except IngestError as exc:
            raise PipelineError(str(exc), "invalid") from exc

    def _cache_key(
        self,
        run: _Run,
        code: NormalizedCode,
        profile: MentoringProfile,
        provider: LLMProvider,
        version: str,
    ) -> str:
        config = getattr(self.settings.providers, run.provider_name, None)
        model = getattr(config, "model", None) or getattr(provider, "model", None)
        return cache.cache_key(
            normalized_code=code.text,
            language=code.language.value,
            engine=code.engine.value,
            question_id=run.request.question_id,
            hint_level=profile.hint_level,
            provider=run.provider_name,
            model=model if isinstance(model, str) else None,
            prompt_version=version,
            rules_version=rules_version(),
            schema_version=SCHEMA_VERSION,
        )

    async def _tier1(self, code: NormalizedCode, request: AnalysisRequest) -> Tier1Result:
        """Tier 1 iş parçacığında koşar (olay döngüsünü kilitlemez); görev iptal edilirse
        derleyici süreci zaman aşımını beklemeden öldürülür (Faz 24)."""
        cancel = threading.Event()
        try:
            return await asyncio.to_thread(
                run_tier1,
                code,
                self._validation(request),
                toolchain=self.toolchain,
                runner=self.tier1_runner,
                cancel=cancel,
            )
        except asyncio.CancelledError:
            cancel.set()
            raise

    def _validation(self, request: AnalysisRequest) -> ValidationSettings:
        tier1 = request.options.tier1
        if tier1 is None:
            return self.settings.validation
        return self.settings.validation.model_copy(update={"tier1_enabled": tier1})

    async def _analyze(
        self,
        run: _Run,
        code: NormalizedCode,
        provider: LLMProvider,
        version: str,
        profile: MentoringProfile,
    ) -> AnalysisReport:
        timer, settings = run.timer, self.settings
        templates = load_templates(settings.data.mentor_templates_file)
        # Ağır senkron aşamalar iş parçacığında: olay döngüsü (API'de diğer istekler, SSE)
        # kilitlenmez (Faz 26). Olaylar bu iş parçacığından yayınlanabilir; aboneler güvenli.
        with timer.stage("tier0"):
            tier0 = await asyncio.to_thread(run_tier0, code)
        tier1 = None
        if tier0.has_errors:
            timer.skip("tier1", "Tier 0 hatası")
        else:
            with timer.stage("tier1"):
                tier1 = await self._tier1(code, run.request)
        policy = decide(tier0, tier1)
        run.warnings += policy.warnings
        if policy.early_exit:  # §5.2.4: LLM hiç çağrılmaz
            socratic = early_exit_socratic(templates, policy.diagnostics, profile.hint_level)
            parts = ReportParts(policy=policy, socratic=socratic, early_exit=True)
            return self._report(run, code, parts, None, version)

        tags = list(run.question.concept_tags) if run.question else []
        static = await asyncio.to_thread(
            stages.run_static, code, run.context, tags, settings, timer, run.attempt
        )
        run.warnings += static.warnings
        reference, notes = stages.load_reference(run.question)
        run.warnings += notes
        verify = stages.VerifyArgs(
            code, static.findings, static.facts_input.hint, run.context, reference, settings
        )
        llm = LLMSession(provider, settings, timer)
        mode = run.request.options.mode or PipelineMode(settings.pipeline.mode)
        try:
            outcome = await run_llm_passes(
                llm, static, verify, profile, mode=mode, provider=run.provider_name
            )
        except (ProviderError, PromptBudgetError, PromptConfigError) as exc:
            outcome = LLMOutcome(verification=None, socratic=None)
            llm.warnings.append(f"Model kullanılamadı ({exc}); rapor statik analizle hazırlandı.")
        run.warnings += [*llm.warnings, *outcome.warnings]

        parts = ReportParts(policy=policy, degraded=outcome.verification is None)
        if outcome.verification is not None:
            verification, notes = stages.scrub_analysis(outcome.verification, verify, templates)
            run.warnings += [*verification.warnings, *notes]
            parts.findings, parts.complexity = verification.findings, verification.complexity
        else:
            parts.findings = static.findings
            parts.complexity = stages.degraded_complexity(static.hint, run.context)
        parts.socratic = outcome.socratic or degraded_socratic(
            templates, parts.findings, run.context, profile.hint_level
        )
        return self._report(run, code, parts, llm, version)

    def _report(
        self,
        run: _Run,
        code: NormalizedCode,
        parts: ReportParts,
        llm: LLMSession | None,
        version: str,
    ) -> AnalysisReport:
        report = assemble_report(
            analysis_id=run.analysis_id,
            code=code,
            question_id=run.request.question_id,
            difficulty=run.question.difficulty if run.question else None,
            parts=parts,
            llm=llm,
            prompt_version=version,
            warnings=run.warnings,
            timer=run.timer,
        )
        meta = report.meta
        meta.cost_est = estimate_cost(
            load_pricing(self.settings.data.pricing_file),
            meta.provider,
            meta.model,
            meta.tokens_in,
            meta.tokens_out,
        )
        return report
