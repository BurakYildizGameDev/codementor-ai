"""Tüm sağlayıcı adaptörlerinin geçtiği ortak sözleşme düzeneği (mimari §15).

Her adaptör için bir `Harness`, sağlayıcıya özgü yanıt gövdesini ve HTTP taklidini (respx)
gizler; `test_contract.py` aynı testleri beşine de uygular. Ağa çıkılmaz.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol

import httpx
import respx

from codementor.config import AnthropicConfig, DeepSeekConfig, OllamaConfig, OpenAIConfig
from codementor.providers import FakeProvider, FakeReply, RetryPolicy
from codementor.providers._http import HttpTransport
from codementor.providers.anthropic import AnthropicProvider
from codementor.providers.base import LLMProvider
from codementor.providers.ollama import OllamaProvider
from codementor.providers.openai_compat import OpenAICompatProvider

API_KEYS = {
    "OPENAI_API_KEY": "sk-test-openai-SECRET-0123456789",
    "DEEPSEEK_API_KEY": "sk-test-deepseek-SECRET-0123456789",
    "ANTHROPIC_API_KEY": "sk-ant-test-SECRET-0123456789",
}


@dataclass(frozen=True)
class Ok:
    data: dict[str, Any] | None = None
    raw: str | None = None

    def text(self) -> str:
        return self.raw if self.raw is not None else json.dumps(self.data)


@dataclass(frozen=True)
class Status:
    code: int
    headers: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Network:
    pass


@dataclass(frozen=True)
class Timeout:
    pass


Step = Ok | Status | Network | Timeout


@dataclass
class SleepRecorder:
    delays: list[float] = field(default_factory=list)

    async def __call__(self, seconds: float) -> None:
        self.delays.append(seconds)


def retry_policy(sleep: SleepRecorder) -> RetryPolicy:
    return RetryPolicy(max_retries=2, base_delay_s=0.01, max_delay_s=5.0, sleep=sleep)


class Harness(Protocol):
    name: str
    expected_usage: tuple[int, int] | None

    def make(self, model: str = "test-model") -> LLMProvider: ...
    def script(self, steps: list[Step]) -> None: ...
    @property
    def request_count(self) -> int: ...
    @property
    def sent_model(self) -> str: ...


# ------------------------------------------------------------------------ HTTP adaptörleri

BodyBuilder = Callable[[str, str], dict[str, Any]]


def ollama_body(text: str, model: str) -> dict[str, Any]:
    return {
        "model": model,
        "message": {"role": "assistant", "content": text},
        "done": True,
        "done_reason": "stop",
        "prompt_eval_count": 10,
        "eval_count": 5,
    }


def openai_body(text: str, model: str) -> dict[str, Any]:
    return {
        "model": model,
        "choices": [{"message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5},
    }


def anthropic_body(text: str, model: str) -> dict[str, Any]:
    return {
        "model": model,
        "content": [{"type": "thinking", "thinking": ""}, {"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 10, "output_tokens": 5},
    }


@dataclass
class HttpHarness:
    name: str
    url: str
    body: BodyBuilder
    factory: Callable[[str, RetryPolicy], LLMProvider]
    router: respx.MockRouter
    sleep: SleepRecorder
    expected_usage: tuple[int, int] | None = (10, 5)
    route: respx.Route | None = None

    def make(self, model: str = "test-model") -> LLMProvider:
        return self.factory(model, retry_policy(self.sleep))

    def script(self, steps: list[Step]) -> None:
        effects: list[Any] = []
        for step in steps:
            if isinstance(step, Ok):
                effects.append(httpx.Response(200, json=self.body(step.text(), "served-model")))
            elif isinstance(step, Status):
                body = {"error": {"type": "error", "message": f"durum {step.code}"}}
                effects.append(httpx.Response(step.code, json=body, headers=step.headers))
            elif isinstance(step, Network):
                effects.append(httpx.ConnectError("bağlantı reddedildi"))
            else:
                effects.append(httpx.ReadTimeout("zaman aşımı"))
        self.route = self.router.post(self.url).mock(side_effect=effects)

    @property
    def request_count(self) -> int:
        return self.route.call_count if self.route is not None else 0

    @property
    def sent_model(self) -> str:
        return str(self.last_payload["model"])

    @property
    def last_payload(self) -> dict[str, Any]:
        assert self.route is not None
        payload: dict[str, Any] = json.loads(self.route.calls.last.request.content)
        return payload


def http_harness(name: str, router: respx.MockRouter, sleep: SleepRecorder) -> HttpHarness:
    def transport(label: str, timeout: int, retry: RetryPolicy) -> HttpTransport:
        return HttpTransport(label, timeout, retry)

    if name == "ollama":
        return HttpHarness(
            name,
            "http://ollama.test/api/chat",
            ollama_body,
            lambda model, retry: OllamaProvider(
                OllamaConfig(base_url="http://ollama.test", model=model),
                transport=transport(name, 120, retry),
            ),
            router,
            sleep,
        )
    if name == "openai":
        return HttpHarness(
            name,
            "https://openai.test/v1/chat/completions",
            openai_body,
            lambda model, retry: OpenAICompatProvider(
                name,
                OpenAIConfig(base_url="https://openai.test/v1", model=model),
                mode="strict_schema",
                transport=transport(name, 60, retry),
            ),
            router,
            sleep,
        )
    if name == "deepseek":
        return HttpHarness(
            name,
            "https://deepseek.test/chat/completions",
            openai_body,
            lambda model, retry: OpenAICompatProvider(
                name,
                DeepSeekConfig(base_url="https://deepseek.test", model=model),
                mode="json_object",
                transport=transport(name, 60, retry),
            ),
            router,
            sleep,
        )
    assert name == "anthropic"
    return HttpHarness(
        name,
        "https://anthropic.test/v1/messages",
        anthropic_body,
        lambda model, retry: AnthropicProvider(
            AnthropicConfig(base_url="https://anthropic.test", model=model),
            transport=transport(name, 60, retry),
        ),
        router,
        sleep,
    )


# ------------------------------------------------------------------------------- Fake


@dataclass
class FakeHarness:
    sleep: SleepRecorder
    name: str = "fake"
    expected_usage: tuple[int, int] | None = None
    replies: list[FakeReply] = field(default_factory=list)
    provider: FakeProvider | None = None

    def make(self, model: str = "test-model") -> LLMProvider:
        self.provider = FakeProvider(
            script=self.replies, model=model, retry=retry_policy(self.sleep)
        )
        return self.provider

    def script(self, steps: list[Step]) -> None:
        self.replies.clear()
        for step in steps:
            if isinstance(step, Ok):
                self.replies.append(FakeReply(data=step.data, raw=step.raw))
            elif isinstance(step, Status):
                self.replies.append(
                    FakeReply(
                        # durum kodu FakeErrorKind değerlerinden biri (Literal; mypy daraltamaz)
                        error=str(step.code),  # type: ignore[arg-type]
                        retry_after=_seconds(step.headers.get("retry-after")),
                    )
                )
            elif isinstance(step, Network):
                self.replies.append(FakeReply(error="network"))
            else:
                self.replies.append(FakeReply(error="timeout"))

    @property
    def request_count(self) -> int:
        return self.provider.attempts if self.provider is not None else 0

    @property
    def sent_model(self) -> str:
        assert self.provider is not None
        return self.provider.model


HARNESS_NAMES = ["fake", "ollama", "openai", "deepseek", "anthropic"]


def _seconds(value: str | None) -> float | None:
    """Retry-After başlığını Fake'e aktarır; tarih biçimi HTTP katmanındaki gibi yok sayılır."""
    try:
        return float(value) if value is not None else None
    except ValueError:
        return None
