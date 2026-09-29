"""Gerçek sağlayıcılara çıkan testler (`@pytest.mark.live`, CI'da çalışmaz).

- Ollama: `ollama serve` açık ve yapılandırılan model çekilmişse.
- Bulut: `[providers.X] model` tanımlı ve anahtar ortam değişkeni doluysa; yoksa atlanır.
"""

from __future__ import annotations

import os

import pytest

from codementor.config import load_settings
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import ProviderError, build_provider
from codementor.providers.ollama import OllamaProvider

pytestmark = [pytest.mark.live, pytest.mark.anyio]

MESSAGES = [
    ChatMessage(
        role="system",
        content="Sen bir programlama mentorusun. Kodu düzeltme; yalnızca soru sor.",
    ),
    ChatMessage(
        role="user",
        content=(
            "Öğrenci kodu:\n  1 | int f(int *a, int n) { return a[n]; }\n"
            "Temel kavram hatasını ve 1-2 yönlendirici soruyu ver."
        ),
    ),
]


async def _assert_structured(name: str) -> None:
    provider = build_provider(name)
    result = await provider.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert result.parsed is not None, result.raw_text[:300]
    LLMSocraticOutput.model_validate(result.parsed)
    assert result.usage.output_tokens > 0


async def test_ollama_live() -> None:
    cfg = load_settings().providers.ollama
    try:
        models = await OllamaProvider(cfg).list_models()
    except ProviderError as exc:
        pytest.skip(f"Ollama erişilemiyor: {exc}")
    if cfg.model not in models and f"{cfg.model}:latest" not in models:
        pytest.skip(f"model çekilmemiş: {cfg.model}")
    await _assert_structured("ollama")


@pytest.mark.parametrize("name", ["openai", "deepseek", "anthropic"])
async def test_cloud_live(name: str) -> None:
    cfg = getattr(load_settings().providers, name)
    if not cfg.model or not os.environ.get(cfg.api_key_env or "", ""):
        pytest.skip(f"{name}: model veya anahtar tanımlı değil")
    await _assert_structured(name)
