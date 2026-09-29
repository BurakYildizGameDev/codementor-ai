"""API anahtarları hiçbir log satırında görünmez (mimari §5.5.3, §12)."""

from __future__ import annotations

import io
import json
import logging
from collections.abc import Iterator

import httpx
import pytest
import respx
import structlog

from codementor.config import AnthropicConfig, OpenAIConfig
from codementor.log import MASK, configure_logging, get_logger, register_secret, scrub
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import ProviderRequestError, ProviderServerError, RetryPolicy
from codementor.providers._http import HttpTransport
from codementor.providers.anthropic import AnthropicProvider
from codementor.providers.openai_compat import OpenAICompatProvider
from tests.providers.contract import API_KEYS, SleepRecorder, anthropic_body

pytestmark = pytest.mark.anyio

MESSAGES = [ChatMessage(role="user", content="incele")]


@pytest.fixture
def captured() -> Iterator[io.StringIO]:
    stream = io.StringIO()
    configure_logging(stream, level=logging.DEBUG)
    yield stream
    configure_logging()  # varsayılan ayarlara dön (stderr, WARNING)


def _anthropic() -> AnthropicProvider:
    return AnthropicProvider(
        AnthropicConfig(base_url="https://an.test", model="m"),
        transport=HttpTransport("anthropic", 30, RetryPolicy(max_retries=1, sleep=SleepRecorder())),
    )


async def test_api_key_never_in_logs(captured: io.StringIO, router: respx.MockRouter) -> None:
    key = API_KEYS["ANTHROPIC_API_KEY"]
    # hata gövdesi anahtarı yansıtsa bile (kötü davranan vekil sunucu) sızmamalı
    echo = {"error": {"message": f"geçersiz anahtar {key} Bearer {key}"}}
    router.post("https://an.test/v1/messages").mock(
        side_effect=[
            httpx.Response(500, json=echo),
            httpx.Response(200, json=anthropic_body("{}", "m")),
            httpx.Response(401, json=echo),
        ]
    )
    provider = _anthropic()
    await provider.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    with pytest.raises(ProviderRequestError) as info:
        await provider.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    log = get_logger("test")
    log.info("başlıklar", headers={"x-api-key": key, "Authorization": f"Bearer {key}"})
    log.error("hata", error=str(info.value), exc_info=info.value)
    output = captured.getvalue()
    assert output.count("\n") >= 5
    assert key not in output
    assert key not in str(info.value)


async def test_error_message_body_is_scrubbed(router: respx.MockRouter) -> None:
    key = API_KEYS["OPENAI_API_KEY"]
    router.post("https://oa.test/v1/chat/completions").mock(
        return_value=httpx.Response(503, json={"error": {"message": f"anahtar: {key}"}})
    )
    provider = OpenAICompatProvider(
        "openai",
        OpenAIConfig(base_url="https://oa.test/v1", model="m"),
        mode="strict_schema",
        transport=HttpTransport("openai", 30, RetryPolicy(max_retries=0)),
    )
    with pytest.raises(ProviderServerError) as info:
        await provider.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert key not in str(info.value)


def test_authorization_redacted(captured: io.StringIO) -> None:
    get_logger("test").info(
        "istek", authorization="Bearer abcdefgh12345678", api_key="xyz", status=200
    )
    line = json.loads(captured.getvalue().splitlines()[-1])
    assert line["authorization"] == MASK
    assert line["api_key"] == MASK
    assert line["status"] == 200


def test_nested_and_pattern_redaction() -> None:
    register_secret("gizli-deger-123456789")
    data = {
        "outer": [{"X-Api-Key": "k"}, "metin gizli-deger-123456789 son"],
        "note": "Bearer eyJhbGciOiJIUzI1NiJ9.payload ve sk-proj-ABCDEFGHIJ1234",
        "tuple": ("sk-ant-api03-ZZZZZZZZZZZZ",),
        "count": 3,
    }
    cleaned = scrub(data)
    assert cleaned["outer"][0]["X-Api-Key"] == MASK
    assert cleaned["outer"][1] == f"metin {MASK} son"
    assert "eyJ" not in cleaned["note"]
    assert "ABCDEFGHIJ" not in cleaned["note"]
    assert cleaned["tuple"] == (MASK,)
    assert cleaned["count"] == 3


def test_short_values_not_registered() -> None:
    register_secret("abc")
    assert scrub("abc def") == "abc def"


def test_token_counters_not_masked(captured: io.StringIO) -> None:
    # denetim O5: `token` alt dizesi sayaçları da maskeliyordu (mimari §13 token muhasebesi)
    get_logger("test").info(
        "kullanım", input_tokens=120, output_tokens=40, max_tokens=900, access_token="gizli"
    )
    line = json.loads(captured.getvalue().splitlines()[-1])
    assert (line["input_tokens"], line["output_tokens"], line["max_tokens"]) == (120, 40, 900)
    assert line["access_token"] == MASK


@pytest.mark.parametrize(
    "key",
    [
        "Authorization",
        "proxy-authorization",
        "x-api-key",
        "api_key",
        "client_secret",
        "password",
        "token",
        "refresh_token",
        "session-token",
    ],
)
def test_secret_key_names(key: str) -> None:
    assert scrub({key: "deger"})[key] == MASK


@pytest.mark.parametrize("key", ["input_tokens", "max_tokens", "token_count", "tokenizer"])
def test_non_secret_key_names(key: str) -> None:
    assert scrub({key: 5})[key] == 5


def test_redaction_survives_foreign_structlog_config(captured: io.StringIO) -> None:
    # denetim O6: başka bir kod structlog'u maskelemesiz yeniden kurarsa sızıyordu
    structlog.reset_defaults()
    structlog.configure(processors=[structlog.processors.JSONRenderer()])
    key = "sk-foreign-config-SECRET-123456"
    get_logger("test").warning("istek", authorization=f"Bearer {key}", note=f"anahtar {key}")
    output = captured.getvalue()
    assert output
    assert key not in output


def test_mapping_keys_are_scrubbed() -> None:
    register_secret("anahtar-olarak-sir-123456")
    cleaned = scrub({"anahtar-olarak-sir-123456": 1})
    assert list(cleaned) == [MASK]
