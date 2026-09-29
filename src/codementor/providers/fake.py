"""Testler ve CI için ağsız sağlayıcı (mimari §5.5.2 "Fake", AGENTS.md kural 4).

Senaryo sırayla oynatılır; her adım bir yanıt (`data` ya da ham `raw` metin) ya da hata
(`429`, `500`, `529`, `400`, `401`, `network`, `timeout`) üretir. Hatalar gerçek adaptörlerle
aynı sınıflardır ve aynı `RetryPolicy` ile yeniden denenir; böylece sözleşme testleri Fake'i de
kapsar. `delay_ms` gecikme simülasyonudur (enjekte edilen `sleep` ile beklenir).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, get_args

import yaml
from pydantic import BaseModel

from codementor.models.provider import (
    ChatMessage,
    GenerationOptions,
    ProviderCapabilities,
    ProviderResult,
    TokenUsage,
)
from codementor.providers._http import parse_json_object
from codementor.providers.base import (
    ProviderConfigError,
    ProviderError,
    ProviderRateLimitError,
    ProviderRequestError,
    ProviderResponseError,
    ProviderServerError,
    ProviderUnavailableError,
    RetryPolicy,
)

FakeErrorKind = Literal[
    "429", "500", "529", "400", "401", "403", "404", "422", "network", "timeout", "response"
]
_ERRORS: frozenset[str] = frozenset(get_args(FakeErrorKind))


@dataclass(frozen=True)
class FakeReply:
    """Senaryonun bir adımı."""

    data: dict[str, Any] | None = None
    raw: str | None = None
    error: FakeErrorKind | None = None
    delay_ms: int = 0
    finish_reason: str | None = "stop"
    retry_after: float | None = None

    def __post_init__(self) -> None:
        if self.delay_ms < 0:
            raise ProviderConfigError("fake", "delay_ms negatif olamaz")

    def text(self) -> str:
        if self.raw is not None:
            return self.raw
        return json.dumps(self.data if self.data is not None else {}, ensure_ascii=False)


@dataclass
class FakeCall:
    """Kaydedilen çağrı (testler prompt'u ve modeli denetler)."""

    messages: list[ChatMessage]
    output_model: type[BaseModel]
    options: GenerationOptions


@dataclass
class FakeProvider:
    """Senaryodan yanıt veren sağlayıcı."""

    script: list[FakeReply]
    name: str = "fake"
    model: str = "fake-model"
    retry: RetryPolicy = field(default_factory=RetryPolicy)
    capabilities: ProviderCapabilities = field(
        default_factory=lambda: ProviderCapabilities(
            native_schema=True, strict_schema=True, seed=True, local=True
        )
    )
    calls: list[FakeCall] = field(default_factory=list)
    attempts: int = 0
    _position: int = 0

    @classmethod
    def from_file(cls, path: Path, **kwargs: Any) -> FakeProvider:
        """YAML/JSON senaryo dosyası: `FakeReply` alanlarından oluşan liste."""
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, list):
            raise ProviderConfigError("fake", f"{path.name}: senaryo bir liste olmalı")
        replies: list[FakeReply] = []
        for index, item in enumerate(loaded):
            if not isinstance(item, dict):
                raise ProviderConfigError("fake", f"{path.name}[{index}]: adım bir sözlük olmalı")
            if item.get("error") is not None:
                item = {**item, "error": str(item["error"])}
                if item["error"] not in _ERRORS:
                    raise ProviderConfigError("fake", f"{path.name}[{index}]: bilinmeyen hata")
            try:
                replies.append(FakeReply(**item))
            except TypeError as exc:
                raise ProviderConfigError("fake", f"{path.name}[{index}]: {exc}") from exc
        return cls(script=replies, **kwargs)

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> ProviderResult:
        if not self.model.strip():
            raise ProviderConfigError(self.name, "model tanımlı değil")
        self.calls.append(FakeCall(list(messages), output_model, options))
        return await self.retry.run(self._step)

    async def _step(self) -> ProviderResult:
        self.attempts += 1
        if self._position >= len(self.script):
            raise ProviderConfigError(self.name, "senaryo bitti")
        reply = self.script[self._position]
        self._position += 1
        if reply.delay_ms:
            await self.retry.sleep(reply.delay_ms / 1000)
        if reply.error is not None:
            raise _error(self.name, reply)
        text = reply.text()
        return ProviderResult(
            raw_text=text,
            parsed=parse_json_object(text),
            usage=TokenUsage(input_tokens=0, output_tokens=len(text) // 4, estimated=True),
            latency_ms=reply.delay_ms,
            model=self.model,
            finish_reason=reply.finish_reason,
            provider=self.name,
        )


def _error(name: str, reply: FakeReply) -> ProviderError:
    kind = reply.error
    if kind == "429":
        return ProviderRateLimitError(name, "hız sınırı (429)", retry_after=reply.retry_after)
    if kind in ("500", "529"):
        return ProviderServerError(name, f"sunucu hatası ({kind})", status=int(kind))
    if kind in ("400", "401", "403", "404", "422"):
        return ProviderRequestError(name, f"istek reddedildi ({kind})", status=int(kind))
    if kind == "timeout":
        return ProviderUnavailableError(name, "zaman aşımı")
    if kind == "response":
        return ProviderResponseError(name, "yanıt gövdesi JSON değil")
    return ProviderUnavailableError(name, "bağlantı kurulamadı")
