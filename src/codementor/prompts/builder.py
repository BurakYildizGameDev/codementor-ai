"""K3 prompt oluşturucu: sürümlü, bütçeli, iki geçişli mesajlar (mimari §5.4).

Prompt metinleri Python'da değil `prompts/v1/*.j2` şablonlarındadır. Hata ayıklama:
`python -m codementor.prompts.builder --demo unity-hard-inventory`.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from codementor.config import Settings, get_settings
from codementor.log import get_logger
from codementor.models.findings import Finding
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMMarkupAnalysisOutput,
    LLMSinglePassOutput,
    LLMSocraticOutput,
    LLMVerifyOutput,
)
from codementor.models.prompts import (
    AnalysisPromptInput,
    BuiltPrompt,
    FewShotExample,
    QuestionContext,
    SocraticPromptInput,
    VerifyPromptInput,
)
from codementor.models.provider import ChatMessage
from codementor.models.request import NormalizedCode
from codementor.prompts.budget import (
    CHARS_PER_TOKEN,
    MESSAGE_OVERHEAD_TOKENS,
    PromptBudgetError,
    Render,
    context_budget,
    estimate_messages,
    estimate_tokens,
    fit_to_budget,
)
from codementor.prompts.fewshot import fewshot_view, load_fewshots, select_fewshots
from codementor.prompts.mentoring import mentoring_profile
from codementor.prompts.summary import Detail, digest_facts, select_function_hints
from codementor.prompts.templates import guard_delimiters, prompt_version, render

FEWSHOT_DIR = "fewshots"
MAX_REPAIR_RAW_CHARS = 8000
MAX_REPAIR_ERRORS = 20
MAX_REPAIR_ERROR_CHARS = 300
_BLANK_RUNS = re.compile(r"\n{3,}")
log = get_logger("codementor.prompts")

# Kademeler: olgular 0 = tam, 1 = kısa, 2 = yok; bulgular 0 = açıklamalı, 1 = yalnız kanıt,
# 2 = yalnız sayı; kontrol listesi 0 = tam, 1 = yarısı, 2 = yok; few-shot'lar birer birer.
_FACT_DETAILS: tuple[Detail, ...] = ("full", "brief")


@lru_cache(maxsize=4)
def _fewshots(directory: Path, version: str) -> tuple[FewShotExample, ...]:
    """Sürüm anahtarı dosya değişince önbelleği geçersiz kılar."""
    del version
    path = directory / FEWSHOT_DIR
    if not path.is_dir():
        log.warning("prompt_fewshot_dir_missing", path=str(path))
        return ()
    return tuple(load_fewshots(path))


def _tidy(text: str) -> str:
    return _BLANK_RUNS.sub("\n\n", text).strip()


def _messages(directory: Path, name: str, context: Mapping[str, Any]) -> list[ChatMessage]:
    return [
        ChatMessage(
            role="system", content=_tidy(render(directory, f"{name}.system.j2", **context))
        ),
        ChatMessage(role="user", content=_tidy(render(directory, f"{name}.user.j2", **context))),
    ]


def _code_view(code: NormalizedCode, settings: Settings) -> str:
    """Numaralı görünüm; `numbered_code` ablasyonunda düz kod (mimari §14.4)."""
    return code.numbered_view if settings.prompts.numbered_code else code.text


def _checklist(inp: AnalysisPromptInput, limit: int) -> list[str]:
    extra = inp.question.checklist_extra if inp.question else []
    items = list(extra) + [item.text for item in inp.checklist]
    return list(dict.fromkeys(items))[:limit]


def _analysis_renderer(
    inp: AnalysisPromptInput, name: str, settings: Settings
) -> tuple[Render, dict[str, int], str]:
    """Kademeli render fonksiyonu, kademe sınırları ve `prompt_version`."""
    directory = settings.prompts.dir
    version = prompt_version(directory)
    lang, engine = inp.code.language, inp.code.engine
    fewshots = [
        fewshot_view(e, numbered=settings.prompts.numbered_code)
        for e in select_fewshots(
            _fewshots(directory.resolve(), version), lang, engine, settings.prompts.max_fewshots
        )
    ]
    checklist = _checklist(inp, settings.prompts.max_checklist_items)
    # olgu kademeleri: 0 = tam, 1 = kısa, 2 = yok (fonksiyon ipuçları da olgudur)
    digests = [digest_facts(inp.facts, detail) for detail in _FACT_DETAILS] + [None]
    hints = [select_function_hints(inp.function_hints, inp.facts, d) for d in _FACT_DETAILS]
    hints.append([])
    base: dict[str, Any] = {
        "language": lang,
        "engine": engine,
        "question": inp.question,
        "code_view": guard_delimiters(_code_view(inp.code, settings)),
        "hint": inp.hint,
        "static_findings": inp.static_findings,
        "profile": mentoring_profile(
            inp.question.difficulty if inp.question else None, inp.attempt
        ),
    }

    def render_levels(levels: Mapping[str, int]) -> list[ChatMessage]:
        kept_checklist = {0: checklist, 1: checklist[: len(checklist) // 2], 2: []}
        context = base | {
            "fewshots": fewshots[: len(fewshots) - levels["fewshots"]],
            "checklist": kept_checklist[levels["checklist"]],
            "facts": digests[levels["facts"]],
            "function_hints": hints[levels["facts"]],
            "findings_level": levels["static_findings"],
        }
        return _messages(directory, name, context)

    max_levels = {
        "fewshots": len(fewshots),
        "checklist": 2 if checklist else 0,
        "facts": 2,
        "static_findings": 2 if inp.static_findings else 0,
    }
    return render_levels, max_levels, version


def _analysis_like(
    inp: AnalysisPromptInput,
    name: str,
    output_model: type[BaseModel],
    settings: Settings | None,
    provider: str | None,
) -> BuiltPrompt:
    settings = settings or get_settings()
    render_levels, max_levels, version = _analysis_renderer(inp, name, settings)
    budget = context_budget(settings, provider, output_model)
    messages, trimmed = fit_to_budget(
        render_levels,
        max_levels,
        budget,
        code_tokens=estimate_tokens(inp.code.numbered_view),
    )
    return BuiltPrompt(
        messages=messages,
        prompt_version=version,
        estimated_tokens=estimate_messages(messages),
        budget_tokens=budget,
        trimmed=trimmed,
    )


def build_analysis_messages(
    inp: AnalysisPromptInput, *, settings: Settings | None = None, provider: str | None = None
) -> BuiltPrompt:
    """Geçiş A: karmaşıklık + ek bulgular (`LLMAnalysisOutput`)."""
    return _analysis_like(inp, "analysis", LLMAnalysisOutput, settings, provider)


def build_markup_analysis_messages(
    inp: AnalysisPromptInput, *, settings: Settings | None = None, provider: str | None = None
) -> BuiltPrompt:
    """HTML/CSS Geçiş A (ADR-0015): yalnızca ek bulgular (`LLMMarkupAnalysisOutput`)."""
    return _analysis_like(inp, "markup_analysis", LLMMarkupAnalysisOutput, settings, provider)


def build_single_pass_messages(
    inp: AnalysisPromptInput, *, settings: Settings | None = None, provider: str | None = None
) -> BuiltPrompt:
    """`pipeline.mode = "single_pass"`: analiz + Sokratik sorular tek çağrıda."""
    return _analysis_like(inp, "single_pass", LLMSinglePassOutput, settings, provider)


def _severity_order(findings: list[Finding]) -> list[Finding]:
    rank = {"high": 0, "medium": 1, "low": 2}
    return sorted(findings, key=lambda f: (rank.get(f.severity, 3), f.line_start))


def build_socratic_messages(
    inp: SocraticPromptInput, *, settings: Settings | None = None, provider: str | None = None
) -> BuiltPrompt:
    """Geçiş B: doğrulanmış analizden Sokratik sorular (`LLMSocraticOutput`). Kırpılmaz."""
    settings = settings or get_settings()
    directory = settings.prompts.dir
    question: QuestionContext | None = inp.question
    context: dict[str, Any] = {
        "language": inp.code.language,
        "engine": inp.code.engine,
        "question": question,
        "code_view": guard_delimiters(_code_view(inp.code, settings)),
        "findings": _severity_order(inp.findings),
        "complexity": inp.complexity,
        "profile": mentoring_profile(question.difficulty if question else None, inp.attempt),
    }
    budget = context_budget(settings, provider, LLMSocraticOutput)
    messages, _ = fit_to_budget(
        lambda _: _messages(directory, "socratic", context),
        {},
        budget,
        code_tokens=estimate_tokens(inp.code.numbered_view),
    )
    return BuiltPrompt(
        messages=messages,
        prompt_version=prompt_version(directory),
        estimated_tokens=estimate_messages(messages),
        budget_tokens=budget,
    )


def build_verify_messages(
    inp: VerifyPromptInput, *, settings: Settings | None = None, provider: str | None = None
) -> BuiltPrompt:
    """Doğrulama geçişi (Faz 35): LLM bulgularını tek tek sınatır (`LLMVerifyOutput`).
    Kırpılmaz; bulgular rapordaki sırayla numaralanır (`verify.proof.verify_targets`)."""
    settings = settings or get_settings()
    directory = settings.prompts.dir
    context: dict[str, Any] = {
        "language": inp.code.language,
        "engine": inp.code.engine,
        "question": inp.question,
        "code_view": guard_delimiters(_code_view(inp.code, settings)),
        "findings": inp.findings,
    }
    budget = context_budget(settings, provider, LLMVerifyOutput)
    messages, _ = fit_to_budget(
        lambda _: _messages(directory, "verify", context),
        {},
        budget,
        code_tokens=estimate_tokens(inp.code.numbered_view),
    )
    return BuiltPrompt(
        messages=messages,
        prompt_version=prompt_version(directory),
        estimated_tokens=estimate_messages(messages),
        budget_tokens=budget,
    )


def repair_errors(exc: ValidationError) -> list[str]:
    """Onarım için hata satırları: yalnızca konum + mesaj. `input_value` verilmez; modelin
    yansıttığı öğrenci metni talimat kanalına geri dönmesin (mimari §12)."""
    return [
        f"{'.'.join(str(part) for part in err['loc']) or '(kök)'}: {err['msg']}"
        for err in exc.errors(include_url=False, include_input=False)
    ]


def build_repair_messages(
    original: BuiltPrompt,
    *,
    raw_text: str,
    errors: list[str],
    settings: Settings | None = None,
) -> BuiltPrompt:
    """Onarım: özgün konuşma + modelin (bütçeye göre kırpılmış) yanıtı + doğrulama hataları.

    Hatalar ve ham yanıt veri olarak çerçevelenir, sınırlayıcı koruması uygulanır. Özgün
    prompt'un bütçesi aşılmaz: ham yanıt payı kalan yere göre küçülür; yer yoksa
    `PromptBudgetError`.
    """
    settings = settings or get_settings()
    shown = [guard_delimiters(e[:MAX_REPAIR_ERROR_CHARS]) for e in errors[:MAX_REPAIR_ERRORS]]
    text = _tidy(
        render(
            settings.prompts.dir,
            "repair.user.j2",
            errors=shown,
            omitted_errors=len(errors) - len(shown),
        )
    )
    fixed = [*original.messages, ChatMessage(role="user", content=text)]
    room = original.budget_tokens - estimate_messages(fixed) - MESSAGE_OVERHEAD_TOKENS
    if room <= 0:
        raise PromptBudgetError(estimate_messages(fixed), original.budget_tokens)
    raw = guard_delimiters(raw_text[: min(MAX_REPAIR_RAW_CHARS, room * CHARS_PER_TOKEN)])
    messages = [*original.messages, ChatMessage(role="assistant", content=raw), fixed[-1]]
    return BuiltPrompt(
        messages=messages,
        prompt_version=original.prompt_version,
        estimated_tokens=estimate_messages(messages),
        budget_tokens=original.budget_tokens,
        trimmed=original.trimmed,
    )


if __name__ == "__main__":  # pragma: no cover - hata ayıklama aracı
    from codementor.prompts._demo import main

    raise SystemExit(main())
