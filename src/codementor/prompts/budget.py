"""Token bütçesi: sağlayıcıdan bağımsız yaklaşık sayım ve öncelikli kırpma (mimari §5.4.5)."""

from __future__ import annotations

import json
import math
from collections.abc import Callable, Mapping

from pydantic import BaseModel

from codementor.config import ProviderConfig, Settings
from codementor.models.provider import ChatMessage
from codementor.providers.factory import (
    PROVIDER_NAMES,
    chain_names,
    unknown_provider_reason,
)

# Kod tokenlaştırıcıları İngilizce metinde ~4, kod ve Türkçede ~3 karakter/token verir;
# temkinli olmak için 3 (fazla tahmin, taşmadan iyidir).
CHARS_PER_TOKEN = 3
MESSAGE_OVERHEAD_TOKENS = 4
MIN_PROMPT_TOKENS = 1024  # bundan azı yapılandırma hatasıdır (kodu suçlamayalım)

# Bütçe aşılırsa bu sırayla kırpılır. Kod, şema ve çekirdek kurallar hiçbir zaman kırpılmaz.
TRIM_ORDER = ("fewshots", "checklist", "facts", "static_findings")
TEST_PROVIDERS = frozenset({"fake"})  # testlerin FakeProvider'ı: varsayılan bağlam
CHAIN_SEPARATOR = "→"  # FallbackProvider.name biçimi

Render = Callable[[Mapping[str, int]], list[ChatMessage]]


class PromptBudgetError(ValueError):
    """Prompt, kırpılabilecek her şey kırpıldığı halde bağlam bütçesine sığmıyor."""

    def __init__(self, estimated: int, budget: int, code_tokens: int | None = None) -> None:
        self.estimated = estimated
        self.budget = budget
        self.code_tokens = code_tokens
        if code_tokens is None or code_tokens + MESSAGE_OVERHEAD_TOKENS > budget:
            reason = "Kod token bütçesine sığmıyor"
            advice = "daha kısa bir kod gönderin"
        else:
            reason = (
                f"Kod (yaklaşık {code_tokens} token) ile kırpılamayan bölümler (kurallar, "
                "soru, ipucu) birlikte bütçeye sığmıyor"
            )
            advice = "kodu kısaltın"
        super().__init__(
            f"{reason} (yaklaşık {estimated} token, bütçe {budget}). Kod kırpılmaz; "
            f"{advice} ya da bağlamı daha geniş bir sağlayıcı seçin."
        )


class PromptConfigError(ValueError):
    """Sağlayıcı bağlamı yapılandırması prompt'a yer bırakmıyor ya da ad bilinmiyor."""


def estimate_tokens(text: str) -> int:
    """Yaklaşık token sayısı (yukarı yuvarlanır)."""
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def estimate_messages(messages: list[ChatMessage]) -> int:
    """Mesaj listesinin yaklaşık token sayısı (mesaj başına küçük ek yük dahil)."""
    return sum(estimate_tokens(m.content) + MESSAGE_OVERHEAD_TOKENS for m in messages)


def schema_tokens(output_model: type[BaseModel]) -> int:
    """Çıktı şemasının yaklaşık token sayısı."""
    return estimate_tokens(json.dumps(output_model.model_json_schema(), ensure_ascii=False))


def provider_chain(settings: Settings, provider: str | None) -> list[str]:
    """Bütçesi hesaba katılacak sağlayıcılar: verilen ad (ya da `a→b` zinciri) veya
    yapılandırmadaki varsayılan + fallback. Prompt zincirdeki her sağlayıcıya gidebilir."""
    if provider and CHAIN_SEPARATOR in provider:
        return [p.strip() for p in provider.split(CHAIN_SEPARATOR) if p.strip()]
    return chain_names(settings.providers, provider)


def _single_budget(settings: Settings, name: str, schema: int) -> int:
    context = settings.prompts.default_context_tokens
    reserve = settings.prompts.reserve_output_tokens
    if name not in TEST_PROVIDERS:
        if name not in PROVIDER_NAMES:
            raise PromptConfigError(f"Sağlayıcı {name!r}: {unknown_provider_reason(name)}")
        config = getattr(settings.providers, name, None)
        if not isinstance(config, ProviderConfig):  # PROVIDER_NAMES ile ProvidersSettings ayrışırsa
            raise PromptConfigError(f"Sağlayıcı yapılandırması bulunamadı: {name}")
        context = config.context_tokens or config.num_ctx or context
        reserve = config.max_tokens or reserve
    budget = context - reserve - schema
    if budget < MIN_PROMPT_TOKENS:
        raise PromptConfigError(
            f"Yapılandırma hatası: {name} için bağlam ({context} token), çıktı payı "
            f"({reserve}) ve şemadan ({schema}) sonra prompt'a {max(budget, 0)} token kalıyor; "
            "context_tokens/num_ctx artırılmalı ya da max_tokens azaltılmalı."
        )
    return budget


def context_budget(settings: Settings, provider: str | None, output_model: type[BaseModel]) -> int:
    """Prompt'a kalan token: zincirdeki en küçük (bağlam - çıktı payı - şema).

    Şema API'de gitse de sayılır. Fallback'teki küçük bağlamlı bir sağlayıcı prompt'u sessizce
    kesmesin diye en dar sağlayıcı belirleyicidir.
    """
    schema = schema_tokens(output_model)
    return min(
        _single_budget(settings, name, schema) for name in provider_chain(settings, provider)
    )


def fit_to_budget(
    render: Render,
    max_levels: Mapping[str, int],
    budget: int,
    *,
    code_tokens: int | None = None,
) -> tuple[list[ChatMessage], list[str]]:
    """Bütçeye sığana dek bölümleri `TRIM_ORDER` sırasıyla birer kademe kısaltır.

    `max_levels[bölüm]`: o bölümün kaç kademe kısaltılabileceği (0 = kırpılamaz).
    `render(kademeler)` her denemede mesajları yeniden üretir. Dönüş: (mesajlar,
    kısaltılan bölümler sırayla). Her şey kırpıldığı halde sığmıyorsa `PromptBudgetError`;
    `code_tokens` verilirse hata kodun kendisinin mi yoksa geri kalanın mı taştığını söyler.
    """
    levels = dict.fromkeys(max_levels, 0)
    trimmed: list[str] = []
    while True:
        messages = render(levels)
        estimated = estimate_messages(messages)
        if estimated <= budget:
            return messages, trimmed
        section = next((s for s in TRIM_ORDER if levels.get(s, 0) < max_levels.get(s, 0)), None)
        if section is None:
            raise PromptBudgetError(estimated, budget, code_tokens)
        levels[section] += 1
        if section not in trimmed:
            trimmed.append(section)
