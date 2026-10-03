"""Ortak sözleşme: tüm adaptörler (Fake, Ollama, Gemini, Anthropic, CLI)
aynı testleri geçer."""

from __future__ import annotations

import pytest

from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import (
    ProviderConfigError,
    ProviderRateLimitError,
    ProviderRequestError,
    ProviderServerError,
    ProviderUnavailableError,
)
from tests.providers.contract import Harness, Network, Ok, SleepRecorder, Status, Timeout

pytestmark = pytest.mark.anyio

MESSAGES = [
    ChatMessage(role="system", content="Sen bir kod mentorusun."),
    ChatMessage(role="user", content="Kodu incele."),
]
ANSWER = {
    "key_flaw_concept": "sınır denetimi",
    "guiding_questions": ["Dizi boşsa ne olur?"],
    "next_step_hint": None,
}


async def _call(harness: Harness, model: str = "test-model") -> object:
    provider = harness.make(model)
    return await provider.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())


async def test_success_parsed_matches_model(harness: Harness) -> None:
    harness.script([Ok(ANSWER)])
    result = await harness.make().generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.parsed == ANSWER
    assert LLMSocraticOutput.model_validate(result.parsed).guiding_questions
    assert result.provider == harness.name
    assert harness.request_count == 1


async def test_usage_and_latency(harness: Harness) -> None:
    harness.script([Ok(ANSWER)])
    result = await harness.make().generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.latency_ms >= 0
    if harness.expected_usage is not None:
        assert (result.usage.input_tokens, result.usage.output_tokens) == harness.expected_usage
        assert not result.usage.estimated
    else:
        assert result.usage.output_tokens > 0


async def test_model_name_from_config(harness: Harness) -> None:
    harness.script([Ok(ANSWER)])
    result = await harness.make("config-model").generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert harness.sent_model == "config-model"  # istekte giden model yapılandırmadan
    # sonuçta sağlayıcının bildirdiği model (HTTP) ya da yapılandırılan (Fake)
    assert result.model in {"config-model", "served-model"}


async def test_broken_json_keeps_raw_text(harness: Harness) -> None:
    harness.script([Ok(raw='{"key_flaw_concept": "yarım')])
    result = await harness.make().generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.parsed is None
    assert result.raw_text == '{"key_flaw_concept": "yarım'
    assert harness.request_count == 1  # bozuk JSON yeniden denenmez (onarım Faz 9'da)


@pytest.mark.parametrize("status", [500, 502, 503, 529])
async def test_retries_on_5xx_then_succeeds(
    harness: Harness, sleep: SleepRecorder, status: int
) -> None:
    harness.script([Status(status), Ok(ANSWER)])
    result = await harness.make().generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.parsed == ANSWER
    assert harness.request_count == 2
    assert len(sleep.delays) == 1


async def test_retries_on_429_respects_retry_after(harness: Harness, sleep: SleepRecorder) -> None:
    if not getattr(harness, "supports_retry_after", True):
        pytest.skip("CLI ajanında HTTP başlığı yok")
    harness.script([Status(429, {"retry-after": "3"}), Ok(ANSWER)])
    result = await harness.make().generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.parsed == ANSWER
    assert sleep.delays == [3.0]


async def test_retries_exhausted_raises(harness: Harness, sleep: SleepRecorder) -> None:
    harness.script([Status(503), Status(503), Status(429)])
    with pytest.raises(ProviderRateLimitError):
        await _call(harness)
    assert harness.request_count == 3  # 1 + en fazla 2 yeniden deneme
    assert len(sleep.delays) == 2


async def test_network_error_retried_then_unavailable(harness: Harness) -> None:
    harness.script([Network(), Network(), Network()])
    with pytest.raises(ProviderUnavailableError):
        await _call(harness)
    assert harness.request_count == 3


async def test_timeout_is_retried(harness: Harness) -> None:
    if harness.name == "claude_cli":
        pytest.skip("CLI zaman aşımı bilerek yeniden denenmez (ADR-0012)")
    harness.script([Timeout(), Ok(ANSWER)])
    result = await harness.make().generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.parsed == ANSWER
    assert harness.request_count == 2


@pytest.mark.parametrize("status", [400, 401, 403, 404, 422])
async def test_4xx_not_retried(harness: Harness, sleep: SleepRecorder, status: int) -> None:
    harness.script([Status(status), Ok(ANSWER)])
    with pytest.raises(ProviderRequestError) as info:
        await _call(harness)
    assert harness.request_count == 1
    assert sleep.delays == []
    assert info.value.status == status


async def test_5xx_error_class(harness: Harness) -> None:
    harness.script([Status(500), Status(500), Status(500)])
    with pytest.raises(ProviderServerError):
        await _call(harness)


async def test_missing_model_config_error(harness: Harness) -> None:
    harness.script([Ok(ANSWER)])
    with pytest.raises(ProviderConfigError):
        await _call(harness, model="")
    assert harness.request_count == 0


async def test_deeply_nested_json_is_not_parsed(harness: Harness) -> None:
    # denetim Y1: prompt injection binlerce `[` ürettirebilir; RecursionError kaçmamalı
    harness.script([Ok(raw="[" * 100_000 + "]" * 100_000)])
    result = await harness.make().generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.parsed is None


@pytest.mark.parametrize("value", ["nan", "inf", "-5", "Wed, 21 Oct 2026 07:28:00 GMT"])
async def test_bad_retry_after_falls_back_to_backoff(
    harness: Harness, sleep: SleepRecorder, value: str
) -> None:
    # denetim O1: `nan` sonsuz beklemeye yol açıyordu
    harness.script([Status(429, {"retry-after": value}), Ok(ANSWER)])
    result = await harness.make().generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.parsed == ANSWER
    assert len(sleep.delays) == 1
    assert 0 <= sleep.delays[0] <= 5.0


async def test_long_retry_after_gives_up_immediately(
    harness: Harness, sleep: SleepRecorder
) -> None:
    # kota tükenmesi (ör. 1 saat): beklemeden bırak, fallback sıradakine geçsin
    if not getattr(harness, "supports_retry_after", True):
        pytest.skip("CLI ajanında HTTP başlığı yok")
    harness.script([Status(429, {"retry-after": "3600"}), Ok(ANSWER)])
    with pytest.raises(ProviderRateLimitError):
        await _call(harness)
    assert harness.request_count == 1
    assert sleep.delays == []
