"""LLM-as-judge ile Sokratik kalite değerlendirme modülü (Faz I / İş 10).

Sokratik soruları, öğrenci kodunu ve ana hata konseptini bağımsız bir LLM yargıcı ile
pedagojik değer, koda temas, Sokratik derinlik ve çözüm sızdırmazlığı ölçütlerine göre
değerlendirir ve yapılandırılmış `SocraticJudgeReport` üretir.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from codementor.log import get_logger
from codementor.models.eval import RunResult, Sample, SocraticJudgeReport
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.paths import resource_path
from codementor.prompts.templates import PromptTemplateError, render
from codementor.providers.base import LLMProvider, ProviderError

DEFAULT_PROMPTS_DIR = resource_path("prompts/v1")
log = get_logger("codementor.eval.judge")


def render_judge_prompt(
    code: str,
    language: str,
    flaw_concept: str,
    questions: Sequence[str],
    next_step_hint: str,
    prompts_dir: Path | None = None,
) -> str:
    """Yargıç LLM için değerlendirme istemini şablondan üretir.

    Kod ve mentor çıktısı `guard` süzgecinden geçer (§12); şablon hataları `PromptTemplateError`.
    """
    return render(
        prompts_dir or DEFAULT_PROMPTS_DIR,
        "judge.j2",
        code=code,
        language=language,
        flaw_concept=flaw_concept,
        questions=list(questions),
        next_step_hint=next_step_hint,
    )


async def evaluate_socratic_quality(
    provider: LLMProvider,
    code: str,
    language: str,
    flaw_concept: str,
    questions: Sequence[str],
    next_step_hint: str,
    prompts_dir: Path | None = None,
) -> SocraticJudgeReport:
    """Tek bir Sokratik mentorluk çıktısını yargıç LLM ile değerlendirir."""
    prompt_text = render_judge_prompt(
        code=code,
        language=language,
        flaw_concept=flaw_concept,
        questions=questions,
        next_step_hint=next_step_hint,
        prompts_dir=prompts_dir,
    )
    messages = [
        ChatMessage(role="user", content=prompt_text),
    ]
    options = GenerationOptions(
        temperature=0.0,
    )
    result = await provider.generate_structured(
        messages=messages,
        output_model=SocraticJudgeReport,
        options=options,
    )
    if result.parsed is not None:
        return SocraticJudgeReport.model_validate(result.parsed)
    text = result.raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    return SocraticJudgeReport.model_validate_json(text)


async def judge_run_result(
    result: RunResult,
    samples: dict[str, Sample],
    provider: LLMProvider,
    prompts_dir: Path | None = None,
    errors: list[str] | None = None,
) -> dict[str, SocraticJudgeReport]:
    """Bir `RunResult` içindeki geçerli Sokratik çıktıları değerlendirir.

    Tek örneğin bozuk yanıtı ya da sağlayıcı hatası koşuyu düşürmez: örnek atlanır, loglanır ve
    kimliği `errors`'a eklenir (o ana dek harcanan yargıç tokenlarının sonucu kaybolmaz).
    """
    reports: dict[str, SocraticJudgeReport] = {}
    for item in result.samples:
        if item.report is None or item.report.socratic is None:
            continue
        socratic = item.report.socratic
        if not socratic.guiding_questions:
            continue
        sample = samples.get(item.id)
        if sample is None:
            continue
        try:
            report = await evaluate_socratic_quality(
                provider=provider,
                code=sample.code,
                language=sample.label.language.value,
                flaw_concept=socratic.key_flaw_concept,
                questions=socratic.guiding_questions,
                next_step_hint=socratic.next_step_hint or "",
                prompts_dir=prompts_dir,
            )
        except PromptTemplateError:
            raise  # kurulum hatası: her örnek aynı şekilde düşer, sessizce atlanmaz
        except (ValidationError, ProviderError, ValueError) as exc:
            log.warning("judge_sample_failed", sample=item.id, error_type=type(exc).__name__)
            if errors is not None:
                errors.append(item.id)
            continue
        reports[item.id] = report
    return reports


def _cell(text: str) -> str:
    """Markdown tablo hücresi: `|` kaçırılır, satır sonları boşluğa çevrilir."""
    return " ".join(text.split()).replace("|", "\\|")


def judge_summary_markdown(reports: dict[str, SocraticJudgeReport]) -> str:
    """Yargıç raporlarının Markdown özet tablosunu üretir."""
    if not reports:
        return "Değerlendirilen örnek bulunamadı.\n"
    lines = [
        (
            "| Örnek | Pedagojik (1-5) | Koda Temas (1-5) | "
            "Sokratik Derinlik (1-5) | Sızıntısız | Genel Puan | Özet |"
        ),
        "|---|---|---|---|---|---|---|",
    ]
    for sample_id, r in sorted(reports.items()):
        leak = "✓" if r.leakage_free else "✗"
        row = (
            f"| {_cell(sample_id)} | {r.pedagogical_value.score} | {r.code_relevance.score} | "
            f"{r.socratic_depth.score} | {leak} | {r.overall_score:.1f} | {_cell(r.summary)} |"
        )
        lines.append(row)
    mean_score = sum(r.overall_score for r in reports.values()) / len(reports)
    lines.append("")
    lines.append(
        f"Ortalama Sokratik Kalite Puanı: **{mean_score:.2f} / 5.0** ({len(reports)} örnek)"
    )
    return "\n".join(lines) + "\n"
