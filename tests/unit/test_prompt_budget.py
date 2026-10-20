"""Token bütçesi ve kırpma sırası (mimari §5.4.5)."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from itertools import pairwise

import pytest
from hypothesis import given
from hypothesis import strategies as st

from codementor.config import Settings, load_settings
from codementor.models.llm_output import LLMAnalysisOutput
from codementor.models.provider import ChatMessage
from codementor.prompts.budget import (
    CHARS_PER_TOKEN,
    TRIM_ORDER,
    PromptBudgetError,
    PromptConfigError,
    context_budget,
    estimate_messages,
    estimate_tokens,
    fit_to_budget,
    provider_chain,
    schema_tokens,
)


@given(st.text(), st.text())
def test_estimate_tokens_monotonic(a: str, b: str) -> None:
    assert estimate_tokens(a + b) >= estimate_tokens(a)
    assert estimate_tokens(a + b) <= estimate_tokens(a) + estimate_tokens(b) + 1


def test_estimate_tokens_is_conservative() -> None:
    assert estimate_tokens("") == 0
    assert estimate_tokens("ab") == 1
    assert estimate_tokens("abc") == 2  # yukarı yuvarlanır
    assert estimate_tokens("x" * 300) == 150


def test_trim_order_matches_architecture() -> None:
    # §5.4.5: sondan kırpılır → few-shot, kontrol listesi, olgular, kural bulguları
    assert TRIM_ORDER == ("fewshots", "checklist", "facts", "static_findings")


SECTION_SIZE = 300  # karakter; ≈ 150 token


Render = Callable[[Mapping[str, int]], list[ChatMessage]]


def _render_factory(calls: list[dict[str, int]]) -> tuple[dict[str, int], Render]:
    max_levels = {"fewshots": 2, "checklist": 2, "facts": 2, "static_findings": 2}

    def render(levels: Mapping[str, int]) -> list[ChatMessage]:
        calls.append(dict(levels))
        parts = ["CODE" * 100]  # kod: ≈ 200 token, asla kırpılmaz
        for name, top in max_levels.items():
            parts.append(name[0] * SECTION_SIZE * (top - levels[name]))
        return [ChatMessage(role="user", content="".join(parts))]

    return max_levels, render


def test_no_trim_when_fits() -> None:
    calls: list[dict[str, int]] = []
    max_levels, render = _render_factory(calls)
    messages, trimmed = fit_to_budget(render, max_levels, budget=10_000)
    assert trimmed == []
    assert len(calls) == 1
    assert estimate_messages(messages) <= 10_000


def test_trim_order_fewshot_then_checklist_then_facts() -> None:
    calls: list[dict[str, int]] = []
    max_levels, render = _render_factory(calls)
    full = estimate_messages(render({k: 0 for k in max_levels}))
    calls.clear()
    # few-shot'ın ikisi ve kontrol listesinin biri gidince sığar
    budget = full - 3 * (SECTION_SIZE // CHARS_PER_TOKEN)
    _, trimmed = fit_to_budget(render, max_levels, budget=budget)
    assert trimmed == ["fewshots", "checklist"]
    assert calls[-1] == {"fewshots": 2, "checklist": 1, "facts": 0, "static_findings": 0}
    # kırpma adımları sırayla: bir sonraki bölüme ancak önceki tükenince geçilir
    order = [next(k for k in TRIM_ORDER if a[k] != b[k]) for a, b in pairwise(calls)]
    assert order == ["fewshots", "fewshots", "checklist"]


def test_facts_trimmed_before_static_findings() -> None:
    calls: list[dict[str, int]] = []
    max_levels, render = _render_factory(calls)
    full = estimate_messages(render({k: 0 for k in max_levels}))
    _, trimmed = fit_to_budget(
        render,
        max_levels,
        budget=full - 7 * (SECTION_SIZE // CHARS_PER_TOKEN),
    )
    assert trimmed == ["fewshots", "checklist", "facts", "static_findings"]


def test_code_never_trimmed_and_too_large_raises() -> None:
    calls: list[dict[str, int]] = []
    max_levels, render = _render_factory(calls)
    with pytest.raises(PromptBudgetError) as info:
        fit_to_budget(render, max_levels, budget=50)
    # her bölüm sonuna kadar kırpıldı, kod hâlâ duruyor
    assert calls[-1] == dict.fromkeys(max_levels, 2)
    assert "kırpılmaz" in str(info.value)
    assert info.value.estimated > info.value.budget == 50


def _providers(**extra: object) -> dict[str, object]:
    base: dict[str, object] = {
        "default": "claude_cli",
        "fallback": [],
        "claude_cli": {"context_tokens": 100_000},
        "ollama": {"num_ctx": 8192},
        "gemini": {"context_tokens": 20_000, "max_tokens": 2000},
        "anthropic": {"context_tokens": None, "max_tokens": None},
    }
    return base | extra


def _settings(**extra: object) -> Settings:
    return load_settings(
        providers=_providers(**extra),
        prompts={"default_context_tokens": 16_384, "reserve_output_tokens": 1000},
    )


def test_budget_from_provider_config() -> None:
    settings = _settings()
    schema = schema_tokens(LLMAnalysisOutput)
    assert schema > 0  # şema tokenları düşülüyor

    def budget(name: str) -> int:
        return context_budget(settings, name, LLMAnalysisOutput)

    assert budget("claude_cli") == 100_000 - 1000 - schema
    assert budget("ollama") == 8192 - 1000 - schema  # num_ctx
    assert budget("gemini") == 20_000 - 2000 - schema  # max_tokens çıktı payı
    assert budget("anthropic") == 16_384 - 1000 - schema  # context_tokens yok → varsayılan
    # zincirde yapılandırılmış ama bölümü olmayan ad (testlerin FakeProvider'ı): varsayılanlar
    chained = _settings(default="fake", fallback=[])
    assert context_budget(chained, "fake", LLMAnalysisOutput) == 16_384 - 1000 - schema
    assert context_budget(chained, None, LLMAnalysisOutput) == 16_384 - 1000 - schema


def test_budget_is_smallest_in_fallback_chain() -> None:
    """Denetim O1: fallback'teki küçük bağlamlı sağlayıcı prompt'u sessizce kesmesin."""
    schema = schema_tokens(LLMAnalysisOutput)
    chained = _settings(fallback=["ollama"])
    assert context_budget(chained, None, LLMAnalysisOutput) == 8192 - 1000 - schema
    # açık birincil seçilse de fallback'ler zincirde kalır
    assert context_budget(chained, "claude_cli", LLMAnalysisOutput) == 8192 - 1000 - schema
    # FallbackProvider.name biçimi
    solo = _settings()
    assert context_budget(solo, "claude_cli→ollama", LLMAnalysisOutput) == 8192 - 1000 - schema
    assert provider_chain(chained, None) == ["claude_cli", "ollama"]


def test_unknown_provider_rejected() -> None:
    with pytest.raises(PromptConfigError, match="'olama': bilinmeyen sağlayıcı"):
        context_budget(_settings(), "olama", LLMAnalysisOutput)
    with pytest.raises(PromptConfigError, match="kaldırıldı"):
        context_budget(_settings(), "openai", LLMAnalysisOutput)


def test_misconfigured_context_is_config_error_not_code_error() -> None:
    """Denetim D10: çıktı payı bağlamı yutarsa kodu suçlayan hata değil yapılandırma hatası."""
    settings = _settings(ollama={"num_ctx": 4096, "max_tokens": 4000})
    with pytest.raises(PromptConfigError, match="Yapılandırma hatası: ollama"):
        context_budget(settings, "ollama", LLMAnalysisOutput)
