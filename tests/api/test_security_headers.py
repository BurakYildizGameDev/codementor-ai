"""Güvenlik başlıkları testleri (Faz E: E6).

Her HTTP yanıtında (200, 401, 404, 413 dahil):
- X-Content-Type-Options: nosniff
- Referrer-Policy: no-referrer
bulunmalıdır.
"""

from __future__ import annotations

import pytest

from codementor.config import Settings
from tests.api.conftest import ClientFactory

pytestmark = pytest.mark.anyio

KEY_ENV = "CODEMENTOR_TEST_API_KEY"
KEY = "cm-test-anahtar-0123456789"


def _with_key(settings: Settings) -> Settings:
    return settings.model_copy(
        update={"api": settings.api.model_copy(update={"api_key_env": KEY_ENV})}
    )


def _assert_security_headers(headers: dict[str, str] | any) -> None:
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("referrer-policy") == "no-referrer"


async def test_security_headers_on_200(client_for: ClientFactory) -> None:
    client = client_for()
    resp = await client.get("/health")
    assert resp.status_code == 200
    _assert_security_headers(resp.headers)


async def test_security_headers_on_404(client_for: ClientFactory) -> None:
    client = client_for()
    resp = await client.get("/v1/analyses/01M4VC2PJ5PRBWEWKRYXGQE8FA")
    assert resp.status_code == 404
    _assert_security_headers(resp.headers)


async def test_security_headers_on_401(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(KEY_ENV, KEY)
    client = client_for(cfg=_with_key(settings))
    resp = await client.get("/v1/rules")
    assert resp.status_code == 401
    _assert_security_headers(resp.headers)


async def test_security_headers_on_413(client_for: ClientFactory, settings: Settings) -> None:
    # Çok küçük max_body_bytes ile 413 tetikle
    tight_settings = settings.model_copy(
        update={"api": settings.api.model_copy(update={"max_body_bytes": 10})}
    )
    client = client_for(cfg=tight_settings)
    resp = await client.post(
        "/v1/analyze",
        content=b'{"code": "very large content exceeding limit"}',
        headers={"content-type": "application/json"},
    )
    assert resp.status_code == 413
    _assert_security_headers(resp.headers)
