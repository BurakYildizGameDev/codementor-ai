"""Sağlayıcıya özgü istek biçimleri: Ollama, OpenAI, DeepSeek, Anthropic (mimari §5.5.2)."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from codementor.config import AnthropicConfig, DeepSeekConfig, OllamaConfig, OpenAIConfig
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import ProviderConfigError
from codementor.providers._http import HttpTransport
from codementor.providers.anthropic import API_VERSION, AnthropicProvider
from codementor.providers.ollama import DEFAULT_NUM_CTX, OllamaProvider
from codementor.providers.openai_compat import OpenAICompatProvider
from codementor.providers.schema_adapter import SchemaAdapter
from tests.providers.contract import API_KEYS, anthropic_body, ollama_body, openai_body

pytestmark = pytest.mark.anyio

MESSAGES = [
    ChatMessage(role="system", content="Sistem talimatı."),
    ChatMessage(role="user", content="Kullanıcı mesajı."),
]
ANSWER = json.dumps({"key_flaw_concept": "k", "guiding_questions": ["?"], "next_step_hint": None})
OPTIONS = GenerationOptions()


def _transport(name: str) -> HttpTransport:
    return HttpTransport(name, 30)


def _sent(route: respx.Route) -> dict[str, object]:
    payload: dict[str, object] = json.loads(route.calls.last.request.content)
    return payload


# ---------------------------------------------------------------------------------- Ollama


async def test_ollama_format_is_json_schema(router: respx.MockRouter) -> None:
    route = router.post("http://o.test/api/chat").mock(
        return_value=httpx.Response(200, json=ollama_body(ANSWER, "m"))
    )
    provider = OllamaProvider(
        OllamaConfig(base_url="http://o.test", model="m"), transport=_transport("ollama")
    )
    await provider.generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)
    sent = _sent(route)
    assert sent["format"] == SchemaAdapter(LLMSocraticOutput).ollama()
    assert sent["stream"] is False
    assert sent["messages"] == [m.model_dump() for m in MESSAGES]


@pytest.mark.parametrize("configured", [None, 4096, 32768])
async def test_ollama_num_ctx_always_sent(router: respx.MockRouter, configured: int | None) -> None:
    route = router.post("http://o.test/api/chat").mock(
        return_value=httpx.Response(200, json=ollama_body(ANSWER, "m"))
    )
    cfg = OllamaConfig(base_url="http://o.test", model="m", num_ctx=configured)
    await OllamaProvider(cfg, transport=_transport("ollama")).generate_structured(
        MESSAGES, LLMSocraticOutput, OPTIONS
    )
    options = _sent(route)["options"]
    assert isinstance(options, dict)
    assert options["num_ctx"] == (configured or DEFAULT_NUM_CTX)


def test_ollama_options_temperature_seed_and_override() -> None:
    cfg = OllamaConfig(model="m", temperature=0.1, seed=42)
    provider = OllamaProvider(cfg)
    options = provider.build_payload(MESSAGES, LLMSocraticOutput, OPTIONS)["options"]
    assert options == {"num_ctx": 16384, "temperature": 0.1, "seed": 42}
    override = GenerationOptions(temperature=0.0, max_tokens=500)
    options = provider.build_payload(MESSAGES, LLMSocraticOutput, override)["options"]
    assert options["temperature"] == 0.0
    assert options["num_predict"] == 500


async def test_ollama_list_models(router: respx.MockRouter) -> None:
    router.get("http://o.test/api/tags").mock(
        return_value=httpx.Response(200, json={"models": [{"name": "qwen2.5-coder:7b"}, {}]})
    )
    provider = OllamaProvider(OllamaConfig(base_url="http://o.test", model="m"))
    assert await provider.list_models() == ["qwen2.5-coder:7b"]


# ---------------------------------------------------------------------- OpenAI / DeepSeek


def _openai(mode: str = "strict_schema") -> OpenAICompatProvider:
    if mode == "strict_schema":
        cfg = OpenAIConfig(base_url="https://oa.test/v1", model="m", seed=7, max_tokens=900)
        return OpenAICompatProvider(
            "openai", cfg, mode="strict_schema", transport=_transport("openai")
        )
    cfg2 = DeepSeekConfig(base_url="https://ds.test", model="m", seed=7, max_tokens=900)
    return OpenAICompatProvider("deepseek", cfg2, mode="json_object", transport=_transport("ds"))


def test_openai_response_format_strict() -> None:
    payload = _openai().build_payload(MESSAGES, LLMSocraticOutput, OPTIONS)
    fmt = payload["response_format"]
    assert fmt == {
        "type": "json_schema",
        "json_schema": {
            "name": "LLMSocraticOutput",
            "schema": SchemaAdapter(LLMSocraticOutput).openai_strict(),
            "strict": True,
        },
    }
    assert payload["seed"] == 7
    assert payload["max_completion_tokens"] == 900
    assert payload["messages"] == [m.model_dump() for m in MESSAGES]


async def test_openai_bearer_header(router: respx.MockRouter) -> None:
    route = router.post("https://oa.test/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=openai_body(ANSWER, "m"))
    )
    await _openai().generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)
    headers = route.calls.last.request.headers
    assert headers["authorization"] == f"Bearer {API_KEYS['OPENAI_API_KEY']}"


async def test_openai_refusal_gives_no_parsed(router: respx.MockRouter) -> None:
    body = openai_body("", "m")
    body["choices"][0]["message"] = {"role": "assistant", "content": None, "refusal": "Hayır."}
    router.post("https://oa.test/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=body)
    )
    result = await _openai().generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert result.parsed is None
    assert result.finish_reason == "refusal"
    assert result.raw_text == "Hayır."


def test_deepseek_json_object_and_schema_in_prompt() -> None:
    payload = _openai("json_object").build_payload(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert payload["response_format"] == {"type": "json_object"}
    messages = payload["messages"]
    assert isinstance(messages, list)
    last = messages[-1]
    assert last["role"] == "system"
    assert "json" in last["content"]  # DeepSeek JSON modu "json" sözcüğünü şart koşar
    assert '"guiding_questions"' in last["content"]
    assert payload["max_tokens"] == 900
    assert "seed" not in payload
    assert "max_completion_tokens" not in payload


async def test_missing_api_key(monkeypatch: pytest.MonkeyPatch, router: respx.MockRouter) -> None:
    monkeypatch.delenv("OPENAI_API_KEY")
    route = router.post("https://oa.test/v1/chat/completions")
    with pytest.raises(ProviderConfigError, match="OPENAI_API_KEY"):
        await _openai().generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert route.call_count == 0


# ------------------------------------------------------------------------------- Anthropic


def _anthropic(**overrides: object) -> AnthropicProvider:
    cfg = AnthropicConfig(base_url="https://an.test", model="m", **overrides)  # type: ignore[arg-type]
    return AnthropicProvider(cfg, transport=_transport("anthropic"))


def test_anthropic_output_config_format_schema() -> None:
    payload = _anthropic().build_payload(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert payload["output_config"] == {
        "format": {"type": "json_schema", "schema": SchemaAdapter(LLMSocraticOutput).anthropic()}
    }


def test_anthropic_no_tools_no_tool_choice() -> None:
    payload = _anthropic().build_payload(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert "tools" not in payload
    assert "tool_choice" not in payload


def test_anthropic_system_message_top_level() -> None:
    payload = _anthropic().build_payload(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert payload["system"] == "Sistem talimatı."
    assert payload["messages"] == [{"role": "user", "content": "Kullanıcı mesajı."}]
    assert payload["max_tokens"] == 16000


def test_anthropic_temperature_only_if_configured() -> None:
    payload = _anthropic().build_payload(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert "temperature" not in payload
    assert "seed" not in payload
    payload = _anthropic(temperature=0.2).build_payload(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert payload["temperature"] == 0.2


def test_anthropic_requires_user_turn() -> None:
    with pytest.raises(ProviderConfigError):
        _anthropic().build_payload(MESSAGES[:1], LLMSocraticOutput, OPTIONS)


async def test_anthropic_headers_version_and_key(router: respx.MockRouter) -> None:
    route = router.post("https://an.test/v1/messages").mock(
        return_value=httpx.Response(200, json=anthropic_body(ANSWER, "m"))
    )
    await _anthropic().generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)
    headers = route.calls.last.request.headers
    assert headers["x-api-key"] == API_KEYS["ANTHROPIC_API_KEY"]
    assert headers["anthropic-version"] == API_VERSION
    assert "anthropic-beta" not in headers


async def test_anthropic_text_block_after_thinking(router: respx.MockRouter) -> None:
    router.post("https://an.test/v1/messages").mock(
        return_value=httpx.Response(200, json=anthropic_body(ANSWER, "m"))
    )
    result = await _anthropic().generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert result.parsed is not None
    assert result.finish_reason == "end_turn"


@pytest.mark.parametrize(("stop", "parsed"), [("refusal", False), ("max_tokens", False)])
async def test_anthropic_refusal_and_max_tokens(
    router: respx.MockRouter, stop: str, parsed: bool
) -> None:
    text = ANSWER if stop == "refusal" else ANSWER[:20]
    body = anthropic_body(text, "m") | {"stop_reason": stop}
    router.post("https://an.test/v1/messages").mock(return_value=httpx.Response(200, json=body))
    result = await _anthropic().generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert (result.parsed is not None) is parsed
    assert result.finish_reason == stop


async def test_unexpected_shape_is_response_error(router: respx.MockRouter) -> None:
    from codementor.providers import ProviderResponseError

    router.post("https://an.test/v1/messages").mock(
        return_value=httpx.Response(200, json={"content": "düz metin"})
    )
    with pytest.raises(ProviderResponseError):
        await _anthropic().generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)


async def test_non_json_body_not_retried(router: respx.MockRouter) -> None:
    from codementor.providers import ProviderResponseError

    route = router.post("https://an.test/v1/messages").mock(
        return_value=httpx.Response(200, text="<html>proxy</html>")
    )
    with pytest.raises(ProviderResponseError):
        await _anthropic().generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)
    assert route.call_count == 1


async def test_oversized_response_rejected(
    router: respx.MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    from codementor.providers import ProviderResponseError, _http

    monkeypatch.setattr(_http, "MAX_RESPONSE_BYTES", 100)
    router.post("https://an.test/v1/messages").mock(
        return_value=httpx.Response(200, json=anthropic_body("x" * 500, "m"))
    )
    with pytest.raises(ProviderResponseError, match="boyut"):
        await _anthropic().generate_structured(MESSAGES, LLMSocraticOutput, OPTIONS)


@pytest.mark.parametrize("think", [None, False, True])
def test_ollama_think_only_if_configured(think: bool | None) -> None:
    payload = OllamaProvider(OllamaConfig(model="m", think=think)).build_payload(
        MESSAGES, LLMSocraticOutput, OPTIONS
    )
    if think is None:
        assert "think" not in payload
    else:
        assert payload["think"] is think
