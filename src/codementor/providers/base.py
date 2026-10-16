"""Sağlayıcı arayüzü, hata sınıfları ve yeniden deneme politikası (mimari §5.5.1, §5.5.3).

Yeniden deneme yalnızca geçici hatalarda yapılır: ağ/zaman aşımı, 429 ve 5xx (Anthropic'in
529 "overloaded" dahil). Diğer 4xx hataları (geçersiz istek, kimlik) hemen fırlatılır.
"""

from __future__ import annotations

import asyncio
import math
import random
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Protocol, TypeVar

from pydantic import BaseModel

from codementor.models.provider import (
    ChatMessage,
    GenerationOptions,
    ProviderCapabilities,
    ProviderResult,
)

T = TypeVar("T")
Sleep = Callable[[float], Awaitable[None]]


class LLMProvider(Protocol):
    """Tüm sağlayıcıların ortak arayüzü."""

    name: str
    capabilities: ProviderCapabilities

    @property
    def primary_name(self) -> str:
        """Zincirin başında gerçekten çağrılan sağlayıcının adı (Faz G6).

        Tek sağlayıcıda `name`'dir; geri dönüş zincirinde ilk halka. Önbellek yalnızca birincil
        sağlayıcı yanıt verdiğinde geçerlidir (`orchestrator`), bu yüzden çağıran `chain` gibi
        sağlayıcıya özel alanları yoklamaz.
        """
        ...

    async def generate_structured(
        self,
        messages: list[ChatMessage],
        output_model: type[BaseModel],
        options: GenerationOptions,
    ) -> ProviderResult: ...


class NamedProvider:
    """Zincirsiz sağlayıcılar `NamedProvider`'dan türer: `primary_name` = `name` (Faz G6)."""

    name: str

    @property
    def primary_name(self) -> str:
        """Tek sağlayıcıda birincil ad kendi adıdır."""
        return self.name


class ProviderError(Exception):
    """Sağlayıcı çağrısı başarısız; mesaj kullanıcıya dönük (Türkçe) ve gizli bilgi içermez."""

    retryable = False

    def __init__(self, provider: str, message: str, *, status: int | None = None) -> None:
        super().__init__(f"{provider}: {message}")
        self.provider = provider
        self.status = status


class ProviderConfigError(ProviderError):
    """Model adı, API anahtarı ya da adres yapılandırılmamış."""


class ProviderRequestError(ProviderError):
    """Yeniden denenmeyen 4xx (geçersiz istek, kimlik doğrulama, yetki)."""


class ProviderResponseError(ProviderError):
    """Sağlayıcı yanıtı işlenemiyor (JSON olmayan gövde, boyut sınırı aşımı); yeniden denenmez."""


class ProviderUnavailableError(ProviderError):
    """Ağ hatası veya zaman aşımı."""

    retryable = True


class ProviderRateLimitError(ProviderError):
    """429: hız sınırı."""

    retryable = True

    def __init__(
        self, provider: str, message: str, *, status: int | None = 429, retry_after: float | None
    ) -> None:
        super().__init__(provider, message, status=status)
        self.retry_after = retry_after


class ProviderServerError(ProviderError):
    """5xx ya da 529: sağlayıcı tarafında geçici sorun."""

    retryable = True


@dataclass(frozen=True)
class RetryPolicy:
    """Üstel geri çekilme + jitter; `Retry-After` verilmişse (üst sınırla) ona uyulur."""

    max_retries: int = 2
    base_delay_s: float = 0.5
    max_delay_s: float = 20.0
    sleep: Sleep = field(default=asyncio.sleep, compare=False)

    def delay(self, attempt: int, error: ProviderError) -> float:
        """`attempt` 0 tabanlı yeniden deneme sırası için bekleme süresi."""
        wait = error.retry_after if isinstance(error, ProviderRateLimitError) else None
        if wait is not None and math.isfinite(wait):
            return min(max(wait, 0.0), self.max_delay_s)
        backoff = self.base_delay_s * (2**attempt)
        jitter: float = random.uniform(0, self.base_delay_s)
        return float(min(backoff + jitter, self.max_delay_s))

    def _too_long(self, error: ProviderError) -> bool:
        """Sağlayıcı `max_delay_s`'ten uzun beklenmesini istiyorsa (ör. kota) beklemeden bırak;
        fallback zinciri sıradaki sağlayıcıya geçer."""
        wait = error.retry_after if isinstance(error, ProviderRateLimitError) else None
        return wait is not None and math.isfinite(wait) and wait > self.max_delay_s

    async def run(self, call: Callable[[], Awaitable[T]]) -> T:
        """`call`'ı çalıştırır; yalnızca `retryable` hatada en fazla `max_retries` kez yineler."""
        attempt = 0
        while True:
            try:
                return await call()
            except ProviderError as exc:
                if not exc.retryable or attempt >= self.max_retries or self._too_long(exc):
                    raise
                await self.sleep(self.delay(attempt, exc))
                attempt += 1
