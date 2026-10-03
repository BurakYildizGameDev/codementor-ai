"""Pipeline aşamaları (mimari §4). Orkestratör bunları sırayla çağırır; iş mantığı katmanlarda.

LLM geçişleri §5.6 kararlarını uygular: şema/karmaşıklık hatasında en fazla
`pipeline.max_repair_attempts` onarım, sızıntıda 1 kez yeniden üretim.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from codementor.analysis.call_costs import load_call_costs
from codementor.analysis.complexity_hint import compute_hint, function_hints
from codementor.analysis.extractor import extract_facts
from codementor.config import Settings
from codementor.log import get_logger
from codementor.models.bigo import parse_bigo
from codementor.models.enums import FindingSource, has_complexity
from codementor.models.facts import CodeFacts, ComplexityHint
from codementor.models.findings import Finding
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMMarkupAnalysisOutput,
    LLMSocraticOutput,
)
from codementor.models.pipeline import MentorTemplates
from codementor.models.prompts import AnalysisPromptInput, QuestionContext
from codementor.models.questions import ChecklistItem, Question
from codementor.models.report import ComplexityResult
from codementor.models.request import NormalizedCode
from codementor.models.verification import (
    AnalysisVerification,
    LeakCheck,
    SocraticVerification,
)
from codementor.paths import resource_root
from codementor.pipeline.events import StageTimer
from codementor.pipeline.templates import fallback_description
from codementor.questions.checklists import Checklists
from codementor.questions.reference import (
    ReferenceError,
    resolve_reference,
)
from codementor.rules.engine import run_rules
from codementor.verify.analysis import (
    question_text,
    verify_analysis,
    verify_markup_analysis,
    verify_socratic,
)
from codementor.verify.complexity import is_optimal
from codementor.verify.leak_guard import check_leaks

log = get_logger("codementor.pipeline")
_HINT_CONFIDENCE = {"low": 0.3, "medium": 0.5, "high": 0.7}
UNKNOWN_SPACE = "?"
# Sızıntı korumasının temizleme uyarıları; eval `guard_interventions` bunları sayar.
SCRUB_WARNING_COMPLEXITY = "Karmaşıklık gerekçesinden çözümü ele veren adımlar çıkarıldı."
SCRUB_WARNING_FINDINGS = "Bazı bulgu açıklamaları çözümü ele verdiği için sadeleştirildi."


@dataclass
class StaticAnalysis:
    """K2 çıktısı: olgular, ipucu, kural bulguları, kontrol listesi."""

    hint: ComplexityHint | None
    function_hints: list[ComplexityHint]
    findings: list[Finding]
    checklist: list[ChecklistItem]
    warnings: list[str]
    facts_input: AnalysisPromptInput


def run_static(
    code: NormalizedCode,
    question: QuestionContext | None,
    concept_tags: list[str],
    settings: Settings,
    timer: StageTimer,
    attempt: int,
) -> StaticAnalysis:
    """Olgu çıkarımı + kurallar (`facts`, `rules` aşamaları)."""
    with timer.stage("facts"):
        if has_complexity(code.language):
            facts = extract_facts(code, costs=load_call_costs(settings.data.call_costs_file))
        else:  # HTML/CSS: olgu ve Big-O yok (ADR-0015)
            facts = CodeFacts()
        hint = compute_hint(facts) if facts.functions or facts.loops or facts.recursion else None
        hints = list(function_hints(facts).values())
    with timer.stage("rules"):
        rules = run_rules(code, facts, disabled=settings.rules.disabled)
        checklist = Checklists.load(settings.data.checklists_dir).select_items(
            code.language, code.engine, concept_tags, settings.prompts.max_checklist_items
        )
    shown = settings.prompts.include_facts  # §14.4 ablasyonu
    inp = AnalysisPromptInput(
        code=code,
        question=question,
        facts=facts if shown else CodeFacts(),
        hint=hint if shown else None,
        function_hints=hints if shown else [],
        static_findings=rules.findings,
        checklist=checklist,
        attempt=attempt,
    )
    return StaticAnalysis(
        hint=hint,
        function_hints=hints,
        findings=rules.findings,
        checklist=checklist,
        warnings=[*facts.warnings, *rules.warnings],
        facts_input=inp,
    )


def load_reference(
    question: Question | None, root: Path | None = None
) -> tuple[str | None, list[str]]:
    """Sorunun referans çözümü (yalnızca sızıntı kontrolü için; prompt'a hiç girmez, §12).

    Yol kaynak köküne (`root`, varsayılan `resource_root()`) göre çözülür, çalışma dizinine
    göre değil. Sembolik bağlantılar çözüldükten sonra dosya `private/` dizininin (o da
    çözülmüş haliyle; başka diske bağlanmış olabilir) dışına çıkıyorsa okunmaz (§7.1).
    Hiçbir durumda istisna fırlatmaz.
    """
    if question is None or not question.reference_solution_path:
        return None, []
    try:
        path = resolve_reference(
            question.reference_solution_path, root if root is not None else resource_root()
        )
        return path.read_text(encoding="utf-8"), []
    except (OSError, UnicodeDecodeError) as exc:
        # öğrenciye iç yapı (referans çözümün varlığı) söylenmez; operatör log'dan görür.
        # Dağıtımda `private/` yoktur: dosyanın hiç olmaması her analizde WARNING değil (Faz 31)
        missing = isinstance(exc, ReferenceError) and exc.missing
        (log.debug if missing else log.warning)(
            "reference_solution_unreadable", question=question.id, error=type(exc).__name__
        )
        return None, []


@dataclass
class VerifyArgs:
    """Doğrulayıcıların sabit girdileri."""

    code: NormalizedCode
    static_findings: list[Finding]
    hint: ComplexityHint | None
    question: QuestionContext | None
    reference: str | None
    settings: Settings

    def analysis(
        self, output: LLMAnalysisOutput | LLMMarkupAnalysisOutput, schema_first_try: bool
    ) -> AnalysisVerification:
        if isinstance(output, LLMMarkupAnalysisOutput):
            return verify_markup_analysis(
                output,
                code=self.code,
                static_findings=self.static_findings,
                schema_first_try=schema_first_try,
                settings=self.settings.verify,
            )
        return verify_analysis(
            output,
            code=self.code,
            static_findings=self.static_findings,
            hint=self.hint,
            expected=self.question.expected if self.question else None,
            schema_first_try=schema_first_try,
            settings=self.settings.verify,
        )

    def leaks(self, texts: list[str]) -> LeakCheck:
        """Serbest metinleri (gerekçe, açıklama) sızıntı kontrolünden geçirir."""
        return check_leaks(
            texts,
            None,
            student_code=self.code.text,
            language=self.code.language,
            engine=self.code.engine,
            reference=self.reference,
            question_text=question_text(self.question),
            settings=self.settings.verify,
        )

    def socratic(
        self, output: LLMSocraticOutput, hint_level: int, regenerated: bool
    ) -> SocraticVerification:
        return verify_socratic(
            output,
            code=self.code,
            hint_level=hint_level,
            question=self.question,
            reference=self.reference,
            regenerated=regenerated,
            settings=self.settings.verify,
        )


def scrub_analysis(
    verification: AnalysisVerification,
    verify: VerifyArgs,
    templates: MentorTemplates,
) -> tuple[AnalysisVerification, list[str]]:
    """Öğrenciye giden gerekçe ve LLM açıklamalarını da sızıntıya karşı süzer (Faz 9 gözlemi):
    çözüm ima eden gerekçe adımı çıkarılır, açıklama nötr metinle değiştirilir."""
    warnings: list[str] = []
    complexity = verification.complexity
    if complexity is not None:
        check = verify.leaks(complexity.reasoning_steps)
        bad = {v.index for v in check.violations}
        if bad:
            steps = [s for i, s in enumerate(complexity.reasoning_steps) if i not in bad]
            complexity = complexity.model_copy(update={"reasoning_steps": steps})
            warnings.append(SCRUB_WARNING_COMPLEXITY)
    llm_findings = [f for f in verification.findings if f.source is FindingSource.LLM]
    check = verify.leaks([f.description for f in llm_findings])
    leaky = {llm_findings[v.index].id for v in check.violations if v.index is not None}
    findings = [
        f.model_copy(update={"description": fallback_description(templates, f)})
        if f.id in leaky
        else f
        for f in verification.findings
    ]
    if leaky:
        warnings.append(SCRUB_WARNING_FINDINGS)
    scrubbed = verification.model_copy(update={"complexity": complexity, "findings": findings})
    return scrubbed, warnings


def degraded_complexity(
    hint: ComplexityHint | None, question: QuestionContext | None
) -> ComplexityResult | None:
    """Zarif bozulma (§5.6): zaman karmaşıklığı statik ipucundan; bellek bilinmiyor."""
    if hint is None:
        return None
    time = parse_bigo(hint.value)
    return ComplexityResult(
        time_complexity=time.canonical,
        space_complexity=UNKNOWN_SPACE,
        display_time=time.display,
        reasoning_steps=list(hint.basis),
        is_optimal=is_optimal(time, question.expected if question else None),
        optimal_time_target=None,
        static_hint=hint.value,
        agreement="no_hint",
        confidence=_HINT_CONFIDENCE[hint.confidence],
    )
