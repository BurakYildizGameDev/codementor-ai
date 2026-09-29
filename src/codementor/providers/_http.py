"""Sağlayıcıların ortak HTTP katmanı: zaman aşımı, durum → hata eşleme, yeniden deneme,
yanıt boyutu sınırı. Başlıklar (API anahtarı) hiçbir zaman loglanmaz."""

from __future__ import annotations

import asyncio
import json
import math
import time
from dataclasses import dataclass, field
from typing import Any

import httpx

from codementor.log import get_logger, scrub
from codementor.providers.base import (
    ProviderError,
    ProviderRateLimitError,
    ProviderRequestError,
    ProviderResponseError,
    ProviderServerError,
    ProviderUnavailableError,
    RetryPolicy,
)

MAX_RESPONSE_BYTES = 4 * 1024 * 1024  # LLM yanıtı bunun çok altında; bellek şişirmeye karşı
_MAX_ERROR_TEXT = 200
_ERROR_SCAN_BYTES = 8192
log = get_logger("codementor.providers")


@dataclass
class HttpTransport:
    """Bir sağlayıcının HTTP ayarları; `client` verilmezse her çağrıda geçici istemci açılır."""

    provider: str
    timeout_s: float
    retry: RetryPolicy = field(default_factory=RetryPolicy)
    client: httpx.AsyncClient | None = None

    async def post_json(
        self, url: str, payload: dict[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]:
        """JSON gönderir, JSON nesnesi döndürür; geçici hatalarda yeniden dener."""
        return await self.retry.run(lambda: self._once("POST", url, headers, payload))

    async def get_json(self, url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
        """GET; yeniden deneme yok (sağlık kontrolü)."""
        return await self._once("GET", url, headers or {}, None)

    async def _once(
        self, method: str, url: str, headers: dict[str, str], payload: dict[str, Any] | None
    ) -> dict[str, Any]:
        # httpx zaman aşımı her fazda (bağlan/oku/yaz) ayrı uygulanır; damla damla yanıt veren
        # sunucuya karşı toplam süre de sınırlanır. İstisnalar `from None` ile zincirlenmez:
        # httpx istek nesnesi başlıkları (API anahtarı) taşır (mimari §12).
        start = time.perf_counter()
        try:
            async with asyncio.timeout(self.timeout_s):
                if self.client is not None:
                    status, body, response_headers = await self._send(
                        self.client, method, url, headers, payload
                    )
                else:
                    async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                        status, body, response_headers = await self._send(
                            client, method, url, headers, payload
                        )
        except (TimeoutError, httpx.TimeoutException):
            self._log("zaman aşımı", start)
            raise ProviderUnavailableError(self.provider, "zaman aşımı") from None
        except httpx.DecodingError:
            self._log("çözülemeyen yanıt", start)
            raise ProviderResponseError(self.provider, "yanıt gövdesi çözülemedi") from None
        except httpx.HTTPError as exc:
            self._log("bağlantı hatası", start)
            raise ProviderUnavailableError(
                self.provider, f"bağlantı kurulamadı ({type(exc).__name__})"
            ) from None
        self._log("yanıt", start, status=status)
        if status >= 400:
            raise _status_error(self.provider, status, body, response_headers)
        try:
            data = json.loads(body)
        except (ValueError, UnicodeDecodeError, RecursionError):
            raise ProviderResponseError(self.provider, "yanıt gövdesi JSON değil") from None
        if not isinstance(data, dict):
            raise ProviderResponseError(self.provider, "yanıt gövdesi JSON nesnesi değil")
        return data

    async def _send(
        self,
        client: httpx.AsyncClient,
        method: str,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any] | None,
    ) -> tuple[int, bytes, httpx.Headers]:
        # sıkıştırma istenmez: tek bir sıkıştırılmış parça bellekte sınırsız açılmasın
        wire_headers = {**headers, "accept-encoding": "identity"}
        async with client.stream(
            method, url, headers=wire_headers, json=payload, timeout=self.timeout_s
        ) as response:
            chunks: list[bytes] = []
            size = 0
            async for chunk in response.aiter_bytes():
                size += len(chunk)
                if size > MAX_RESPONSE_BYTES:
                    raise ProviderResponseError(self.provider, "yanıt boyutu sınırı aşıldı")
                chunks.append(chunk)
            return response.status_code, b"".join(chunks), response.headers

    def _log(self, event: str, start: float, **fields: Any) -> None:
        elapsed = int((time.perf_counter() - start) * 1000)
        log.debug(event, provider=self.provider, latency_ms=elapsed, **fields)


def _error_text(body: bytes) -> str:
    """Hata gövdesinden kısa, maskelenmiş açıklama (`error.message` ya da ham metin)."""
    try:
        data = json.loads(body)
    except (ValueError, UnicodeDecodeError, RecursionError):
        text = body[:_ERROR_SCAN_BYTES].decode("utf-8", errors="replace")
    else:
        error = data.get("error") if isinstance(data, dict) else None
        message = error.get("message") if isinstance(error, dict) else error
        text = str(message if message is not None else data)[:_ERROR_SCAN_BYTES]
    # önce maskele, sonra kırp: kırpılmış bir anahtar öneki maskeleyiciden kaçmasın
    return " ".join(str(scrub(text)).split())[:_MAX_ERROR_TEXT]


def _retry_after(headers: httpx.Headers) -> float | None:
    value = headers.get("retry-after")
    try:
        seconds = float(value) if value is not None else None
    except ValueError:
        return None  # HTTP tarihi biçimi: üstel geri çekilmeye bırak
    if seconds is None or not math.isfinite(seconds) or seconds < 0:
        return None  # `nan`/`inf`/negatif: sonsuz ya da anlamsız bekleme olmasın
    return seconds


def _status_error(provider: str, status: int, body: bytes, headers: httpx.Headers) -> ProviderError:
    detail = _error_text(body)
    if status == 429:
        return ProviderRateLimitError(
            provider, f"hız sınırı (429): {detail}", retry_after=_retry_after(headers)
        )
    if status >= 500:
        return ProviderServerError(provider, f"sunucu hatası ({status}): {detail}", status=status)
    if status in (401, 403):
        return ProviderRequestError(
            provider, f"kimlik doğrulama/yetki hatası ({status})", status=status
        )
    return ProviderRequestError(provider, f"istek reddedildi ({status}): {detail}", status=status)


def parse_json_object(text: str) -> dict[str, Any] | None:
    """Model metnini JSON nesnesine çözer; ```json çitlerini kabul eder; olmazsa None."""
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = candidate.strip("`")
        candidate = candidate.removeprefix("json").strip()
    try:
        data = json.loads(candidate)
    except (ValueError, RecursionError):  # çok derin iç içe JSON da "çözülemedi" sayılır
        return None
    return data if isinstance(data, dict) else None
