"""Ollama adaptörü (mimari §5.5.2): `POST /api/chat`, `format` = JSON Schema.

`options.num_ctx` her istekte gönderilir: Ollama'nın varsayılan bağlam penceresi küçüktür
ve uzun prompt sessizce kırpılır. Kaynak: https://docs.ollama.com/capabilities/structured-outputs
"""

from __future__ import annotations

import time
from typing import Any

from pydantic import BaseModel

from codementor.config import OllamaConfig, ProviderConfig
from codementor.models.provider import (
    ChatMessage,
    GenerationOptions,
    ProviderCapabilities,
    ProviderResult,
    TokenUsage,
)
from codementor.providers._common import (
    as_int,
    as_text,
    elapsed_ms,
    field,
    merged,
    require_base_url,
    require_model,
)
from codementor.providers._http import HttpTransport, parse_json_object
from codementor.providers.base import RetryPolicy
from codementor.providers.schema_adapter import SchemaAdapter

DEFAULT_NUM_CTX = OllamaConfig().num_ctx or 16384


class OllamaProvider:
    """Yerel Ollama sunucusu."""

    name = "ollama"
    capabilities = ProviderCapabilities(
        native_schema=True, strict_schema=False, seed=True, local=True
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
        """İstek gövdesi (testlerde de denetlenir)."""
        opts = merged(options, self.config)
        runtime: dict[str, Any] = {"num_ctx": self.config.num_ctx or DEFAULT_NUM_CTX}
        if opts.temperature is not None:
            runtime["temperature"] = opts.temperature
        if opts.seed is not None:
            runtime["seed"] = opts.seed
        if opts.max_tokens is not None:
            runtime["num_predict"] = opts.max_tokens
        return {
            "model": require_model(self.name, self.config),
            "messages": [m.model_dump() for m in messages],
            "stream": False,
            "format": SchemaAdapter(output_model).ollama(),
            "options": runtime,
        }

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> ProviderResult:
        payload = self.build_payload(messages, output_model, options)
        url = f"{require_base_url(self.name, self.config)}/api/chat"
        start = time.perf_counter()
        data = await self.transport.post_json(url, payload, {})
        text = as_text(field(self.name, data, "message", "content"))
        return ProviderResult(
            raw_text=text,
            parsed=parse_json_object(text),
            usage=TokenUsage(
                input_tokens=as_int(data.get("prompt_eval_count")),
                output_tokens=as_int(data.get("eval_count")),
            ),
            latency_ms=elapsed_ms(start),
            model=as_text(data.get("model")) or payload["model"],
            finish_reason=as_text(data.get("done_reason")) or None,
            provider=self.name,
        )

    async def list_models(self) -> list[str]:
        """Yerelde çekilmiş modeller (`GET /api/tags`)."""
        url = f"{require_base_url(self.name, self.config)}/api/tags"
        data = await self.transport.get_json(url)
        models = data.get("models")
        if not isinstance(models, list):
            return []
        return [m["name"] for m in models if isinstance(m, dict) and isinstance(m.get("name"), str)]
