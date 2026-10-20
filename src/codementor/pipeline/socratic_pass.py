"""Sokratik mentorluk geçişi ve kalite kapısı (Faz I / İş 11, ADR-0031).

G0/Faz I: `passes.py` 400 satır sınırında kalsın diye ayrıldı.
"""

from __future__ import annotations

from codementor.models.findings import issues_only
from codementor.models.llm_output import LLMAnalysisOutput, LLMSocraticOutput
from codementor.models.prompts import BuiltPrompt, MentoringProfile, SocraticPromptInput
from codementor.models.verification import AnalysisVerification, SocraticVerification
from codementor.pipeline.llm_session import LLMSession
from codementor.pipeline.stages import VerifyArgs
from codementor.verify.socratic_gate import SocraticGateResult, evaluate_socratic_gate


async def run_pass_socratic(
    llm: LLMSession,
    verify: VerifyArgs,
    verification: AnalysisVerification,
    pass_a_output: object | None,
    profile: MentoringProfile,
    attempt: int,
    first: LLMSocraticOutput | None,
    provider: str | None,
) -> SocraticVerification | None:
    """Geçiş B: prompt + çağrı + Sokratik kalite kapısı denetimi."""
    import codementor.pipeline.passes as passes_mod

    complexity = (
        pass_a_output.complexity
        if isinstance(pass_a_output, LLMAnalysisOutput) and verification.complexity is not None
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
        with llm.timer.stage("prompt_b"):
            return passes_mod.build_socratic_messages(
                prompt, settings=llm.settings, provider=provider, abstract=abstract
            )

    initial = rebuild(False)
    checked = await passes_mod.run_pass_b(
        llm,
        initial,
        verify,
        profile.hint_level,
        first,
        name_concept=profile.name_concept,
        rebuild=rebuild,
    )
    if checked is not None and checked.result is not None:
        gate = evaluate_socratic_gate(
            questions=checked.result.guiding_questions,
            next_step_hint=checked.result.next_step_hint,
            code=verify.code.text,
            hint_level=profile.hint_level,
            model_profile=llm.settings.pipeline.model_profile,
        )
        return apply_gate(checked, gate)
    return checked


def apply_gate(checked: SocraticVerification, gate: SocraticGateResult) -> SocraticVerification:
    """Kapı kararını uygular: geçemediyse sonuç düşer (şablona dönülür), geçtiyse elenen sorular
    çıkarılır. Kapı uyarıları her durumda rapora taşınır — soru listesi değişmese de."""
    if not gate.passed:
        result = None
    elif checked.result is not None and gate.filtered_questions != checked.result.guiding_questions:
        result = checked.result.model_copy(update={"guiding_questions": gate.filtered_questions})
    else:
        result = checked.result
    if result is checked.result and not gate.warnings:
        return checked
    return SocraticVerification(
        decision=checked.decision, result=result, warnings=[*checked.warnings, *gate.warnings]
    )
