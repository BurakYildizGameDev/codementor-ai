"""FakeProvider: senaryo dosyası, gecikme, hata türleri, çağrı kaydı."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import (
    FakeProvider,
    FakeReply,
    ProviderConfigError,
    ProviderUnavailableError,
    RetryPolicy,
)
from tests.providers.contract import SleepRecorder

pytestmark = pytest.mark.anyio

MESSAGES = [ChatMessage(role="user", content="incele")]


async def test_from_file_plays_script_in_order(tmp_path: Path) -> None:
    path = tmp_path / "script.yaml"
    path.write_text(
        "- error: 500\n"
        "- delay_ms: 250\n"
        "  data: {key_flaw_concept: k, guiding_questions: ['?'], next_step_hint: null}\n"
        "- raw: '{bozuk'\n",
        encoding="utf-8",
    )
    sleep = SleepRecorder()
    fake = FakeProvider.from_file(
        path, retry=RetryPolicy(max_retries=2, base_delay_s=0, sleep=sleep)
    )
    first = await fake.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert first.parsed is not None
    assert first.latency_ms == 250
    assert 0.25 in sleep.delays  # gecikme simülasyonu enjekte edilen sleep ile
    second = await fake.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert second.parsed is None
    assert second.raw_text == "{bozuk"
    with pytest.raises(ProviderConfigError, match="senaryo bitti"):
        await fake.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())


async def test_calls_are_recorded() -> None:
    fake = FakeProvider(script=[FakeReply(data={})])
    options = GenerationOptions(temperature=0.1)
    await fake.generate_structured(MESSAGES, LLMSocraticOutput, options)
    assert fake.calls[0].messages == MESSAGES
    assert fake.calls[0].output_model is LLMSocraticOutput
    assert fake.calls[0].options == options


async def test_schema_enforced_defaults_false() -> None:
    """G7: şemayı sağlayıcı zorlamıyorsa alan varsayılan False kalır (fake şema zorlamaz)."""
    fake = FakeProvider(script=[FakeReply(data={})])
    result = await fake.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert result.schema_enforced is False


async def test_timeout_error_kind() -> None:
    fake = FakeProvider(script=[FakeReply(error="timeout")], retry=RetryPolicy(max_retries=0))
    with pytest.raises(ProviderUnavailableError, match="zaman aşımı"):
        await fake.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("a: 1\n", "liste"),
        ("- 3\n", "sözlük"),
        ("- error: 418\n", "bilinmeyen"),
        ("- foo: 1\n", "foo"),
    ],
)
def test_from_file_rejects_bad_script(tmp_path: Path, content: str, message: str) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ProviderConfigError, match=message):
        FakeProvider.from_file(path)


async def test_response_error_kind() -> None:
    from codementor.providers import ProviderResponseError

    fake = FakeProvider(script=[FakeReply(error="response")], retry=RetryPolicy(max_retries=2))
    with pytest.raises(ProviderResponseError):
        await fake.generate_structured(MESSAGES, LLMSocraticOutput, GenerationOptions())
    assert fake.attempts == 1  # yeniden denenmez


def test_negative_delay_rejected() -> None:
    with pytest.raises(ProviderConfigError, match="delay_ms"):
        FakeReply(delay_ms=-1)
