"""K0-K6 orkestratörü (mimari §4): katmanları sırayla çağırır; iş mantığı katman modüllerinde,
aşamalar `stages.py` / `passes.py`, rapor montajı `assemble.py`'de."""

from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

import structlog

from codementor.config import Settings, ValidationSettings
from codementor.ingest.errors import CodeTooLargeError, IngestError
from codementor.ingest.normalize import normalize
from codementor.log import get_logger
from codementor.models.enums import PipelineMode
from codementor.models.prompts import MentoringProfile, QuestionContext
from codementor.models.questions import Question
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest, LanguageHint, NormalizedCode
from codementor.models.validation import Tier1Result, Toolchain
from codementor.models.verification import FindingCheck
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
from codementor.providers.cli_agent import model_label
from codementor.providers.factory import build_chain
from codementor.questions.bank import QuestionBank, QuestionBankError, QuestionNotFoundError
from codementor.storage import cache, sessions
from codementor.storage.db import Database
from codementor.validation.policy import decide
from codementor.validation.runner import Runner, run_process
from codementor.validation.tier0_isolation import STOP_WARNING, check_syntax, stopped
from codementor.validation.tier1 import run_tier1

ProviderFactory = Callable[[str], LLMProvider]


PipelineErrorKind = Literal["too_large", "invalid", "not_found", "provider", "unavailable"]

log = get_logger("codementor.pipeline")
BANK_UNREADABLE = "Soru bankası okunamadı; ayrıntı sunucu log'unda."


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
    started: float = field(default_factory=time.monotonic)
    question: Question | None = None
    context: QuestionContext | None = None
    warnings: list[str] = field(default_factory=list)
    finding_checks: list[FindingCheck] = field(default_factory=list)
    saved: bool = False  # analiz kaydedildi: deneme artık geri alınmaz (Faz 49)

    @property
    def analysis_id(self) -> str:
        return self.timer.analysis_id


@dataclass(frozen=True)
class AnalysisTrace:
    """Rapor ve öğrenciye gösterilmeyen iç kayıtlar (eval için; Faz 39)."""

    report: AnalysisReport
    finding_checks: list[FindingCheck]


@dataclass
class Orchestrator:
    """`await Orchestrator(settings, db).analyze(request)`; `db` yoksa önbellek/oturum kapalı."""

    settings: Settings
    db: Database | None = None
    provider_factory: ProviderFactory | None = None
    bus: EventBus = field(default_factory=EventBus)
    toolchain: Toolchain | None = None
    tier1_runner: Runner = run_process
    # Faz 49: API/masaüstü süreç başına yüklenmiş bankayı verir; yoksa her istekte diskten
    questions: Callable[[], QuestionBank] | None = None

    async def analyze(self, request: AnalysisRequest) -> AnalysisReport:
        """§4 yaşam döngüsü. Kullanıcı hatasında `PipelineError`; sağlayıcı hatası bozulmadır."""
        return (await self.analyze_traced(request)).report

    async def analyze_traced(self, request: AnalysisRequest) -> AnalysisTrace:
        """`analyze` ile aynı; ek olarak doğrulama geçişi kararlarını döndürür (önbellekten
        gelen raporda boştur)."""
        name = request.provider or self.settings.providers.default
        run = _Run(request, StageTimer(new_ulid(), self.bus), name)
        # analiz boyunca yazılan her log satırı `analysis_id` taşır (mimari §13, Faz 50)
        with structlog.contextvars.bound_contextvars(analysis_id=run.analysis_id):
            return await self._traced(run)

    async def _traced(self, run: _Run) -> AnalysisTrace:
        request = run.request
        code = self._ingest(run)
        if self.db is not None:
            # Faz 49: atomik ayırma; eşzamanlı gönderimler ayrı deneme alır
            run.attempt = sessions.reserve_attempt(self.db, request.session_id, request.question_id)
        try:
            return await self._run_attempt(run, code)
        except BaseException:
            # iptal ya da hata: yarıda kalan analiz ipucu merdivenini ilerletmez (Faz 19);
            # kayıt yazıldıysa deneme geçmişte durur, geri alınmaz
            if self.db is not None and not run.saved:
                self._release(run)
            raise

    def _release(self, run: _Run) -> None:
        """Ayrılan denemeyi geri verir; bu da başarısız olursa asıl istisnayı örtmez."""
        assert self.db is not None
        request = run.request
        try:
            sessions.release_attempt(self.db, request.session_id, request.question_id, run.attempt)
        except Exception as exc:
            log.warning("attempt_release_failed", error=type(exc).__name__)

    async def _run_attempt(self, run: _Run, code: NormalizedCode) -> AnalysisTrace:
        request = run.request
        name = run.provider_name
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
                self.db,
                report,
                key=key,
                session_id=request.session_id,
                latency_ms=latency,
                max_analyses=self.settings.storage.max_analyses,
            )
            run.saved = True
            sessions.record_attempt(
                self.db,
                request.session_id,
                request.question_id,
                attempt=run.attempt,
                hint_level=profile.hint_level,
            )
        return AnalysisTrace(report, run.finding_checks)

    def _build_provider(self, name: str) -> LLMProvider:
        return build_chain(self.settings, primary=name)

    def _use_cache(self, request: AnalysisRequest) -> bool:
        use = request.options.use_cache
        return self.settings.pipeline.use_cache if use is None else use

    def _ingest(self, run: _Run) -> NormalizedCode:
        request = run.request
        try:
            if request.question_id:
                bank = self._question_bank()
                run.question = bank.get(request.question_id)
                run.context = QuestionContext.from_question(run.question)
            with run.timer.stage("ingest"):
                hint = LanguageHint(
                    language=request.language or (run.question.language if run.question else None),
                    engine=request.engine or (run.question.engine if run.question else None),
                )
                return normalize(request.code, hint, limits=self.settings.limits)
        except QuestionBankError as exc:
            # dosya adı/ayrıştırıcı ayrıntısı yanıta değil log'a (Faz 49 denetimi)
            log.error("question_bank_unreadable", error=type(exc).__name__, detail=str(exc)[:300])
            raise PipelineError(BANK_UNREADABLE, "unavailable") from exc
        except QuestionNotFoundError as exc:
            raise PipelineError(str(exc).strip("'\""), "not_found") from exc
        except CodeTooLargeError as exc:
            raise PipelineError(str(exc), "too_large") from exc
        except IngestError as exc:
            raise PipelineError(str(exc), "invalid") from exc

    def _question_bank(self) -> QuestionBank:
        if self.questions is not None:
            return self.questions()
        return QuestionBank.load(self.settings.data.questions_dir)

    def _rules_version(self) -> str:
        data = self.settings.data
        return rules_version(data.call_costs_file, data.mentor_templates_file)

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
            rules_version=self._rules_version(),
            schema_version=SCHEMA_VERSION,
            pipeline=self._pipeline_signature(run.request),
        )

    def _mode(self, request: AnalysisRequest) -> PipelineMode:
        return request.options.mode or PipelineMode(self.settings.pipeline.mode)

    def _pipeline_signature(self, request: AnalysisRequest) -> str:
        """Önbellek anahtarı için çıktıyı etkileyen pipeline ayarları (Faz 35)."""
        verify = "+verify" if self.settings.pipeline.verify_findings else ""
        return f"{self._mode(request).value}{verify}"

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
        # İstek Tier 1'i yalnız kapatabilir; yapılandırmada kapalıysa açamaz (Faz 47, ADR-0023)
        if request.options.tier1 is not False:
            return self.settings.validation
        return self.settings.validation.model_copy(update={"tier1_enabled": False})

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
            # Faz 59: yapılandırmaya göre süre/bellek sınırlı alt süreçte (ADR-0025)
            tier0 = await asyncio.to_thread(check_syntax, code, settings.validation)
        if stopped(tier0):  # erken çıkış eksik bir rapordur; kullanıcı bilsin
            run.warnings.append(STOP_WARNING)
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
        mode = self._mode(run.request)
        limit = settings.pipeline.analysis_timeout_s
        remaining = self._remaining(run, limit)
        outcome: LLMOutcome | None = None
        if remaining != 0.0:  # süre LLM'den önce bittiyse CLI süreci hiç açılmaz
            try:
                # Aşım görevi iptal eder; CLI sağlayıcıları iptalde süreç ağacını öldürür (Faz 48)
                async with asyncio.timeout(remaining) as deadline:
                    outcome = await run_llm_passes(
                        llm, static, verify, profile, mode=mode, provider=run.provider_name
                    )
            except (ProviderError, PromptBudgetError, PromptConfigError) as exc:
                outcome = LLMOutcome(verification=None, socratic=None)
                llm.warnings.append(
                    f"Model kullanılamadı ({exc}); rapor statik analizle hazırlandı."
                )
            except TimeoutError:
                if not deadline.expired():  # başka kaynaklı zaman aşımı bizim sınırımız değil
                    raise
        if outcome is None:
            outcome = LLMOutcome(verification=None, socratic=None)
            llm.warnings.append(
                f"Analiz süre sınırı ({limit:g} sn) aşıldı; rapor statik analizle hazırlandı."
            )
        run.warnings += [*llm.warnings, *outcome.warnings]

        parts = ReportParts(policy=policy, degraded=outcome.verification is None)
        if outcome.verification is not None:
            verification, notes = stages.scrub_analysis(outcome.verification, verify, templates)
            run.warnings += [*verification.warnings, *notes]
            run.finding_checks = verification.finding_checks
            parts.findings, parts.complexity = verification.findings, verification.complexity
        else:
            parts.findings = static.findings
            parts.complexity = stages.degraded_complexity(static.hint, run.context)
        parts.socratic = outcome.socratic or degraded_socratic(
            templates, parts.findings, run.context, profile.hint_level
        )
        return self._report(run, code, parts, llm, version)

    @staticmethod
    def _remaining(run: _Run, limit: float | None) -> float | None:
        """Toplam süre sınırından kalan saniye (Tier 0/1 ve statik aşama düşülmüş); yoksa None."""
        if limit is None:
            return None
        return max(limit - (time.monotonic() - run.started), 0.0)

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
            rules_version_value=self._rules_version(),
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
