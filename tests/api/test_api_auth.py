"""İsteğe bağlı API anahtarı (Faz 26): `api.api_key_env` doluysa `/v1/*` `X-API-Key` ister."""

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


async def test_missing_or_wrong_key_rejected(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(KEY_ENV, KEY)
    client = client_for(cfg=_with_key(settings))
    for headers in ({}, {"X-API-Key": "yanlis"}, {"X-API-Key": KEY + "x"}):
        response = await client.get("/v1/rules", headers=headers)
        assert response.status_code == 401
        assert response.headers["content-type"].startswith("application/problem+json")
        assert response.headers["www-authenticate"] == "ApiKey"
        body = response.json()
        assert body["title"] == "Yetkisiz"
        assert KEY not in response.text


async def test_correct_key_allowed(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(KEY_ENV, KEY)
    client = client_for(cfg=_with_key(settings))
    response = await client.get("/v1/rules", headers={"X-API-Key": KEY})
    assert response.status_code == 200


async def test_health_stays_open(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(KEY_ENV, KEY)
    client = client_for(cfg=_with_key(settings))
    assert (await client.get("/health")).status_code == 200


async def test_no_key_configured_means_open(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(KEY_ENV, raising=False)
    # ad verildi ama değişken boş: koruma kapalı (yerel varsayılan davranış)
    assert (await client_for(cfg=_with_key(settings)).get("/v1/rules")).status_code == 200
    assert (await client_for().get("/v1/rules")).status_code == 200


async def test_cors_preflight_allows_key_header(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(KEY_ENV, KEY)
    client = client_for(cfg=_with_key(settings))
    origin = settings.api.cors_origins[0]
    response = await client.options(
        "/v1/analyze",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-api-key",
        },
    )
    assert response.status_code == 200
    assert "x-api-key" in response.headers["access-control-allow-headers"].lower()
