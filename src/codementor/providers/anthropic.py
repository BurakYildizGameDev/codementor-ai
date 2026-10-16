"""Anthropic Messages API adaptörü (ADR-0011).

Yapılandırılmış çıktı `output_config: {format: {type: "json_schema", schema}}` ile istenir;
beta başlığı gerekmez. Mimari ilk taslaktaki zorunlu `tool_choice` yolu güncel Claude
modellerinde 400 döndürdüğü için kullanılmaz. `temperature`/`seed` yalnızca yapılandırmada
açıkça verilmişse gönderilir (güncel modeller örnekleme parametrelerini reddeder).
Kaynak: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
"""

from __future__ import annotations

import time
from typing import Any

from pydantic import BaseModel

from codementor.config import ANTHROPIC_DEFAULT_MAX_TOKENS, ProviderConfig
from codementor.models.provider import (
    ChatMessage,
    GenerationOptions,
    ProviderCapabilities,
    ProviderResult,
    TokenUsage,
)
from codementor.providers._common import (
    api_key,
    as_int,
    as_text,
    elapsed_ms,
    field,
    merged,
    require_base_url,
    require_model,
)
from codementor.providers._http import HttpTransport, parse_json_object
from codementor.providers.base import (
    NamedProvider,
    ProviderConfigError,
    ProviderResponseError,
    RetryPolicy,
)
from codementor.providers.schema_adapter import SchemaAdapter

API_VERSION = "2023-06-01"  # Messages API protokol sürümü (başlık), model/URL değil


class AnthropicProvider(NamedProvider):
    """Claude modelleri."""

    name = "anthropic"
    capabilities = ProviderCapabilities(
        native_schema=True, strict_schema=True, seed=False, local=False
    )

    def __init__(
        self,
        config: ProviderConfig,
        *,
        retry: RetryPolicy | None = None,
        transport: HttpTransport | None = None,
    ) -> None:
        self.config = config
        self.transport = transport or HttpTransport(
            self.name, config.timeout_s, retry or RetryPolicy()
        )

    def build_payload(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> dict[str, Any]:
        """İstek gövdesi: sistem mesajları üst düzey `system` alanına taşınır."""
        opts = merged(options, self.config)
        system = "\n\n".join(m.content for m in messages if m.role == "system")
        turns = [m.model_dump() for m in messages if m.role != "system"]
        if not turns:
            raise ProviderConfigError(self.name, "en az bir kullanıcı mesajı gerekli")
        payload: dict[str, Any] = {
            "model": require_model(self.name, self.config),
            "max_tokens": opts.max_tokens or ANTHROPIC_DEFAULT_MAX_TOKENS,
            "messages": turns,
            "output_config": {
                "format": {"type": "json_schema", "schema": SchemaAdapter(output_model).anthropic()}
            },
        }
        if system:
            payload["system"] = system
        if opts.temperature is not None:
            payload["temperature"] = opts.temperature
        return payload

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> ProviderResult:
        payload = self.build_payload(messages, output_model, options)
        url = f"{require_base_url(self.name, self.config, carries_key=True)}/v1/messages"
        headers = {
            "x-api-key": api_key(self.name, self.config),
            "anthropic-version": API_VERSION,
        }
        start = time.perf_counter()
        data = await self.transport.post_json(url, payload, headers)
        blocks = field(self.name, data, "content") or []
        if not isinstance(blocks, list):
            raise ProviderResponseError(self.name, "beklenmeyen yanıt biçimi (content)")
        # düşünme blokları atlanır; yapılandırılmış JSON `text` bloklarındadır
        text = "".join(
            as_text(b.get("text"))
            for b in blocks
            if isinstance(b, dict) and b.get("type") == "text"
        )
        stop = as_text(data.get("stop_reason")) or None
        return ProviderResult(
            raw_text=text,
            parsed=None if stop == "refusal" else parse_json_object(text),
            usage=TokenUsage(
                input_tokens=as_int(field(self.name, data, "usage", "input_tokens")),
                output_tokens=as_int(field(self.name, data, "usage", "output_tokens")),
            ),
            latency_ms=elapsed_ms(start),
            model=as_text(data.get("model")) or payload["model"],
            finish_reason=stop,
            provider=self.name,
        )
