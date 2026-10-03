"""Faz 28: Gemini sağlayıcısı (ADR-0020), Google'ın OpenAI uyumlu uç noktası üzerinden.

Kaynak: https://ai.google.dev/gemini-api/docs/openai (base_url `.../v1beta/openai/`,
`Authorization: Bearer`, yapılandırılmış çıktı OpenAI SDK'nın `parse()` biçimiyle).
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from codementor.config import GeminiConfig, ProvidersSettings
from codementor.models.llm_output import LLMAnalysisOutput, LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import ProviderConfigError
from codementor.providers.factory import PROVIDER_NAMES, build_provider
from codementor.providers.openai_compat import OpenAICompatProvider
from codementor.providers.schema_adapter import SchemaAdapter
from tests.providers.contract import openai_body

pytestmark = pytest.mark.anyio
MESSAGES = [
    ChatMessage(role="system", content="Sistem."),
    ChatMessage(role="user", content="Kullanıcı."),
]
ANSWER = json.dumps({"key_flaw_concept": "k", "guiding_questions": ["?"], "next_step_hint": None})
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"


def _gemini(**overrides: object) -> OpenAICompatProvider:
    providers = ProvidersSettings()
    providers.gemini = GeminiConfig(model="gemini-test", **overrides)  # type: ignore[arg-type]
    provider = build_provider("gemini", providers)
    assert isinstance(provider, OpenAICompatProvider)
    return provider


def test_registered_with_documented_defaults() -> None:
    assert "gemini" in PROVIDER_NAMES
    cfg = GeminiConfig()
    assert cfg.base_url == "https://generativelanguage.googleapis.com/v1beta/openai"
    assert cfg.api_key_env == "GEMINI_API_KEY"
    assert cfg.model == ""  # model adı koda gömülmez (AGENTS.md kural 5)


def test_payload_uses_strict_json_schema() -> None:
    payload = _gemini().build_payload(MESSAGES, LLMAnalysisOutput, GenerationOptions())
    assert payload["response_format"] == {
        "type": "json_schema",
        "json_schema": {
            "name": "LLMAnalysisOutput",
            "schema": SchemaAdapter(LLMAnalysisOutput).openai_strict(),
            "strict": True,
        },
    }
    assert payload["model"] == "gemini-test"
    assert payload["messages"] == [m.model_dump() for m in MESSAGES]


def test_token_limit_field_and_no_seed() -> None:
    """Gemini uyumlu uç `max_tokens`'ı uygular; `seed` belgelenmemiş, gönderilmez."""
    payload = _gemini(max_tokens=900, seed=7, temperature=0.2).build_payload(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert payload["max_tokens"] == 900
    assert "max_completion_tokens" not in payload
    assert "seed" not in payload
    assert payload["temperature"] == 0.2


def test_no_sampling_params_unless_configured() -> None:
    payload = _gemini().build_payload(MESSAGES, LLMSocraticOutput, GenerationOptions())
    for key in ("temperature", "seed", "max_tokens", "max_completion_tokens"):
        assert key not in payload


async def test_bearer_header_and_url(
    router: respx.MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "gm-test-SECRET-0123456789")
    route = router.post(GEMINI_URL).mock(
        return_value=httpx.Response(200, json=openai_body(ANSWER, "gemini-test"))
    )
    result = await _gemini().generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert result.parsed is not None
    assert result.provider == "gemini"
    assert route.calls.last.request.headers["authorization"] == "Bearer gm-test-SECRET-0123456789"


async def test_missing_key_is_config_error(
    router: respx.MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    route = router.post(GEMINI_URL)
    with pytest.raises(ProviderConfigError, match="GEMINI_API_KEY"):
        await _gemini().generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert route.call_count == 0


def test_other_providers_unchanged() -> None:
    """OpenAI `max_completion_tokens` + seed; DeepSeek `max_tokens`, seed yok."""
    providers = ProvidersSettings()
    providers.openai.model = providers.deepseek.model = "m"
    providers.openai.max_tokens = providers.deepseek.max_tokens = 100
    providers.openai.seed = providers.deepseek.seed = 3
    openai = build_provider("openai", providers)
    deepseek = build_provider("deepseek", providers)
    assert isinstance(openai, OpenAICompatProvider)
    assert isinstance(deepseek, OpenAICompatProvider)
    op = openai.build_payload(MESSAGES, LLMSocraticOutput, GenerationOptions())
    ds = deepseek.build_payload(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert (op["max_completion_tokens"], op["seed"]) == (100, 3)
    assert ds["max_tokens"] == 100
    assert "seed" not in ds
