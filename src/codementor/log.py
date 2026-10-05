"""Yapılandırılmış log (mimari §13) ve gizli bilgi maskeleme (mimari §5.5.3, §12).

`get_logger` global structlog yapılandırmasından **bağımsız** bir logger döndürür: işlemci
zinciri her çağrıda buradan kurulur ve `redact_secrets` render'dan hemen önce her zaman
çalışır. Başka bir kod `structlog.configure(...)` ya da `reset_defaults()` çağırsa da
maskeleme devre dışı kalmaz. Maskelenenler:
- adı gizli görünen alanlar (`authorization`, `x-api-key`, `api_key`, `access_token`,
  `secret`, `password` ...) her derinlikte; `input_tokens` / `max_tokens` gibi sayaçlar değil;
- `register_secret` ile kaydedilen gerçek anahtar değerleri ve `Bearer …` / `sk-…` desenleri
  tüm metinlerde (istisna izleri ve sözlük anahtarları dahil).
"""

from __future__ import annotations

import logging
import re
import sys
import threading
from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass
from typing import Any, TextIO

import structlog
from structlog.typing import FilteringBoundLogger, Processor

MASK = "***"
# Alan adı gizli mi: son parça tam eşleşmeli (`x-api-key`, `access_token` evet;
# `input_tokens`, `max_tokens`, `token_count` hayır).
_SECRET_KEY = re.compile(
    r"(?:^|[-_.])(?:authorization|api[-_]?key|secret|password|passwd"
    r"|(?:access|auth|refresh|bearer|id|session)?[-_]?token)$",
    re.IGNORECASE,
)
_SECRET_PATTERNS = re.compile(
    r"(?i:bearer)\s+[A-Za-z0-9._~+/=-]{8,}|\bsk-[A-Za-z0-9_-]{8,}|\bya29\.[A-Za-z0-9._-]{8,}"
)
_MIN_SECRET_LEN = 8
_secrets: set[str] = set()
_lock = threading.Lock()


@dataclass
class _Settings:
    stream: TextIO | None = None  # None: çağrı anındaki sys.stderr
    json: bool = True
    level: int = logging.WARNING


_settings = _Settings()


def register_secret(value: str | None) -> None:
    """Gerçek bir gizli değeri (API anahtarı) maskelenecekler listesine ekler."""
    if value and len(value) >= _MIN_SECRET_LEN:
        with _lock:
            _secrets.add(value)


def scrub(value: Any) -> Any:
    """Değerin gizli bilgilerden arındırılmış kopyası (sözlük/liste özyinelemeli)."""
    if isinstance(value, str):
        return _scrub_text(value)
    if value is None or isinstance(value, bool | int | float):
        return value
    if isinstance(value, Mapping):
        return {_scrub_key(k): MASK if _is_secret_key(k) else scrub(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return tuple(scrub(v) for v in value)
    if isinstance(value, list | set | frozenset):
        return [scrub(v) for v in value]
    # bilinmeyen nesne: renderer onu str() ile yazacağı için önce metne çevirip maskele
    return _scrub_text(str(value))


def _is_secret_key(key: object) -> bool:
    return isinstance(key, str) and bool(_SECRET_KEY.search(key))


def _scrub_key(key: object) -> object:
    return _scrub_text(key) if isinstance(key, str) else key


def _scrub_text(text: str) -> str:
    with _lock:
        known = sorted(_secrets, key=len, reverse=True)
    for secret in known:
        if secret in text:
            text = text.replace(secret, MASK)
    return _SECRET_PATTERNS.sub(MASK, text)


def redact_secrets(
    _logger: object, _method: str, event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    """structlog işlemcisi: olay sözlüğünü maskeler."""
    return {
        str(_scrub_key(k)): MASK if _is_secret_key(k) else scrub(v) for k, v in event_dict.items()
    }


def _processors(json: bool) -> list[Processor]:
    renderer: Processor = (
        structlog.processors.JSONRenderer(ensure_ascii=False)
        if json
        else structlog.dev.ConsoleRenderer(colors=False)
    )
    return [
        structlog.contextvars.merge_contextvars,  # analysis_id / stage bağlamı (§13, Faz 50)
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.format_exc_info,
        redact_secrets,  # her zaman render'dan hemen önce
        renderer,
    ]


def configure_logging(
    stream: TextIO | None = None, *, json: bool = True, level: int = logging.WARNING
) -> None:
    """Çıktı hedefi, biçim ve düzey. Varsayılan WARNING: CLI çıktısı sade kalır; sunucu
    (Faz 11) INFO ile kurar. Global structlog da aynı zincirle kurulur (üçüncü taraf
    `structlog.get_logger` kullanımları için); `get_logger` ona bağlı değildir."""
    _settings.stream, _settings.json, _settings.level = stream, json, level
    structlog.configure(
        processors=_processors(json),
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.PrintLoggerFactory(stream if stream is not None else sys.stderr),
        cache_logger_on_first_use=False,
    )


@dataclass(frozen=True)
class LoggingSnapshot:
    """`configure_logging` ayarlarının anlık görüntüsü (testler önceki hâle döner, Faz 31)."""

    stream: TextIO | None
    json: bool
    level: int


def logging_snapshot() -> LoggingSnapshot:
    """Geçerli log yapılandırması."""
    return LoggingSnapshot(_settings.stream, _settings.json, _settings.level)


def restore_logging(snapshot: LoggingSnapshot) -> None:
    """Anlık görüntüdeki yapılandırmayı geri yükler."""
    configure_logging(snapshot.stream, json=snapshot.json, level=snapshot.level)


class RedactingLogger:
    """Her çağrıda güncel ayarlarla ve maskeleme zinciriyle kurulan logger."""

    def __init__(self, name: str) -> None:
        self.name = name

    def _bound(self) -> FilteringBoundLogger:
        stream = _settings.stream if _settings.stream is not None else sys.stderr
        logger: FilteringBoundLogger = structlog.wrap_logger(
            structlog.PrintLogger(stream),
            processors=_processors(_settings.json),
            wrapper_class=structlog.make_filtering_bound_logger(_settings.level),
            cache_logger_on_first_use=False,
        )
        return logger.bind(logger=self.name)

    def debug(self, event: str, **fields: Any) -> None:
        self._bound().debug(event, **fields)

    def info(self, event: str, **fields: Any) -> None:
        self._bound().info(event, **fields)

    def warning(self, event: str, **fields: Any) -> None:
        self._bound().warning(event, **fields)

    def error(self, event: str, **fields: Any) -> None:
        self._bound().error(event, **fields)

    def exception(self, event: str, **fields: Any) -> None:
        """`error` + etkin istisnanın izi (`except` içinde çağrılır); iz metni de maskelenir
        (`format_exc_info` maskelemeden önce çalışır)."""
        self._bound().exception(event, **fields)


def get_logger(name: str) -> RedactingLogger:
    """Maskeleme işlemcisi her zaman kurulu logger."""
    return RedactingLogger(name)
