"""K0-K6 orkestratörü (mimari §4): katmanları sırayla çağırır; iş mantığı katman modüllerinde,
aşamalar `stages.py` / `passes.py`, rapor montajı `assemble.py`, önbellek/kayıt akışı
`cache_flow.py`, süre sınırı `deadline.py`'de (G0)."""

from __future__ import annotations

import asyncio
import threading
from collections.abc import Callable
from dataclasses import dataclass, field

import structlog

from codementor.config import Settings, ValidationSettings
from codementor.ingest.errors import CodeTooLargeError, IngestError
from codementor.ingest.normalize import normalize
from codementor.log import get_logger
from codementor.models.enums import PipelineMode
from codementor.models.prompts import MentoringProfile, QuestionContext
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest, LanguageHint, NormalizedCode
from codementor.models.validation import SkipReason, Tier1Result, Toolchain
from codementor.pipeline import cache_flow, deadline, stages
from codementor.pipeline.assemble import ReportParts, assemble_with_cost, from_cache
from codementor.pipeline.events import EventBus, StageTimer
from codementor.pipeline.ids import new_ulid
from codementor.pipeline.passes import LLMOutcome, LLMSession, run_llm_passes
from codementor.pipeline.run_state import (
    BANK_UNREADABLE,
    AnalysisTrace,
    PipelineError,
    ProviderFactory,
    Run,
)
from codementor.pipeline.templates import degraded_socratic, early_exit_socratic, load_templates
from codementor.pipeline.versions import rules_version
from codementor.prompts.budget import PromptBudgetError, PromptConfigError
from codementor.prompts.mentoring import mentoring_profile
from codementor.prompts.templates import UNAVAILABLE_VERSION, PromptTemplateError, prompt_version
from codementor.providers.base import LLMProvider, ProviderError
from codementor.providers.factory import build_chain
from codementor.questions.bank import QuestionBank, QuestionBankError, QuestionNotFoundError
from codementor.storage import cache, sessions
from codementor.storage.db import Database
from codementor.validation.policy import decide
from codementor.validation.runner import Runner, run_process
from codementor.validation.tier0_isolation import STOP_WARNING, check_syntax, stopped
from codementor.validation.tier1 import run_tier1

# Tier 1'in geçici atlanma nedenleri: bu raporlar önbelleğe girmez (denetim O-3)
_TRANSIENT_SKIPS = frozenset({SkipReason.TIMEOUT, SkipReason.TOOL_ERROR})

log = get_logger("codementor.pipeline")


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
    # D11: enjekte edilmeyen banka ve veri dosyası sürümü örnek başına bir kez okunur. Örnek
    # istek/örnekleme başına kurulduğu için (API, masaüstü, CLI, eval) tazelik korunur.
    _bank: QuestionBank | None = field(default=None, init=False, repr=False, compare=False)
    _rules: str | None = field(default=None, init=False, repr=False, compare=False)

    async def analyze(self, request: AnalysisRequest) -> AnalysisReport:
        """§4 yaşam döngüsü. Kullanıcı hatasında `PipelineError`; sağlayıcı hatası bozulmadır."""
        return (await self.analyze_traced(request)).report

    async def analyze_traced(self, request: AnalysisRequest) -> AnalysisTrace:
        """`analyze` ile aynı; ek olarak doğrulama geçişi kararlarını döndürür (önbellekten
        gelen raporda boştur)."""
        name = request.provider or self.settings.providers.default
        run = Run(request, StageTimer(new_ulid(), self.bus), name)
        # analiz boyunca yazılan her log satırı `analysis_id` taşır (mimari §13, Faz 50)
        with structlog.contextvars.bound_contextvars(analysis_id=run.analysis_id):
            return await self._traced(run)

    async def _traced(self, run: Run) -> AnalysisTrace:
        request = run.request
        code = await self._ingest(run)
        if self.db is not None:
            if request.options.advance_hint is False:
                current = (
                    sessions.next_attempt(self.db, request.session_id, request.question_id) - 1
                )
                run.attempt = max(1, current)
                run.advance = False
            else:
                # Faz 49: atomik ayırma; eşzamanlı gönderimler ayrı deneme alır
                run.attempt = sessions.reserve_attempt(
                    self.db, request.session_id, request.question_id
                )
        try:
            return await self._run_attempt(run, code)
        except BaseException:
            # iptal ya da hata: yarıda kalan analiz ipucu merdivenini ilerletmez (Faz 19);
            # kayıt yazıldıysa istisnalar için deneme geçmişte durur, geri alınmaz
            if self.db is not None and run.advance and not run.saved:
                self._release(run)
            raise

    def _release(self, run: Run) -> None:
        """Ayrılan denemeyi geri verir (gövde `cache_flow.release_attempt`, G0)."""
        assert self.db is not None
        cache_flow.release_attempt(self.db, run)

    async def _run_attempt(self, run: Run, code: NormalizedCode) -> AnalysisTrace:
        request = run.request
        name = run.provider_name
        profile = mentoring_profile(run.context.difficulty if run.context else None, run.attempt)
        try:
            provider = (self.provider_factory or self._build_provider)(name)
        except ProviderError as exc:
            raise PipelineError(f"Sağlayıcı kullanılamıyor: {exc}", "provider") from exc
        try:
            version = prompt_version(self.settings.prompts.dir)
        except PromptTemplateError as exc:
            # D8: şablon dizini okunamazsa prompt kurulamaz. Analiz ham `FileNotFoundError` ile
            # 500'e düşmez: sürüm yer tutucu olur, LLM geçişi bozulmaya iner ve rapor statik
            # analizle üretilir. Rapor önbelleğe alınmaz (kurulum düzelince yeniden üretilsin).
            log.error(
                "prompt_templates_unreadable", error=type(exc).__name__, detail=str(exc)[:300]
            )
            version = UNAVAILABLE_VERSION
            run.cacheable = False
        # Denetim Y-2: imza derleyici keşfi ve dosya stat'ı yapar (zig sondası 30 sn sürebilir);
        # olay döngüsünü kilitlemesin
        key = await asyncio.to_thread(self._cache_key, run, code, profile, provider, version)

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
            cache_flow.save_report(
                self.db,
                run,
                report,
                key=key,
                profile=profile,
                max_analyses=self.settings.storage.max_analyses,
            )
        return AnalysisTrace(report, run.finding_checks)

    def _build_provider(self, name: str) -> LLMProvider:
        return build_chain(self.settings, primary=name)

    def _use_cache(self, request: AnalysisRequest) -> bool:
        use = request.options.use_cache
        return self.settings.pipeline.use_cache if use is None else use

    async def _ingest(self, run: Run) -> NormalizedCode:
        """Doğrulama + dil tespiti iş parçacığında: regex/ayrıştırma olay döngüsünü kilitlemesin
        (Faz A1, K2)."""
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
                return await asyncio.to_thread(
                    normalize, request.code, hint, limits=self.settings.limits
                )
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
        """Soru bankası (D11). Enjekte edilmişse çağıran kendi önbelleğini yönetir (state.py);
        yoksa örnek başına bir kez diskten yüklenir (banka salt okunur)."""
        if self.questions is not None:
            return self.questions()
        if self._bank is None:
            self._bank = QuestionBank.load_all(self.settings.data)
        return self._bank

    def _rules_version(self) -> str:
        """Kural/veri sürümü (D11). Aynı analizde önbellek anahtarı ve rapor `meta`'sı aynı değeri
        kullanır; maliyet tablosu, mentor şablonları ve kontrol listeleri istek başına bir kez
        okunur (Faz J4/O3: kontrol listesi içeriği de sürüme girer)."""
        if self._rules is None:
            data = self.settings.data
            self._rules = rules_version(
                data.call_costs_file, data.mentor_templates_file, data.checklists_dir
            )
        return self._rules

    def _cache_key(
        self,
        run: Run,
        code: NormalizedCode,
        profile: MentoringProfile,
        provider: LLMProvider,
        version: str,
    ) -> str:
        """Önbellek anahtarı (gövde `cache_flow.cache_key`'de; G0)."""
        return cache_flow.cache_key(self, run, code, profile, provider, version)

    def _mode(self, request: AnalysisRequest) -> PipelineMode:
        return request.options.mode or PipelineMode(self.settings.pipeline.mode)

    def _pipeline_signature(self, run: Run, code: NormalizedCode) -> str:
        """Önbellek anahtarı için ayar imzası (gövde `cache_flow.run_signature`, G0)."""
        return cache_flow.run_signature(self, run, code)

    async def _tier1(self, code: NormalizedCode, validation: ValidationSettings) -> Tier1Result:
        """Tier 1 iş parçacığında koşar (olay döngüsünü kilitlemez); görev iptal edilirse
        derleyici süreci zaman aşımını beklemeden öldürülür (Faz 24)."""
        cancel = threading.Event()
        try:
            return await asyncio.to_thread(
                run_tier1,
                code,
                validation,
                toolchain=self.toolchain,
                runner=self.tier1_runner,
                cancel=cancel,
            )
        except asyncio.CancelledError:
            cancel.set()
            raise

    def _run_validation(self, run: Run) -> ValidationSettings:
        """Analiz başına bir kez: Tier 1 ayarı (gövde `cache_flow.validation_settings`; G0)."""
        return cache_flow.validation_settings(self, run)

    def _validation(self, request: AnalysisRequest) -> ValidationSettings:
        # İstek Tier 1'i yalnız kapatabilir; yapılandırmada kapalıysa açamaz (Faz 47, ADR-0023)
        if request.options.tier1 is not False:
            return self.settings.validation
        return self.settings.validation.model_copy(update={"tier1_enabled": False})

    async def _analyze(
        self,
        run: Run,
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
            run.cacheable = False  # denetim O-3: geçici altyapı durması kalıcılaşmasın
        tier1 = None
        if tier0.has_errors:
            timer.skip("tier1", "Tier 0 hatası")
        else:
            with timer.stage("tier1"):
                tier1 = await self._tier1(code, self._run_validation(run))
        if tier1 is not None and tier1.skip_reason in _TRANSIENT_SKIPS:
            run.cacheable = False  # zaman aşımı / araç hatası geçici: rapor önbelleğe girmez
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
        verify_provider = None
        if settings.pipeline.verify_provider:
            try:
                verify_provider = (self.provider_factory or self._build_provider)(
                    settings.pipeline.verify_provider
                )
            except ProviderError as exc:
                run.warnings.append(
                    f"Doğrulama sağlayıcısı ({settings.pipeline.verify_provider}) kurulamadı: {exc}"
                )
        llm = LLMSession(provider, settings, timer, verify_provider=verify_provider)
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
            except (
                ProviderError,
                PromptBudgetError,
                PromptConfigError,
                PromptTemplateError,
            ) as exc:
                outcome = LLMOutcome(verification=None, socratic=None)
                llm.warnings.append(
                    f"Model kullanılamadı ({exc}); rapor statik analizle hazırlandı."
                )
            except TimeoutError:
                if not deadline.expired():  # başka kaynaklı zaman aşımı bizim sınırımız değil
                    raise
        if outcome is None:
            outcome = self._timed_out(llm, limit)
        run.warnings += [*llm.warnings, *outcome.warnings]
        # G6: sağlayıcı kendi birincil adını bildirir; `getattr(provider, "chain", ...)` yok
        primary = provider.primary_name
        run.cacheable = run.cacheable and not llm.incomplete and llm.providers <= {primary}

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
    def _timed_out(llm: LLMSession, limit: float | None) -> LLMOutcome:
        """Süre sınırı sonucu (gövde `deadline.timed_out`'da; G0): Geçiş A bittiyse doğrulanmış
        bulgular korunur, sorular şablondan (Faz B, Y4); bitmediyse rapor statik analizle."""
        return deadline.timed_out(llm, limit)

    @staticmethod
    def _remaining(run: Run, limit: float | None) -> float | None:
        """Toplam süre sınırından kalan saniye (gövde `deadline.remaining`'de; G0)."""
        return deadline.remaining(run.started, limit)

    def _report(
        self,
        run: Run,
        code: NormalizedCode,
        parts: ReportParts,
        llm: LLMSession | None,
        version: str,
    ) -> AnalysisReport:
        """Raporu kurar ve maliyeti tahmin eder (gövde `assemble.assemble_with_cost`'ta; G0)."""
        return assemble_with_cost(
            settings=self.settings,
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
