"""Yapılandırmadan sağlayıcı kurma ve geri dönüş zinciri (mimari §5.5.3).

Zincir, bir sağlayıcı `ProviderError` fırlatırsa (ağ, 429/5xx yeniden denemeler tükendikten
sonra, 4xx, eksik anahtar/model) sıradakine geçer ve her geçişi `ProviderResult.warnings`'e
Türkçe olarak yazar; bu uyarılar rapora `meta.warnings` olarak gider. Yanıtın bozuk JSON
olması geçiş sebebi değildir: onarım K5'in (Faz 9) işidir.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import httpx
from pydantic import BaseModel

from codementor.config import ProvidersSettings, Settings, get_settings
from codementor.models.provider import (
    ChatMessage,
    GenerationOptions,
    ProviderCapabilities,
    ProviderResult,
)
from codementor.providers._http import HttpTransport
from codementor.providers.anthropic import AnthropicProvider
from codementor.providers.base import LLMProvider, ProviderConfigError, ProviderError, RetryPolicy
from codementor.providers.ollama import OllamaProvider
from codementor.providers.openai_compat import OpenAICompatProvider

PROVIDER_NAMES = ("ollama", "openai", "deepseek", "anthropic")
FALLBACK_WARNING = "{failed} sağlayıcısı kullanılamadı ({reason}); {next} ile devam edildi."


class AllProvidersFailedError(ProviderError):
    """Zincirdeki tüm sağlayıcılar başarısız."""


def build_provider(
    name: str,
    settings: ProvidersSettings | None = None,
    *,
    retry: RetryPolicy | None = None,
    client: httpx.AsyncClient | None = None,
) -> LLMProvider:
    """Adı verilen sağlayıcıyı yapılandırmasıyla kurar (ağa çıkmaz)."""
    providers = settings if settings is not None else get_settings().providers
    policy = retry or RetryPolicy(max_retries=providers.max_retries)

    def transport(label: str, timeout_s: int) -> HttpTransport:
        return HttpTransport(label, timeout_s, policy, client)

    if name == "ollama":
        ollama = providers.ollama
        return OllamaProvider(ollama, transport=transport(name, ollama.timeout_s))
    if name == "openai":
        openai = providers.openai
        return OpenAICompatProvider(
            name, openai, mode="strict_schema", transport=transport(name, openai.timeout_s)
        )
    if name == "deepseek":
        deepseek = providers.deepseek
        return OpenAICompatProvider(
            name, deepseek, mode="json_object", transport=transport(name, deepseek.timeout_s)
        )
    if name == "anthropic":
        anthropic = providers.anthropic
        return AnthropicProvider(anthropic, transport=transport(name, anthropic.timeout_s))
    raise ProviderConfigError(
        name, f"bilinmeyen sağlayıcı (seçenekler: {', '.join(PROVIDER_NAMES)})"
    )


def chain_names(providers: ProvidersSettings, primary: str | None = None) -> list[str]:
    """Varsayılan (ya da seçilen) sağlayıcı + fallback listesi, tekrarsız."""
    names: list[str] = []
    for name in [primary or providers.default, *providers.fallback]:
        if name not in names:
            names.append(name)
    return names


def build_chain(
    settings: Settings | None = None,
    *,
    primary: str | None = None,
    retry: RetryPolicy | None = None,
    client: httpx.AsyncClient | None = None,
) -> LLMProvider:
    """Yapılandırmadaki zincir; tek sağlayıcı varsa zincirsiz döner."""
    providers = (settings or get_settings()).providers
    chain = [
        build_provider(n, providers, retry=retry, client=client)
        for n in chain_names(providers, primary)
    ]
    return chain[0] if len(chain) == 1 else FallbackProvider(chain)


@dataclass
class FallbackProvider:
    """Sırayla dener; başarılı yanıta önceki başarısızlıkları uyarı olarak ekler."""

    chain: list[LLMProvider]
    name: str = field(init=False)
    capabilities: ProviderCapabilities = field(init=False)

    def __post_init__(self) -> None:
        if not self.chain:
            raise ProviderConfigError("fallback", "zincir boş")
        self.name = "→".join(p.name for p in self.chain)
        self.capabilities = self.chain[0].capabilities

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> ProviderResult:
        failures: list[tuple[str, ProviderError]] = []
        for provider in self.chain:
            try:
                result = await provider.generate_structured(messages, output_model, options)
            except ProviderError as exc:
                failures.append((provider.name, exc))
                continue
            warnings = [
                FALLBACK_WARNING.format(
                    failed=name,
                    reason=_reason(exc),
                    next=self.chain[i + 1].name,
                )
                for i, (name, exc) in enumerate(failures)
            ]
            return result.model_copy(update={"warnings": [*warnings, *result.warnings]})
        summary = "; ".join(f"{name}: {_reason(exc)}" for name, exc in failures)
        raise AllProvidersFailedError(
            "fallback", f"tüm sağlayıcılar başarısız ({summary})"
        ) from failures[-1][1]


def _reason(exc: ProviderError) -> str:
    """`ollama: zaman aşımı` → `zaman aşımı`."""
    return str(exc).removeprefix(f"{exc.provider}: ")
