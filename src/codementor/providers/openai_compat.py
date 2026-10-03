"""OpenAI uyumlu Chat Completions adaptörü: OpenAI ve Gemini (katı şema), DeepSeek (JSON modu).

- OpenAI: `response_format: {type: "json_schema", json_schema: {name, schema, strict: true}}`.
  Katı modda tüm alanlar zorunlu, `additionalProperties: false`, opsiyonel = `anyOf[T, null]`.
  Kaynak: https://developers.openai.com/api/docs/guides/structured-outputs
- DeepSeek: yalnızca `response_format: {type: "json_object"}`; şema ve "json" sözcüğü prompt'ta
  olmalı, doğrulama tamamen Pydantic'e düşer. Kaynak: https://api-docs.deepseek.com/guides/json_mode
- Gemini (ADR-0020): `.../v1beta/openai` ucu OpenAI SDK'nın `parse()` biçimini (katı
  `json_schema`) kabul eder; çıktı sınırı `max_tokens` ile verilir, `seed` gönderilmez.
  Kaynak: https://ai.google.dev/gemini-api/docs/openai
"""

from __future__ import annotations

import time
from typing import Any, Literal

from pydantic import BaseModel

from codementor.config import ProviderConfig
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
from codementor.providers.base import RetryPolicy
from codementor.providers.schema_adapter import SchemaAdapter

Mode = Literal["strict_schema", "json_object"]
TokenField = Literal["max_completion_tokens", "max_tokens"]


class OpenAICompatProvider:
    """OpenAI / Gemini (`strict_schema`) ya da DeepSeek (`json_object`) modu.

    `token_field`: çıktı sınırının alan adı (OpenAI `max_completion_tokens`, diğerleri
    `max_tokens`); `seed`: sağlayıcı belgeliyorsa ve yapılandırmada verildiyse gönderilir.
    """

    def __init__(
        self,
        name: str,
        config: ProviderConfig,
        *,
        mode: Mode,
        token_field: TokenField | None = None,
        seed: bool | None = None,
        retry: RetryPolicy | None = None,
        transport: HttpTransport | None = None,
    ) -> None:
        self.name = name
        self.config = config
        self.mode = mode
        strict = mode == "strict_schema"
        self.token_field: TokenField = token_field or (
            "max_completion_tokens" if strict else "max_tokens"
        )
        self.capabilities = ProviderCapabilities(
            native_schema=strict,
            strict_schema=strict,
            seed=strict if seed is None else seed,
            local=False,
        )
        self.transport = transport or HttpTransport(name, config.timeout_s, retry or RetryPolicy())

    def build_payload(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> dict[str, Any]:
        """İstek gövdesi (testlerde de denetlenir)."""
        opts = merged(options, self.config)
        adapter = SchemaAdapter(output_model)
        wire = [m.model_dump() for m in messages]
        payload: dict[str, Any] = {"model": require_model(self.name, self.config)}
        if self.mode == "strict_schema":
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": output_model.__name__[:64],
                    "schema": adapter.openai_strict(),
                    "strict": True,
                },
            }
        else:
            # "json" sözcüğü + şema + örnek biçim prompt'ta olmalı (DeepSeek JSON modu)
            wire.append(
                {"role": "system", "content": f"Output json only.\n{adapter.prompt_text()}"}
            )
            payload["response_format"] = {"type": "json_object"}
        if opts.max_tokens is not None:
            payload[self.token_field] = opts.max_tokens
        payload["messages"] = wire
        if opts.temperature is not None:
            payload["temperature"] = opts.temperature
        if opts.seed is not None and self.capabilities.seed:
            payload["seed"] = opts.seed
        return payload

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> ProviderResult:
        payload = self.build_payload(messages, output_model, options)
        url = f"{require_base_url(self.name, self.config, carries_key=True)}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key(self.name, self.config)}"}
        start = time.perf_counter()
        data = await self.transport.post_json(url, payload, headers)
        refusal = as_text(field(self.name, data, "choices", 0, "message", "refusal"))
        text = as_text(field(self.name, data, "choices", 0, "message", "content"))
        finish = as_text(field(self.name, data, "choices", 0, "finish_reason")) or None
        if refusal:
            text, finish = refusal, "refusal"
        return ProviderResult(
            raw_text=text,
            parsed=None if refusal else parse_json_object(text),
            usage=TokenUsage(
                input_tokens=as_int(field(self.name, data, "usage", "prompt_tokens")),
                output_tokens=as_int(field(self.name, data, "usage", "completion_tokens")),
            ),
            latency_ms=elapsed_ms(start),
            model=as_text(data.get("model")) or payload["model"],
            finish_reason=finish,
            provider=self.name,
        )
