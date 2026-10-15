"""Doğrulama geçişi (Faz 35, ADR-0019): LLM bulguları kanıtlatılır, kanıtlanamayan atılır.

G0'da `passes.py`'den ayrıldı (dosya 400 satırın altına insin); `passes.py` `VERIFY_STAGES`,
`VERIFY_FAILED` ve `run_pass_verify` adlarını yeniden dışa aktarır.
"""

from __future__ import annotations

from codementor.models.llm_output import LLMVerifyOutput
from codementor.models.pipeline import Stage
from codementor.models.prompts import VerifyPromptInput
from codementor.models.verification import AnalysisVerification
from codementor.pipeline.llm_session import LLMSession
from codementor.pipeline.stages import VerifyArgs
from codementor.prompts.budget import PromptBudgetError
from codementor.prompts.builder import build_verify_messages
from codementor.prompts.templates import PromptTemplateError
from codementor.providers.base import ProviderError
from codementor.verify.proof import apply_verdicts, redact_reasons, verify_targets

VERIFY_STAGES: tuple[Stage, ...] = ("prompt_v", "llm_v", "verify_v")
VERIFY_FAILED = "Bulgu doğrulama geçişi tamamlanamadı; bulgular olduğu gibi bırakıldı."


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
    # `call_structured` onarım prompt'unu `passes.py`'de kurar (testler oradaki
    # `build_repair_messages`'i yamalıyor) ve o modül bu modülü içe aktardığı için döngü
    # olmasın diye çağrı anında alınır (G0).
    from codementor.pipeline.passes import call_structured

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
        parsed = await call_structured(llm, "llm_v", built, LLMVerifyOutput)
    except (ProviderError, PromptBudgetError, PromptTemplateError) as exc:
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
