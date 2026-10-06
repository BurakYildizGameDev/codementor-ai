"""LLM'siz mentor soruları: erken çıkış (mimari §5.2.4) ve zarif bozulma (§5.6).

Metinler `data/mentor_templates.yaml`'dadır; burada yalnızca seçim yapılır.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from codementor.models.enums import Severity
from codementor.models.findings import Diagnostic, Finding, issues_only
from codementor.models.pipeline import MentorTemplates
from codementor.models.prompts import QuestionContext
from codementor.models.report import SocraticResult
from codementor.questions._loader import DataFileError, load_model

MAX_TEMPLATE_QUESTIONS = 3
_SEVERITY_RANK = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}


class MentorTemplatesError(DataFileError):
    """Şablon dosyası okunamadı ya da geçersiz."""


@lru_cache(maxsize=4)
def load_templates(path: Path) -> MentorTemplates:
    """`data/mentor_templates.yaml` (önbellekli)."""
    return load_model(path, MentorTemplates, MentorTemplatesError)


def _early_exit_question(templates: MentorTemplates, diagnostic: Diagnostic) -> str:
    message = diagnostic.message
    for template in templates.early_exit:
        if message.startswith(template.match) if template.prefix else template.match in message:
            return template.question.format(line=diagnostic.line, message=diagnostic.message)
    return templates.early_exit_default.format(line=diagnostic.line, message=diagnostic.message)


def early_exit_socratic(
    templates: MentorTemplates, diagnostics: list[Diagnostic], hint_level: int
) -> SocraticResult:
    """Derleme başarısız: ilk hatalardan (satır sırasıyla, tekrarsız) şablon sorular."""
    errors = sorted((d for d in diagnostics if d.severity == "error"), key=lambda d: d.line)
    questions = list(
        dict.fromkeys(_early_exit_question(templates, d) for d in errors or diagnostics)
    )[:MAX_TEMPLATE_QUESTIONS]
    if not questions:
        questions = [templates.early_exit_default.format(line=1, message="derleme başarısız")]
    return SocraticResult(
        key_flaw_concept=templates.early_exit_concept,
        hint_level=hint_level,
        guiding_questions=questions,
        next_step_hint=templates.early_exit_hint,
        leak_check="skipped",
    )


def degraded_socratic(
    templates: MentorTemplates,
    findings: list[Finding],
    question: QuestionContext | None,
    hint_level: int,
) -> SocraticResult:
    """LLM analizi kullanılamadı: sorunun ipucu merdiveni + en önemli bulgulardan sorular.

    Seviye 1'de satır verilmez (kavramsal şablon); 2-3'te satıra işaret edilir.
    """
    questions: list[str] = []
    if question is not None and question.hint_ladder.get(hint_level):
        questions.append(question.hint_ladder[hint_level])
    ranked = sorted(issues_only(findings), key=lambda f: (_SEVERITY_RANK[f.severity], f.line_start))
    for finding in ranked:
        template = templates.categories.get(finding.category)
        if template is None:
            continue
        text = (
            template.conceptual
            if hint_level == 1
            else template.pointed.format(line=finding.line_start)
        )
        if text not in questions:
            questions.append(text)
        if len(questions) >= MAX_TEMPLATE_QUESTIONS:
            break
    if not questions:
        questions.append(templates.degraded_generic)
    top = templates.categories.get(ranked[0].category) if ranked else None
    return SocraticResult(
        key_flaw_concept=top.label if top else templates.degraded_concept,
        hint_level=hint_level,
        guiding_questions=questions,
        next_step_hint=templates.degraded_hint,
        leak_check="skipped",
    )


def fallback_description(templates: MentorTemplates, finding: Finding) -> str:
    """Çözümü ele veren LLM açıklamasının yerine konan nötr metin."""
    template = templates.categories.get(finding.category)
    label = template.label if template else finding.category.value
    return templates.finding_fallback.format(label=label)
