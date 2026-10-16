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
from codementor.providers.cli_agent import CliAgentProvider
from codementor.providers.codex_cli import CodexCliProvider
from codementor.providers.ollama import OllamaProvider
from codementor.providers.openai_compat import OpenAICompatProvider

PROVIDER_NAMES = (
    "ollama",
    "gemini",
    "anthropic",
    "claude_cli",
    "agy",
    "codex",
)
# ADR-0021: canlı doğrulanamadığı için kaldırıldı; eski yapılandırmada kalan ad anlaşılır hata verir
REMOVED_PROVIDERS = ("openai", "deepseek")
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
    if name == "gemini":  # ADR-0020: OpenAI uyumlu uç, katı şema
        gemini = providers.gemini
        return OpenAICompatProvider(
            name,
            gemini,
            token_field="max_tokens",
            seed=False,
            transport=transport(name, gemini.timeout_s),
        )
    if name == "anthropic":
        anthropic = providers.anthropic
        return AnthropicProvider(anthropic, transport=transport(name, anthropic.timeout_s))
    if name == "claude_cli":
        return CliAgentProvider("claude_cli", providers.claude_cli, retry=policy)
    if name == "agy":
        return CliAgentProvider("agy", providers.agy, retry=policy)
    if name == "codex":
        return CodexCliProvider(providers.codex, retry=policy)
    raise ProviderConfigError(name, unknown_provider_reason(name))


def unknown_provider_reason(name: str) -> str:
    """Bilinmeyen ya da kaldırılmış sağlayıcı adı için Türkçe açıklama (ADR-0021)."""
    options = ", ".join(PROVIDER_NAMES)
    if name in REMOVED_PROVIDERS:
        return f"bu sağlayıcı kaldırıldı (ADR-0021); seçenekler: {options}"
    return f"bilinmeyen sağlayıcı (seçenekler: {options})"


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

    @property
    def primary_name(self) -> str:
        """Zincirin ilk halkası: önbellek kararı buna göre verilir (Faz G6)."""
        return self.chain[0].primary_name

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
