"""LLM geçişleri (mimari §4 adım 6-10, §5.6): onarım döngüsü ve sızıntıda yeniden üretim."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from pydantic import BaseModel

from codementor.config import Settings
from codementor.models.enums import PipelineMode, has_complexity
from codementor.models.findings import issues_only
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMMarkupAnalysisOutput,
    LLMSinglePassOutput,
    LLMSocraticOutput,
    LLMVerifyOutput,
)
from codementor.models.pipeline import Stage
from codementor.models.prompts import (
    BuiltPrompt,
    MentoringProfile,
    SocraticPromptInput,
    VerifyPromptInput,
)
from codementor.models.provider import GenerationOptions, ProviderResult, TokenUsage
from codementor.models.report import SocraticResult, TokenSplit
from codementor.models.verification import AnalysisVerification, SocraticVerification
from codementor.pipeline.events import StageTimer
from codementor.pipeline.stages import StaticAnalysis, VerifyArgs
from codementor.prompts.budget import (
    PromptBudgetError,
    PromptConfigError,
    estimate_messages,
    estimate_tokens,
)
from codementor.prompts.builder import (
    build_analysis_messages,
    build_markup_analysis_messages,
    build_repair_messages,
    build_single_pass_messages,
    build_socratic_messages,
    build_verify_messages,
)
from codementor.providers.base import LLMProvider, ProviderError
from codementor.verify.proof import apply_verdicts, redact_reasons, verify_targets
from codementor.verify.schema_check import check_schema

# `verify_a` olayının `detail`i: eval `schema_valid_first_try/after_repair` buradan ölçer
SCHEMA_OK = "schema:ok"
SCHEMA_INVALID = "schema:invalid"
VERIFY_STAGES: tuple[Stage, ...] = ("prompt_v", "llm_v", "verify_v")
VERIFY_FAILED = "Bulgu doğrulama geçişi tamamlanamadı; bulgular olduğu gibi bırakıldı."
SOCRATIC_FAILED = "Mentor soruları doğrulanamadı; şablon sorular kullanıldı."


@dataclass
class LLMSession:
    """Bir analizdeki tüm LLM çağrıları: token, onarım ve sağlayıcı uyarıları birikir."""

    provider: LLMProvider
    settings: Settings
    timer: StageTimer
    tokens_in: int = 0
    tokens_out: int = 0
    repair_attempts: int = 0
    warnings: list[str] = field(default_factory=list)
    provider_name: str | None = None
    model: str | None = None
    usage_estimated: bool = False
    # Faz B: yanıt veren sağlayıcılar (fallback tespiti), LLM'in bir kısmı başarısız mı (rapor
    # önbelleğe alınmaz) ve süre sınırında kullanılacak son doğrulanmış Geçiş A sonucu
    providers: set[str] = field(default_factory=set)
    incomplete: bool = False
    checkpoint: AnalysisVerification | None = None
    checkpoint_verified: bool = True
    stage_tokens: dict[str, TokenSplit] = field(default_factory=dict)  # Faz K

    def fail_part(self, warning: str) -> None:
        """LLM'in bir kısmı başarısız: uyarı yazılır, rapor önbelleğe alınmaz."""
        self.warnings.append(warning)
        self.incomplete = True

    async def call(
        self, stage: Stage, built: BuiltPrompt, model: type[BaseModel]
    ) -> ProviderResult:
        with self.timer.stage(stage):
            result = await self.provider.generate_structured(
                built.messages, model, GenerationOptions()
            )
            usage = self._usage(built, result)
            self.tokens_in += usage.input_tokens
            self.tokens_out += usage.output_tokens
            split = self.stage_tokens.get(stage, TokenSplit(input=0, output=0))
            self.stage_tokens[stage] = TokenSplit(
                input=split.input + usage.input_tokens, output=split.output + usage.output_tokens
            )
            self.timer.add_tokens(stage, usage.input_tokens + usage.output_tokens)
        self.warnings.extend(result.warnings)
        self.provider_name, self.model = result.provider, result.model
        self.providers.add(result.provider)
        return result

    def _usage(self, built: BuiltPrompt, result: ProviderResult) -> TokenUsage:
        """Sağlayıcı token bildirmediyse yaklaşık sayım (mimari §13, `usage_estimated`)."""
        usage = result.usage
        if usage.input_tokens or usage.output_tokens:
            self.usage_estimated |= usage.estimated
            return usage
        self.usage_estimated = True
        return TokenUsage(
            input_tokens=estimate_messages(built.messages),
            output_tokens=estimate_tokens(result.raw_text),
            estimated=True,
        )


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
            verification: AnalysisVerification | None = None
            analysis: AnalysisOutput | None = None
            if parsed is not None:
                analysis = extract(parsed)
                verification = verify.analysis(analysis, schema_first_try)
                errors = verification.repair.errors if verification.repair else []
                last_valid = (parsed, analysis, verification)
        if not errors:
            return parsed, PassA(output=analysis, verification=verification)
        if attempt == llm.settings.pipeline.max_repair_attempts:
            break
        llm.repair_attempts += 1
        built = build_repair_messages(
            built, raw_text=result.raw_text, errors=errors, settings=llm.settings
        )
        try:
            result = await llm.call(llm_stage, built, model)
        except ProviderError:
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
    kept = verification_valid.model_copy(update={"repair": None, "complexity": None})
    return parsed_valid, PassA(output=analysis_valid, verification=kept, rescued=True)


async def run_pass_b(
    llm: LLMSession,
    built: BuiltPrompt,
    verify: VerifyArgs,
    hint_level: int,
    first: LLMSocraticOutput | None = None,
) -> SocraticVerification | None:
    """Sokratik geçiş: şema onarımı + sızıntıda 1 kez yeniden üretim. `first` verilirse
    (tek geçiş) ilk yanıt odur. Sonuç None ise şablona düşülür."""
    output = first
    for regenerated in (False, True):
        if output is None:
            parsed, _ = await run_pass_socratic_schema(llm, built)
            if parsed is None:
                return None
            output = parsed
        with llm.timer.stage("verify_b"):
            checked = verify.socratic(output, hint_level, regenerated)
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


async def run_pass_verify(
    llm: LLMSession,
    verification: AnalysisVerification,
    verify: VerifyArgs,
    provider: str | None,
) -> tuple[AnalysisVerification, int]:
    """Doğrulama geçişi (Faz 35, ADR-0019): LLM bulgularını kanıtlatır, kanıtlanamayanı atar.

    Dönen sayı atılan bulgu sayısıdır. Sağlayıcı/bütçe hatası ya da onarımdan sonra da bozuk
    şema bulguları değiştirmez; uyarı yazılır (güvenli geri dönüş).
    """
    targets = verify_targets(verification.findings)
    if not targets:
        for stage in VERIFY_STAGES:
            llm.timer.skip(stage, "Doğrulanacak model bulgusu yok")
        return verification, 0
    try:
        with llm.timer.stage("prompt_v"):
            built = build_verify_messages(
                VerifyPromptInput(code=verify.code, question=verify.question, findings=targets),
                settings=llm.settings,
                provider=provider,
            )
        parsed, _ = await call_structured(llm, "llm_v", built, LLMVerifyOutput)
    except (ProviderError, PromptBudgetError) as exc:
        llm.fail_part(f"{VERIFY_FAILED} ({exc})")
        return verification, 0
    if parsed is None:
        llm.fail_part(VERIFY_FAILED)
        return verification, 0
    with llm.timer.stage("verify_v"):
        result = apply_verdicts(verification.findings, parsed)
        leaks = verify.leaks([c.reason for c in result.checks])
        leaky = {v.index for v in leaks.violations if v.index is not None}
        llm.timer.note("verify_v", f"dropped:{result.dropped}/{len(targets)}")
    updated = verification.model_copy(
        update={
            "findings": result.findings,
            "finding_checks": redact_reasons(result.checks, leaky),
            "warnings": [*verification.warnings, *result.warnings],
        }
    )
    return updated, result.dropped


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
    except (ProviderError, PromptBudgetError, PromptConfigError) as exc:
        llm.incomplete = True
        warning = f"Mentor soruları üretilemedi ({exc}); şablon sorular kullanıldı."
        return LLMOutcome(verification, None, [warning])
    if checked is None:
        llm.incomplete = True
        return LLMOutcome(verification, None, [SOCRATIC_FAILED])
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
    with llm.timer.stage("prompt_b"):
        built_b = build_socratic_messages(
            SocraticPromptInput(
                code=verify.code,
                question=verify.question,
                findings=issues_only(verification.findings),
                complexity=complexity,
                attempt=attempt,
            ),
            settings=llm.settings,
            provider=provider,
        )
    return await run_pass_b(llm, built_b, verify, profile.hint_level, first)
