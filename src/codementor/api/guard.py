"""API güven sınırı (Faz 47, mimari §9/§12, ADR-0023).

İstemci sunucu yapılandırmasını aşamaz:
- **Host doğrulaması (DNS rebinding):** tarayıcıdaki kötü bir sayfa alan adını 127.0.0.1'e
  çözdürüp yerel API'ye istek atabilir; Host başlığı yalnız loopback adları ya da
  `api.allowed_hosts` olabilir. Hata `400` problem+json (Starlette'in düz metin yanıtı değil).
- **Gövde sınırı:** `Content-Length` `api.max_body_bytes`'ı aşarsa okunmadan, başlıksız (chunked)
  gövde sınırı geçince okuma kesilerek `413`.
- **Eşzamanlı analiz sınırı:** `AnalysisSlots`; dolunca rota `503` döner.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from codementor.api.errors import ApiProblemError, problem_response
from codementor.config import Settings
from codementor.models.api import Problem

LOOPBACK_HOSTS = ("127.0.0.1", "localhost", "[::1]")
ANY_HOST = "*"
_BODY_METHODS = frozenset({"POST", "PUT", "PATCH"})


_WINDOW_S = 60.0


class RateLimiter:
    """İstemci IP başına kayan pencere (dakika) hız sınırlayıcı (Faz E, mimari §17).

    Saat monotoniktir (sistem saati geri alınınca pencere bozulmaz). Penceresi boşalan IP'lerin
    kayıtları dakikada bir süpürülür: geçip giden istemciler sözlüğü sınırsız büyütmez.
    """

    def __init__(
        self, limit_per_minute: int | None, clock: Callable[[], float] = time.monotonic
    ) -> None:
        self.limit = limit_per_minute
        self._clock = clock
        self._lock = threading.Lock()
        self._records: dict[str, deque[float]] = {}
        self._next_sweep = clock() + _WINDOW_S

    def check(self, client_host: str) -> None:
        if self.limit is None:
            return
        now = self._clock()
        cutoff = now - _WINDOW_S
        with self._lock:
            if now >= self._next_sweep:
                self._sweep(cutoff)
                self._next_sweep = now + _WINDOW_S
            timestamps = self._records.setdefault(client_host, deque())
            while timestamps and timestamps[0] <= cutoff:
                timestamps.popleft()
            if len(timestamps) >= self.limit:
                raise ApiProblemError(
                    429,
                    "Çok fazla istek; bir dakika sonra yeniden deneyin.",
                    headers={"Retry-After": "60"},
                )
            timestamps.append(now)

    def _sweep(self, cutoff: float) -> None:
        """Son isteği pencerenin dışında kalan IP'leri siler (kilit altında çağrılır)."""
        stale = [
            host for host, stamps in self._records.items() if not stamps or stamps[-1] <= cutoff
        ]
        for host in stale:
            del self._records[host]

    def tracked_clients(self) -> int:
        """İzlenen IP sayısı (testler ve tanılama)."""
        with self._lock:
            return len(self._records)


def host_of(header: str) -> str | None:
    """Host başlığından port'suz, küçük harfli ad; IPv6 köşeli ayraçlı kalır."""
    value = header.strip().lower()
    if value.startswith("["):
        end = value.find("]")
        return value[: end + 1] if end > 0 else None
    host = value.split(":", 1)[0]
    return host or None


def allowed_hosts(settings: Settings) -> frozenset[str]:
    """Loopback adları her zaman, üstüne yapılandırılanlar."""
    return frozenset([*LOOPBACK_HOSTS, *(h.strip().lower() for h in settings.api.allowed_hosts)])


@dataclass
class AnalysisSlots:
    """Eşzamanlı analiz sayacı. Tek olay döngüsünde çalışır; denetle-artır arasında `await` yok."""

    limit: int
    active: int = 0

    def try_acquire(self) -> bool:
        if self.active >= self.limit:
            return False
        self.active += 1
        return True

    def release(self) -> None:
        self.active = max(0, self.active - 1)


class GuardMiddleware:
    """Host ve gövde boyutu denetimi; en dışta çalışır (CORS ve API anahtarından önce)."""

    def __init__(self, app: ASGIApp, *, hosts: frozenset[str], max_body_bytes: int) -> None:
        self.app = app
        self.hosts = hosts
        self.max_body_bytes = max_body_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = Headers(scope=scope)
        path = scope.get("path", "")
        if ANY_HOST not in self.hosts and host_of(headers.get("host", "")) not in self.hosts:
            detail = "Host başlığına izin verilmiyor (api.allowed_hosts)."
            await _problem(400, "Hatalı istek", detail, path)(scope, receive, send)
            return
        if scope["method"] not in _BODY_METHODS:
            await self.app(scope, receive, send)
            return
        declared = headers.get("content-length", "")
        if declared.isdigit() and int(declared) > self.max_body_bytes:
            await self._too_large(scope, receive, send, path)
            return
        body = await self._read_body(receive)
        if body is None:
            await self._too_large(scope, receive, send, path)
            return
        await self.app(scope, _replay(body, receive), send)

    async def _read_body(self, receive: Receive) -> bytes | None:
        """Gövdeyi sınıra kadar okur; aşılırsa None. Sınır küçük olduğu için bellekte tutulur."""
        chunks: list[bytes] = []
        size = 0
        while True:
            message = await receive()
            if message["type"] != "http.request":  # istemci koptu
                return b"".join(chunks)
            chunk: bytes = message.get("body", b"")
            size += len(chunk)
            if size > self.max_body_bytes:
                return None
            chunks.append(chunk)
            if not message.get("more_body", False):
                return b"".join(chunks)

    async def _too_large(self, scope: Scope, receive: Receive, send: Send, path: str) -> None:
        detail = f"İstek gövdesi {self.max_body_bytes} baytı aşıyor (api.max_body_bytes)."
        await _problem(413, "İstek çok büyük", detail, path)(scope, receive, send)


def _problem(status: int, title: str, detail: str, path: str) -> ASGIApp:
    return problem_response(Problem(title=title, status=status, detail=detail, instance=path))


def _replay(body: bytes, receive: Receive) -> Receive:
    """Okunan gövdeyi bir kez verir; sonrası özgün kanal (SSE kopma algısı korunur)."""
    sent = False

    async def replay() -> Message:
        nonlocal sent
        if not sent:
            sent = True
            return {"type": "http.request", "body": body, "more_body": False}
        return await receive()

    return replay
