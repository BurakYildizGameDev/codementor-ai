"""Adaptörlerin ortak yardımcıları: anahtar/model çözümü, seçenek birleştirme, güvenli okuma."""

from __future__ import annotations

import os
import time
from typing import Any
from urllib.parse import urlsplit

from codementor.config import ProviderConfig
from codementor.log import register_secret
from codementor.models.provider import GenerationOptions
from codementor.providers.base import ProviderConfigError, ProviderResponseError


def require_model(provider: str, config: ProviderConfig) -> str:
    """Model adı yalnızca yapılandırmadan gelir (AGENTS.md kural 5)."""
    if not config.model.strip():
        raise ProviderConfigError(
            provider, f"model tanımlı değil ([providers.{provider}] model = ...)"
        )
    return config.model.strip()


_LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


def require_base_url(provider: str, config: ProviderConfig, *, carries_key: bool = False) -> str:
    """Sağlayıcı adresi; anahtar taşıyan istek yerel olmayan adrese yalnızca https ile gider."""
    if not config.base_url:
        raise ProviderConfigError(
            provider, f"adres tanımlı değil ([providers.{provider}] base_url)"
        )
    url = config.base_url.rstrip("/")
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ProviderConfigError(provider, "base_url geçerli bir http(s) adresi değil")
    if carries_key and parts.scheme != "https" and parts.hostname not in _LOCAL_HOSTS:
        raise ProviderConfigError(
            provider, "API anahtarı şifrelenmemiş bağlantıyla gönderilmez; base_url https olmalı"
        )
    return url


def api_key(provider: str, config: ProviderConfig) -> str:
    """Anahtar yalnızca ortam değişkeninden okunur ve log maskeleyicisine kaydedilir."""
    if not config.api_key_env:
        raise ProviderConfigError(provider, "api_key_env tanımlı değil")
    value = os.environ.get(config.api_key_env, "").strip()
    if not value:
        raise ProviderConfigError(provider, f"{config.api_key_env} ortam değişkeni tanımlı değil")
    register_secret(value)
    return value


def merged(options: GenerationOptions, config: ProviderConfig) -> GenerationOptions:
    """Çağrı seçenekleri önce, yoksa sağlayıcı yapılandırması."""
    return GenerationOptions(
        temperature=options.temperature if options.temperature is not None else config.temperature,
        seed=options.seed if options.seed is not None else config.seed,
        max_tokens=options.max_tokens if options.max_tokens is not None else config.max_tokens,
    )


def elapsed_ms(start: float) -> int:
    return max(0, int((time.perf_counter() - start) * 1000))


def field(provider: str, data: Any, *path: str | int) -> Any:
    """İç içe alanı okur; yol yoksa None, tip uyuşmazlığında `ProviderResponseError`."""
    current = data
    for step in path:
        if isinstance(step, int):
            if not isinstance(current, list):
                raise ProviderResponseError(provider, "beklenmeyen yanıt biçimi")
            if step >= len(current):
                return None
            current = current[step]
        else:
            if not isinstance(current, dict):
                raise ProviderResponseError(provider, "beklenmeyen yanıt biçimi")
            current = current.get(step)
            if current is None:
                return None
    return current


def as_int(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else 0


def as_text(value: Any) -> str:
    return value if isinstance(value, str) else ""
