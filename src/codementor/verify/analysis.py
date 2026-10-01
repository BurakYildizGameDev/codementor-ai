"""K5 birleştirici: Geçiş A ve B çıktılarını §5.6 kontrollerinden sırayla geçirir.

Saf fonksiyonlar; LLM çağırmaz, onarım/yeniden üretim kararını döndürür (Faz 10 uygular).
"""

from __future__ import annotations

from typing import Literal

from codementor.config import VerifySettings, get_settings
from codementor.models.bigo import parse_bigo
from codementor.models.enums import FindingSource
from codementor.models.facts import ComplexityHint
from codementor.models.findings import Finding
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMFinding,
    LLMMarkupAnalysisOutput,
    LLMSocraticOutput,
)
from codementor.models.prompts import QuestionContext
from codementor.models.questions import ExpectedComplexity
from codementor.models.report import ComplexityResult, SocraticResult
from codementor.models.request import NormalizedCode
from codementor.models.verification import (
    AgreementState,
    AnalysisVerification,
    CommonIdentifiers,
    ComplexityCheck,
    RepairReason,
    RepairRequest,
    SocraticVerification,
)
from codementor.verify.complexity import check_complexity
from codementor.verify.confidence import (
    LLM_EXACT_CONFIDENCE,
    LLM_SHIFTED_CONFIDENCE,
    analysis_confidence,
    evidence_ratio,
)
from codementor.verify.leak_guard import check_leaks, decide_leak_action
from codementor.verify.lines import check_line_range, match_evidence
from codementor.verify.merge import merge_findings

ReportAgreement = Literal["agrees", "conflicts", "no_hint"]
LeakStatus = Literal["passed", "regenerated", "dropped_questions"]
_AGREEMENT: dict[AgreementState, ReportAgreement] = {
    "agrees": "agrees",
    "justified_conflict": "conflicts",
    "no_hint": "no_hint",
}


def _to_finding(
    finding: LLMFinding, line_start: int, line_end: int | None, shifted: bool
) -> Finding:
    return Finding(
        id="F-000",  # merge_findings numaralar
        rule_id=None,
        category=finding.category,
        severity=finding.severity,
        line_start=line_start,
        line_end=line_end,
        evidence=finding.evidence,
        description=finding.description,
        source=FindingSource.LLM,
        confidence=LLM_SHIFTED_CONFIDENCE if shifted else LLM_EXACT_CONFIDENCE,
    )


def verify_findings(
    findings: list[LLMFinding], lines: list[str], window: int
) -> tuple[list[Finding], list[str]]:
    """Satır aralığı + kanıt kontrolü; geçemeyen bulgu atılır ve Türkçe uyarı yazılır."""
    kept: list[Finding] = []
    warnings: list[str] = []
    for finding in findings:
        if not check_line_range(finding.line_start, finding.line_end, len(lines)):
            warnings.append(
                f"Model {finding.line_start}. satırda bir sorun bildirdi ama kod "
                f"{len(lines)} satır; bulgu atıldı."
            )
            continue
        match = match_evidence(
            finding.evidence, finding.line_start, finding.line_end, lines, window
        )
        if not match.found or match.line_start is None:
            warnings.append(
                f"Modelin {finding.line_start}. satır için gösterdiği kanıt kodda bulunamadı; "
                "bulgu atıldı."
            )
            continue
        kept.append(_to_finding(finding, match.line_start, match.line_end, match.shifted))
    return kept, warnings


def _repair(check: ComplexityCheck) -> RepairRequest | None:
    if not check.needs_repair:
        return None
    reasons: list[RepairReason] = []
    if check.time is None or check.space is None:
        reasons.append("complexity_unparsable")
    if check.state == "unjustified_conflict":
        reasons.append("unjustified_conflict")
    return RepairRequest(reasons=reasons, errors=check.errors)


def _complexity_result(
    output: LLMAnalysisOutput,
    check: ComplexityCheck,
    hint: ComplexityHint | None,
    confidence: float,
) -> ComplexityResult | None:
    if check.time is None or check.space is None or check.state == "unjustified_conflict":
        return None
    return ComplexityResult(
        time_complexity=check.time,
        space_complexity=check.space,
        display_time=parse_bigo(check.time).display,
        reasoning_steps=output.complexity.reasoning_steps,
        is_optimal=check.is_optimal,
        optimal_time_target=check.optimal_target,
        static_hint=hint.value if hint else None,
        agreement=_AGREEMENT[check.state],
        confidence=confidence,
    )


def verify_analysis(
    output: LLMAnalysisOutput,
    *,
    code: NormalizedCode,
    static_findings: list[Finding],
    hint: ComplexityHint | None,
    expected: ExpectedComplexity | None,
    schema_first_try: bool,
    settings: VerifySettings | None = None,
) -> AnalysisVerification:
    """Geçiş A: bulguları doğrula ve statiklerle birleştir, karmaşıklığı uzlaştır, güveni hesapla.

    `repair` doluysa Faz 10 modelden bir kez düzeltme ister; karmaşıklık o zamana dek `None`.
    """
    settings = settings or get_settings().verify
    verified, warnings = verify_findings(
        output.additional_findings, code.lines, settings.evidence_window
    )
    ratio = evidence_ratio(len(verified), len(output.additional_findings))
    check = check_complexity(output.complexity, hint, expected)
    confidence = analysis_confidence(schema_first_try, check.state, ratio)
    return AnalysisVerification(
        findings=merge_findings(static_findings, verified),
        complexity=_complexity_result(output, check, hint, confidence),
        confidence=confidence,
        evidence_ratio=ratio,
        warnings=warnings,
        repair=_repair(check),
    )


def verify_markup_analysis(
    output: LLMMarkupAnalysisOutput,
    *,
    code: NormalizedCode,
    static_findings: list[Finding],
    schema_first_try: bool,
    settings: VerifySettings | None = None,
) -> AnalysisVerification:
    """HTML/CSS Geçiş A (ADR-0015): bulgular satır kanıtıyla doğrulanır; karmaşıklık yok."""
    settings = settings or get_settings().verify
    verified, warnings = verify_findings(
        output.additional_findings, code.lines, settings.evidence_window
    )
    ratio = evidence_ratio(len(verified), len(output.additional_findings))
    return AnalysisVerification(
        findings=merge_findings(static_findings, verified),
        complexity=None,
        confidence=analysis_confidence(schema_first_try, "no_hint", ratio),
        evidence_ratio=ratio,
        warnings=warnings,
    )


def question_text(question: QuestionContext | None) -> str:
    """Sızıntı kontrolünde serbest sayılan soru metni (başlık, açıklama, kısıtlar)."""
    if question is None:
        return ""
    return "\n".join([question.title, question.prompt, *question.constraints])


def verify_socratic(
    output: LLMSocraticOutput,
    *,
    code: NormalizedCode,
    hint_level: int,
    question: QuestionContext | None,
    reference: str | None,
    regenerated: bool,
    settings: VerifySettings | None = None,
    common: CommonIdentifiers | None = None,
) -> SocraticVerification:
    """Geçiş B: sızıntı kontrolü ve kararı. `regenerate` ise sonuç yok (Faz 10 yeniden üretir)."""
    check = check_leaks(
        output.guiding_questions,
        output.next_step_hint,
        student_code=code.text,
        language=code.language,
        engine=code.engine,
        reference=reference,
        question_text=question_text(question),
        settings=settings,
        common=common,
    )
    decision = decide_leak_action(
        output.guiding_questions, output.next_step_hint, check, regenerated=regenerated
    )
    if decision.action == "regenerate":
        return SocraticVerification(decision=decision, result=None)
    warnings: list[str] = []
    if decision.action == "dropped_questions":
        warnings.append("Bazı mentor soruları çözümü ele verdiği için çıkarıldı.")
    if not decision.guiding_questions:
        warnings.append("Mentor sorularının tümü çözümü ele verdiği için çıkarıldı.")
        return SocraticVerification(decision=decision, result=None, warnings=warnings)
    status: LeakStatus = (
        "dropped_questions"
        if decision.action == "dropped_questions"
        else "regenerated"
        if regenerated
        else "passed"
    )
    result = SocraticResult(
        key_flaw_concept=output.key_flaw_concept,
        hint_level=hint_level,
        guiding_questions=decision.guiding_questions,
        next_step_hint=decision.next_step_hint,
        leak_check=status,
    )
    return SocraticVerification(decision=decision, result=result, warnings=warnings)
