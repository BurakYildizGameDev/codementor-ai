"""LLM geçişleri (mimari §4 adım 6-10, §5.6): onarım döngüsü ve sızıntıda yeniden üretim.

G0: `LLMSession` → `pipeline/llm_session.py`, doğrulama geçişi → `pipeline/verify_pass.py`.
Onarım/sokratik prompt kuran fonksiyonlar (`run_pass_a`, `_socratic`, `call_structured`) burada
kalır: testler `passes.build_repair_messages` ve `passes.build_socratic_messages`'i yamalıyor,
Python'da yama adı o modülde arayan kodu etkiler. Taşınan adlar geriye dönük uyum için yeniden
dışa aktarılır.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from pydantic import BaseModel

from codementor.models.enums import PipelineMode, has_complexity
from codementor.models.findings import issues_only
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMMarkupAnalysisOutput,
    LLMSinglePassOutput,
    LLMSocraticOutput,
)
from codementor.models.pipeline import Stage
from codementor.models.prompts import BuiltPrompt, MentoringProfile, SocraticPromptInput
from codementor.models.report import SocraticResult
from codementor.models.verification import AnalysisVerification, RepairReason, SocraticVerification
from codementor.pipeline.llm_session import LLMSession
from codementor.pipeline.stages import StaticAnalysis, VerifyArgs
from codementor.pipeline.verify_pass import VERIFY_FAILED, VERIFY_STAGES, run_pass_verify
from codementor.prompts.budget import PromptBudgetError, PromptConfigError
from codementor.prompts.builder import (
    build_analysis_messages,
    build_markup_analysis_messages,
    build_repair_messages,
    build_single_pass_messages,
    build_socratic_messages,
)
from codementor.prompts.templates import PromptTemplateError
from codementor.providers.base import ProviderError
from codementor.verify.schema_check import check_schema

__all__ = [
    "COMPLEXITY_UNVERIFIED",
    "PASS_A_FAILED",
    "SCHEMA_INVALID",
    "SCHEMA_OK",
    "SOCRATIC_FAILED",
    "VERIFY_FAILED",
    "VERIFY_STAGES",
    "LLMOutcome",
    "LLMSession",
    "PassA",
    "call_structured",
    "run_llm_passes",
    "run_pass_a",
    "run_pass_b",
    "run_pass_socratic_schema",
    "run_pass_verify",
]

# `verify_a` olayının `detail`i: eval `schema_valid_first_try/after_repair` buradan ölçer
SCHEMA_OK = "schema:ok"
SCHEMA_INVALID = "schema:invalid"
SOCRATIC_FAILED = "Mentor soruları doğrulanamadı; şablon sorular kullanıldı."


AnalysisOutput = LLMAnalysisOutput | LLMMarkupAnalysisOutput


@dataclass
class PassA:
    """Geçiş A sonucu; `verification is None` ise onarım da başarısız (zarif bozulma)."""

    output: AnalysisOutput | None
    verification: AnalysisVerification | None
    # Faz B (Y3): onarım başarısız ama şemaya uyan bir yanıt vardı; bulgular korundu, karmaşıklık
    # doğrulanamadığı için boş
    rescued: bool = False


COMPLEXITY_UNVERIFIED = (
    "Karmaşıklık analizi onarımdan sonra da doğrulanamadı; bulgular korundu, karmaşıklık "
    "gösterilmiyor."
)
PASS_A_FAILED = (
    "Model yanıtı onarımdan sonra da doğrulanamadı; rapor yalnızca statik analizle hazırlandı."
)


def _repair_cause(reasons: list[RepairReason]) -> RepairReason:
    """Onarım prompt'unun giriş cümlesi (D1): şema dışındaki neden varsa o anlatılır."""
    return next((reason for reason in reasons if reason != "schema"), "schema")


async def run_pass_a[M: BaseModel](
    llm: LLMSession,
    built: BuiltPrompt,
    model: type[M],
    extract: Callable[[M], AnalysisOutput],
    verify: VerifyArgs,
    llm_stage: Stage = "llm_a",
    verify_stage: Stage = "verify_a",
) -> tuple[M | None, PassA]:
    """Çağır → şema → doğrula; hata varsa `max_repair_attempts` kez onarım iste.

    `model` Geçiş A şeması ya da tek geçiş şeması; `extract` ondan analiz kısmını alır.
    Onarım tükenir ya da onarım çağrısı sağlayıcı hatası verirse şemaya uyan son yanıtın
    bulguları korunur (Faz B, Y3); hiç uyan yanıt yoksa zarif bozulma.
    """
    result = await llm.call(llm_stage, built, model)
    schema_first_try: bool | None = None
    last_valid: tuple[M, AnalysisOutput, AnalysisVerification] | None = None
    for attempt in range(llm.settings.pipeline.max_repair_attempts + 1):
        with llm.timer.stage(verify_stage):
            parsed, check = check_schema(model, parsed=result.parsed, raw_text=result.raw_text)
            if schema_first_try is None:
                schema_first_try = check.ok
            llm.timer.note(verify_stage, SCHEMA_OK if check.ok else SCHEMA_INVALID)
            errors = check.errors
            cause: RepairReason = "schema"
            verification: AnalysisVerification | None = None
            analysis: AnalysisOutput | None = None
            if parsed is not None:
                analysis = extract(parsed)
                verification = verify.analysis(analysis, schema_first_try)
                if verification.repair is not None:
                    errors = verification.repair.errors
                    cause = _repair_cause(verification.repair.reasons)  # D1: doğru giriş cümlesi
                last_valid = (parsed, analysis, verification)
        if not errors:
            return parsed, PassA(output=analysis, verification=verification)
        if attempt == llm.settings.pipeline.max_repair_attempts:
            break
        llm.repair_attempts += 1
        if last_valid is not None:
            # denetim: onarım sürerken süre dolarsa da doğrulanmış bulgular korunsun
            llm.checkpoint = _rescued(last_valid[2])
            llm.checkpoint_verified = not llm.settings.pipeline.verify_findings
        try:
            built = build_repair_messages(
                built,
                raw_text=result.raw_text,
                errors=errors,
                cause=cause,
                settings=llm.settings,
            )
            result = await llm.call(llm_stage, built, model)
        except (ProviderError, PromptBudgetError):
            if last_valid is None:
                raise
            break
    if last_valid is None:
        llm.warnings.append(PASS_A_FAILED)
        return None, PassA(output=None, verification=None)
    # Şemaya uyan yanıtta onarım nedeni yalnız karmaşıklıktır; `_complexity_result` onu zaten
    # boş bırakır, bulgular doğrulanmıştır
    parsed_valid, analysis_valid, verification_valid = last_valid
    llm.fail_part(COMPLEXITY_UNVERIFIED)
    kept = _rescued(verification_valid)
    return parsed_valid, PassA(output=analysis_valid, verification=kept, rescued=True)


def _rescued(verification: AnalysisVerification) -> AnalysisVerification:
    """Onarımı tamamlanamayan geçerli yanıt: bulgular korunur, karmaşıklık boş (Y3)."""
    return verification.model_copy(update={"repair": None, "complexity": None})


async def run_pass_b(
    llm: LLMSession,
    built: BuiltPrompt,
    verify: VerifyArgs,
    hint_level: int,
    first: LLMSocraticOutput | None = None,
    *,
    name_concept: bool,
    rebuild: Callable[[bool], BuiltPrompt] | None = None,
) -> SocraticVerification | None:
    """Sokratik geçiş: şema onarımı + sızıntıda 1 kez yeniden üretim. `first` verilirse
    (tek geçiş) ilk yanıt odur. Sonuç None ise şablona düşülür.

    `rebuild` (D7): `True` ile çağrıldığında yeniden üretim prompt'unu (soyut soru notuyla)
    yeniden kurar; verilmezse aynı prompt yeniden gönderilir.
    """
    output, prompt = first, built
    for regenerated in (False, True):
        if output is None:
            if regenerated and rebuild is not None:
                prompt = rebuild(True)
            parsed, _ = await run_pass_socratic_schema(llm, prompt)
            if parsed is None:
                return None
            output = parsed
        with llm.timer.stage("verify_b"):
            checked = verify.socratic(output, hint_level, regenerated, name_concept)
        if checked.decision.action != "regenerate":
            return checked
        output = None
    return None


async def call_structured[M: BaseModel](
    llm: LLMSession, stage: Stage, built: BuiltPrompt, model: type[M]
) -> tuple[M | None, BuiltPrompt]:
    """Yanıtı şemaya uydur (`max_repair_attempts` kez onarımlı); olmazsa None."""
    result = await llm.call(stage, built, model)
    for attempt in range(llm.settings.pipeline.max_repair_attempts + 1):
        parsed, check = check_schema(model, parsed=result.parsed, raw_text=result.raw_text)
        if parsed is not None:
            return parsed, built
        if attempt == llm.settings.pipeline.max_repair_attempts:
            break
        llm.repair_attempts += 1
        built = build_repair_messages(
            built, raw_text=result.raw_text, errors=check.errors, settings=llm.settings
        )
        result = await llm.call(stage, built, model)
    return None, built


async def run_pass_socratic_schema(
    llm: LLMSession, built: BuiltPrompt
) -> tuple[LLMSocraticOutput | None, BuiltPrompt]:
    """Sokratik yanıtı şemaya uydur (onarımlı)."""
    return await call_structured(llm, "llm_b", built, LLMSocraticOutput)


@dataclass
class LLMOutcome:
    """İki geçişin sonucu; `verification is None` → zarif bozulma, `socratic is None` → şablon."""

    verification: AnalysisVerification | None
    socratic: SocraticResult | None
    warnings: list[str] = field(default_factory=list)


def _identity(output: AnalysisOutput) -> AnalysisOutput:
    return output


def _analysis_part(output: LLMSinglePassOutput) -> LLMAnalysisOutput:
    return output.analysis


async def run_llm_passes(
    llm: LLMSession,
    static: StaticAnalysis,
    verify: VerifyArgs,
    profile: MentoringProfile,
    *,
    mode: PipelineMode,
    provider: str | None,
) -> LLMOutcome:
    """Geçiş A (+onarım) ve B (+sızıntıda yeniden üretim); `single_pass`'ta ikisi tek çağrıda,
    sızıntı olursa yeniden üretim ayrı Geçiş B ile yapılır."""
    timer, settings = llm.timer, llm.settings
    attempt = static.facts_input.attempt
    first: LLMSocraticOutput | None = None
    markup = not has_complexity(verify.code.language)
    if markup:  # HTML/CSS: karmaşıklıksız şema yalnızca iki geçişte (ADR-0015)
        mode = PipelineMode.TWO_PASS
    with timer.stage("prompt_a"):
        if markup:
            built = build_markup_analysis_messages(
                static.facts_input, settings=settings, provider=provider
            )
        elif mode is PipelineMode.SINGLE_PASS:
            built = build_single_pass_messages(
                static.facts_input, settings=settings, provider=provider
            )
        else:
            built = build_analysis_messages(
                static.facts_input, settings=settings, provider=provider
            )
    if mode is PipelineMode.SINGLE_PASS:
        single, pass_a = await run_pass_a(llm, built, LLMSinglePassOutput, _analysis_part, verify)
        first = single.socratic if single is not None else None
    elif markup:
        _, pass_a = await run_pass_a(llm, built, LLMMarkupAnalysisOutput, _identity, verify)
    else:
        _, pass_a = await run_pass_a(llm, built, LLMAnalysisOutput, _identity, verify)
    if pass_a.verification is None or pass_a.output is None:
        for stage in (*VERIFY_STAGES, "prompt_b", "llm_b", "verify_b"):
            timer.skip(stage, "Geçiş A doğrulanamadı")
        return LLMOutcome(verification=None, socratic=None)
    verification = pass_a.verification
    # O2 (§5.4.2): K5 bulgu attıysa ya da karmaşıklık kurtarıldıysa tek geçişin soruları
    # doğrulanmamış içeriğe dayanıyor olabilir: ayrı Geçiş B
    if pass_a.rescued or verification.evidence_ratio < 1:
        first = None
    llm.checkpoint = verification
    if settings.pipeline.verify_findings:
        llm.checkpoint_verified = False
        verification, dropped = await run_pass_verify(llm, verification, verify, provider)
        llm.checkpoint, llm.checkpoint_verified = verification, True
        if dropped:  # tek geçişin soruları atılan bulguya dayanıyor olabilir: ayrı Geçiş B
            first = None
    else:
        for stage in VERIFY_STAGES:
            timer.skip(stage, "Bulgu doğrulama kapalı")
    # Y4: Geçiş B'nin hatası doğrulanmış bulguları silmez; sorular şablona düşer
    try:
        checked = await _socratic(
            llm, verify, verification, pass_a, profile, attempt, first, provider
        )
    except (ProviderError, PromptBudgetError, PromptConfigError, PromptTemplateError) as exc:
        llm.incomplete = True
        warning = f"Mentor soruları üretilemedi ({exc}); şablon sorular kullanıldı."
        return LLMOutcome(verification, None, [warning])
    if checked is None:
        llm.incomplete = True
        return LLMOutcome(verification, None, [SOCRATIC_FAILED])
    if checked.result is None:  # denetim O-2: sızıntı yüzünden tüm sorular atıldı → şablon
        llm.incomplete = True
    return LLMOutcome(verification, checked.result, list(checked.warnings))


async def _socratic(
    llm: LLMSession,
    verify: VerifyArgs,
    verification: AnalysisVerification,
    pass_a: PassA,
    profile: MentoringProfile,
    attempt: int,
    first: LLMSocraticOutput | None,
    provider: str | None,
) -> SocraticVerification | None:
    """Geçiş B: prompt + çağrı. Karmaşıklık yalnız doğrulandıysa prompt'a girer (kurtarılan
    çelişkili karmaşıklık soruya taşınmasın)."""
    complexity = (
        pass_a.output.complexity
        if isinstance(pass_a.output, LLMAnalysisOutput) and verification.complexity is not None
        else None
    )
    prompt = SocraticPromptInput(
        code=verify.code,
        question=verify.question,
        findings=issues_only(verification.findings),
        complexity=complexity,
        attempt=attempt,
    )

    def rebuild(abstract: bool) -> BuiltPrompt:
        """D7: sızıntıdan sonraki yeniden üretim için prompt (soyut soru notuyla).

        Her kurulum `prompt_b` süresi ölçülür; yeniden üretimde aynı aşama ikinci kez
        ölçülür (`stage_latency_ms` son pencereyi taşır).
        """
        with llm.timer.stage("prompt_b"):
            return build_socratic_messages(
                prompt, settings=llm.settings, provider=provider, abstract=abstract
            )

    initial = rebuild(False)
    return await run_pass_b(
        llm,
        initial,
        verify,
        profile.hint_level,
        first,
        name_concept=profile.name_concept,
        rebuild=rebuild,
    )
