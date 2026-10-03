"""Faz 28: bulut API hata gövdeleri → Türkçe, eyleme dönük hata ve doğru yeniden deneme kararı.

Gövdeler sağlayıcıların belgelediği biçimlerdedir (OpenAI `error.code/type`, DeepSeek 402,
Gemini OpenAI uyumlu uçta liste sarmalı ve `status`). Ağa çıkılmaz (respx).
"""

from __future__ import annotations

from typing import Any

import httpx
import pytest
import respx

from codementor.config import OpenAIConfig
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import (
    ProviderError,
    ProviderRateLimitError,
    ProviderRequestError,
    ProviderServerError,
    RetryPolicy,
)
from codementor.providers._http import HttpTransport
from codementor.providers.openai_compat import OpenAICompatProvider
from tests.providers.contract import SleepRecorder

pytestmark = pytest.mark.anyio
URL = "https://oa.test/v1/chat/completions"
MESSAGES = [ChatMessage(role="user", content="x")]


def _provider(sleep: SleepRecorder) -> OpenAICompatProvider:
    retry = RetryPolicy(max_retries=2, base_delay_s=0.01, sleep=sleep)
    return OpenAICompatProvider(
        "openai",
        OpenAIConfig(base_url="https://oa.test/v1", model="m"),
        mode="strict_schema",
        transport=HttpTransport("openai", 30, retry),
    )


async def _fail(router: respx.MockRouter, sleep: SleepRecorder, status: int, body: Any) -> Any:
    route = router.post(URL).mock(return_value=httpx.Response(status, json=body))
    with pytest.raises(ProviderError) as info:
        await _provider(sleep).generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    return info.value, route.call_count


def _openai_error(
    message: str, code: str | None = None, kind: str = "invalid_request_error"
) -> dict[str, Any]:
    return {"error": {"message": message, "type": kind, "param": None, "code": code}}


async def test_insufficient_quota_not_retried(
    router: respx.MockRouter, sleep: SleepRecorder
) -> None:
    body = _openai_error(
        "You exceeded your current quota, please check your plan and billing details.",
        code="insufficient_quota",
        kind="insufficient_quota",
    )
    exc, calls = await _fail(router, sleep, 429, body)
    assert isinstance(exc, ProviderRequestError)
    assert not isinstance(exc, ProviderRateLimitError)
    assert calls == 1  # kota yeniden denemeyle düzelmez
    assert sleep.delays == []
    assert exc.status == 429
    assert "kota" in str(exc)
    assert "billing" in str(exc)  # sağlayıcının kendi açıklaması da görünür


async def test_gemini_daily_quota_not_retried(
    router: respx.MockRouter, sleep: SleepRecorder
) -> None:
    body = [{"error": {"code": 429, "message": "Daily quota exceeded", "status": "quota_exceeded"}}]
    exc, calls = await _fail(router, sleep, 429, body)
    assert isinstance(exc, ProviderRequestError)
    assert calls == 1
    assert "Daily quota exceeded" in str(exc)


async def test_rate_limit_still_retried(router: respx.MockRouter, sleep: SleepRecorder) -> None:
    body = _openai_error("Rate limit reached for requests", code="rate_limit_exceeded")
    exc, calls = await _fail(router, sleep, 429, body)
    assert isinstance(exc, ProviderRateLimitError)
    assert calls == 3


@pytest.mark.parametrize(
    ("status", "body", "expected"),
    [
        (401, _openai_error("Incorrect API key provided: sk-...", "invalid_api_key"), "anahtar"),
        (402, {"error": {"message": "Insufficient Balance"}}, "bakiye"),
        (403, _openai_error("Project does not have access to model m"), "yetki"),
        (404, _openai_error("The model `m` does not exist", "model_not_found"), "model"),
    ],
)
async def test_actionable_turkish_messages(
    router: respx.MockRouter,
    sleep: SleepRecorder,
    status: int,
    body: dict[str, Any],
    expected: str,
) -> None:
    exc, calls = await _fail(router, sleep, status, body)
    assert isinstance(exc, ProviderRequestError)
    assert calls == 1
    assert exc.status == status
    assert expected in str(exc)
    assert f"({status})" in str(exc)


async def test_auth_error_detail_is_masked(router: respx.MockRouter, sleep: SleepRecorder) -> None:
    key = "sk-test-openai-SECRET-0123456789"  # conftest ile ortamdaki anahtar
    body = _openai_error(f"Incorrect API key provided: {key}", "invalid_api_key")
    exc, _ = await _fail(router, sleep, 401, body)
    assert "SECRET" not in str(exc)


async def test_list_wrapped_error_body_message_shown(
    router: respx.MockRouter, sleep: SleepRecorder
) -> None:
    """Gemini OpenAI uyumlu uç, hata gövdesini bazen tek öğeli liste olarak döndürür."""
    body = [
        {"error": {"code": 400, "message": "Invalid JSON payload", "status": "INVALID_ARGUMENT"}}
    ]
    exc, _ = await _fail(router, sleep, 400, body)
    assert "Invalid JSON payload" in str(exc)
    assert "[{" not in str(exc)


async def test_server_overload_retried(router: respx.MockRouter, sleep: SleepRecorder) -> None:
    exc, calls = await _fail(router, sleep, 503, {"error": {"message": "overloaded"}})
    assert isinstance(exc, ProviderServerError)
    assert calls == 3
