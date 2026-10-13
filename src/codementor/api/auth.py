"""İsteğe bağlı API anahtarı (Faz 26, mimari §9/§12).

`api.api_key_env` bir ortam değişkeni adıdır; değişken doluysa `/v1/*` istekleri `X-API-Key`
başlığında aynı anahtarı taşımalıdır. Anahtar koda ya da toml'a yazılmaz (AGENTS kural 5).
Değişken boşsa koruma kapalıdır (varsayılan yerel kullanım). `/health` her zaman açıktır.
"""

from __future__ import annotations

import hmac
import os
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request
from starlette.responses import Response

from codementor.api.errors import problem_response
from codementor.config import Settings
from codementor.log import register_secret
from codementor.models.api import Problem

API_KEY_HEADER = "x-api-key"
PROTECTED_PREFIX = "/v1/"
PROTECTED_EXACT_PATHS = frozenset(
    {"/health/ready", "/docs", "/redoc", "/openapi.json", "/docs/oauth2-redirect"}
)


def _is_protected(path: str) -> bool:
    """Verilen yol API anahtarı korumasına tabi mi? (/health açık kalır)."""
    return path.startswith(PROTECTED_PREFIX) or path in PROTECTED_EXACT_PATHS


def configured_key(settings: Settings) -> str | None:
    """Etkin anahtar; tanımsız ya da boşsa None."""
    name = settings.api.api_key_env
    value = os.environ.get(name, "").strip() if name else ""
    return value or None


def install_api_key(app: FastAPI, settings: Settings) -> None:
    """Anahtar tanımlıysa `/v1/*` ve dahili uçlar için denetleyen ara katmanı ekler."""
    key = configured_key(settings)
    if key is None:
        return
    register_secret(key)  # log'lara maskeli düşer
    expected = key.encode("utf-8")

    @app.middleware("http")
    async def require_key(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.method == "OPTIONS" or not _is_protected(request.url.path):
            return await call_next(request)
        given = request.headers.get(API_KEY_HEADER, "").encode("utf-8")
        if not hmac.compare_digest(given, expected):
            response = problem_response(
                Problem(
                    title="Yetkisiz",
                    status=401,
                    detail="Geçerli bir API anahtarı gerekli (X-API-Key başlığı).",
                    instance=request.url.path,
                )
            )
            response.headers["WWW-Authenticate"] = "ApiKey"
            return response
        return await call_next(request)
