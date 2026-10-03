"""Yapılandırmadan sağlayıcı kurma ve geri dönüş zinciri (mimari §5.5.3)."""

from __future__ import annotations

import pytest

from codementor.config import ProvidersSettings, Settings
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import (
    AllProvidersFailedError,
    FakeProvider,
    FakeReply,
    FallbackProvider,
    ProviderConfigError,
    RetryPolicy,
    build_chain,
    build_provider,
)
from codementor.providers.anthropic import AnthropicProvider
from codementor.providers.factory import PROVIDER_NAMES, chain_names
from codementor.providers.ollama import OllamaProvider
from codementor.providers.openai_compat import OpenAICompatProvider
from tests.providers.contract import SleepRecorder

pytestmark = pytest.mark.anyio

MESSAGES = [ChatMessage(role="user", content="incele")]
ANSWER = {"key_flaw_concept": "k", "guiding_questions": ["?"], "next_step_hint": None}


def _fake(name: str, *replies: FakeReply) -> FakeProvider:
    return FakeProvider(
        script=list(replies), name=name, retry=RetryPolicy(max_retries=0, sleep=SleepRecorder())
    )


def test_build_each_provider_from_settings() -> None:
    providers = ProvidersSettings()
    assert isinstance(build_provider("ollama", providers), OllamaProvider)
    assert isinstance(build_provider("gemini", providers), OpenAICompatProvider)
    assert isinstance(build_provider("anthropic", providers), AnthropicProvider)


def test_build_uses_config_retries() -> None:
    provider = build_provider("ollama", ProvidersSettings(max_retries=4))
    assert isinstance(provider, OllamaProvider)
    assert provider.transport.retry.max_retries == 4


def test_unknown_provider() -> None:
    with pytest.raises(ProviderConfigError, match="bilinmeyen"):
        build_provider("mistral", ProvidersSettings())


@pytest.mark.parametrize("name", ["openai", "deepseek"])
def test_removed_provider_names_not_registered(name: str) -> None:
    """ADR-0021: kaldırılan adlar kayıtta yok, hata nedeni söylüyor."""
    assert name not in PROVIDER_NAMES
    with pytest.raises(ProviderConfigError, match="kaldırıldı"):
        build_chain(Settings(providers=ProvidersSettings(default=name)))


def test_chain_names_dedup_and_primary() -> None:
    providers = ProvidersSettings(default="ollama", fallback=["gemini", "ollama", "anthropic"])
    assert chain_names(providers) == ["ollama", "gemini", "anthropic"]
    assert chain_names(providers, "anthropic") == ["anthropic", "gemini", "ollama"]


def test_build_chain_single_and_multiple() -> None:
    single = build_chain(Settings(providers=ProvidersSettings(fallback=[])))
    assert isinstance(single, OllamaProvider)
    chain = build_chain(Settings(providers=ProvidersSettings(fallback=["gemini"])))
    assert isinstance(chain, FallbackProvider)
    assert chain.name == "ollama→gemini"


async def test_no_fallback_on_success() -> None:
    first, second = _fake("a", FakeReply(data=ANSWER)), _fake("b", FakeReply(data=ANSWER))
    result = await FallbackProvider([first, second]).generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.provider == "a"
    assert result.warnings == []
    assert second.calls == []


async def test_fallback_on_error_writes_warning() -> None:
    chain = FallbackProvider(
        [
            _fake("ollama", FakeReply(error="network")),
            _fake("gemini", FakeReply(error="401")),
            _fake("anthropic", FakeReply(data=ANSWER)),
        ]
    )
    result = await chain.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert result.provider == "anthropic"
    assert result.parsed == ANSWER
    assert result.warnings == [
        "ollama sağlayıcısı kullanılamadı (bağlantı kurulamadı); gemini ile devam edildi.",
        "gemini sağlayıcısı kullanılamadı (istek reddedildi (401)); anthropic ile devam edildi.",
    ]


async def test_missing_key_triggers_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY")
    providers = ProvidersSettings(default="gemini")
    providers.gemini.model = "m"
    chain = FallbackProvider(
        [build_provider("gemini", providers), _fake("f", FakeReply(data=ANSWER))]
    )
    result = await chain.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert result.provider == "f"
    assert "GEMINI_API_KEY" in result.warnings[0]


async def test_all_fail_raises() -> None:
    chain = FallbackProvider(
        [_fake("a", FakeReply(error="500")), _fake("b", FakeReply(error="400"))]
    )
    with pytest.raises(AllProvidersFailedError, match=r"a: sunucu hatası \(500\); b: istek"):
        await chain.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())


async def test_broken_json_does_not_trigger_fallback() -> None:
    second = _fake("b", FakeReply(data=ANSWER))
    chain = FallbackProvider([_fake("a", FakeReply(raw="{bozuk")), second])
    result = await chain.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert result.provider == "a"
    assert result.parsed is None
    assert second.calls == []


def test_empty_chain_rejected() -> None:
    with pytest.raises(ProviderConfigError):
        FallbackProvider([])
