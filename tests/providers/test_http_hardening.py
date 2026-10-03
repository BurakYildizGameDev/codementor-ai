"""HTTP katmanının kötü niyetli/bozuk yanıtlara dayanıklılığı (Faz 7 denetim bulguları)."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

import httpx
import pytest
import respx

from codementor.config import AnthropicConfig, GeminiConfig
from codementor.log import register_secret
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import (
    ProviderConfigError,
    ProviderRequestError,
    ProviderResponseError,
    ProviderUnavailableError,
    RetryPolicy,
)
from codementor.providers._http import HttpTransport
from codementor.providers.anthropic import AnthropicProvider
from codementor.providers.openai_compat import OpenAICompatProvider
from tests.providers.contract import API_KEYS, anthropic_body

pytestmark = pytest.mark.anyio

MESSAGES = [ChatMessage(role="user", content="incele")]
URL = "https://an.test/v1/messages"
DEEP = b"[" * 200_000 + b"]" * 200_000


def _anthropic(
    timeout: float = 30, client: httpx.AsyncClient | None = None, base: str = "https://an.test"
) -> AnthropicProvider:
    return AnthropicProvider(
        AnthropicConfig(base_url=base, model="m"),
        transport=HttpTransport("anthropic", timeout, RetryPolicy(max_retries=0), client),
    )


async def _call(provider: AnthropicProvider) -> object:
    return await provider.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())


async def test_deep_json_body_is_response_error(router: respx.MockRouter) -> None:
    router.post(URL).mock(return_value=httpx.Response(200, content=DEEP))
    with pytest.raises(ProviderResponseError):
        await _call(_anthropic())


async def test_deep_json_error_body_keeps_status_error(router: respx.MockRouter) -> None:
    router.post(URL).mock(return_value=httpx.Response(400, content=DEEP))
    with pytest.raises(ProviderRequestError, match=r"\(400\)"):
        await _call(_anthropic())


async def test_deep_json_in_text_block_gives_no_parsed(router: respx.MockRouter) -> None:
    body = anthropic_body(DEEP.decode(), "m")
    router.post(URL).mock(return_value=httpx.Response(200, json=body))
    result = await _anthropic().generate_structured(
        MESSAGES, LLMSocraticOutput, GenerationOptions()
    )
    assert result.parsed is None


async def test_decoding_error_is_response_error_without_cause(router: respx.MockRouter) -> None:
    router.post(URL).mock(
        return_value=httpx.Response(
            200, headers={"content-encoding": "gzip"}, stream=httpx.ByteStream(b"gzip-degil")
        )
    )
    with pytest.raises(ProviderResponseError) as info:
        await _call(_anthropic())
    assert info.value.__cause__ is None
    assert info.value.__suppress_context__


async def test_network_error_does_not_chain_request_with_key(router: respx.MockRouter) -> None:
    router.post(URL).mock(side_effect=httpx.ConnectError("reddedildi"))
    with pytest.raises(ProviderUnavailableError) as info:
        await _call(_anthropic())
    # httpx istek nesnesi `x-api-key` başlığını açık metinle taşır; zincirlenmemeli
    assert info.value.__cause__ is None
    assert info.value.__suppress_context__


async def test_error_text_masked_before_truncation(router: respx.MockRouter) -> None:
    secret = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcd"
    register_secret(secret)
    message = "x" * 185 + " " + secret
    router.post(URL).mock(return_value=httpx.Response(422, json={"error": {"message": message}}))
    with pytest.raises(ProviderRequestError) as info:
        await _call(_anthropic())
    assert "ABCDEFGHIJ" not in str(info.value)


async def test_identity_encoding_requested(router: respx.MockRouter) -> None:
    route = router.post(URL).mock(return_value=httpx.Response(200, json=anthropic_body("{}", "m")))
    await _call(_anthropic())
    assert route.calls.last.request.headers["accept-encoding"] == "identity"


class _Trickle(httpx.AsyncByteStream):
    """Her parçayı gecikmeyle gönderen sunucu (faz başına zaman aşımını hiç tetiklemez)."""

    async def __aiter__(self) -> AsyncIterator[bytes]:
        for _ in range(100):
            await asyncio.sleep(0.05)
            yield b" "


class _TrickleTransport(httpx.AsyncBaseTransport):
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, stream=_Trickle())


async def test_total_timeout_bounds_trickling_server() -> None:
    async with httpx.AsyncClient(transport=_TrickleTransport()) as client:
        provider = _anthropic(timeout=0.3, client=client)
        with pytest.raises(ProviderUnavailableError, match="zaman aşımı"):
            await _call(provider)


@pytest.mark.parametrize("base", ["http://an.test", "ftp://an.test", "an.test"])
async def test_key_never_sent_over_plain_http(router: respx.MockRouter, base: str) -> None:
    route = router.post(url__regex=r".*")
    with pytest.raises(ProviderConfigError):
        await _call(_anthropic(base=base))
    assert route.call_count == 0


async def test_plain_http_allowed_for_localhost(router: respx.MockRouter) -> None:
    route = router.post("http://localhost:8080/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
                "usage": {},
            },
        )
    )
    provider = OpenAICompatProvider(
        "gemini",
        GeminiConfig(base_url="http://localhost:8080", model="m"),
        token_field="max_tokens",
        seed=False,
        transport=HttpTransport("gemini", 30),
    )
    await provider.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert route.call_count == 1
    sent = json.loads(route.calls.last.request.content)
    assert sent["model"] == "m"
    assert route.calls.last.request.headers["authorization"].endswith(API_KEYS["GEMINI_API_KEY"])
