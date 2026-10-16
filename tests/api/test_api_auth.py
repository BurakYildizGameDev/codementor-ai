"""İsteğe bağlı API anahtarı (Faz 26): `api.api_key_env` doluysa `/v1/*` `X-API-Key` ister."""

from __future__ import annotations

import pytest

from codementor.config import Settings
from tests.api.conftest import ClientFactory
from tests.integration.conftest import LINKED_LIST, FakeFactory, analysis_reply, socratic_reply

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


async def test_delete_without_key_rejected_and_record_kept(
    client_for: ClientFactory,
    settings: Settings,
    fake: FakeFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Denetim O4 (Faz 62): anahtar tanımlıyken anahtarsız DELETE 401 döner ve kayıt silinmez."""
    monkeypatch.setenv(KEY_ENV, KEY)
    client = client_for(fake(analysis_reply(), socratic_reply()), cfg=_with_key(settings))
    auth = {"X-API-Key": KEY}
    body = {"code": LINKED_LIST, "question_id": "c-medium-linked-list"}
    analysis_id = (await client.post("/v1/analyze", json=body, headers=auth)).json()["analysis_id"]
    for headers in ({}, {"X-API-Key": "yanlis"}):
        response = await client.delete(f"/v1/analyses/{analysis_id}", headers=headers)
        assert response.status_code == 401
    assert (await client.get(f"/v1/analyses/{analysis_id}", headers=auth)).status_code == 200
    deleted = await client.delete(f"/v1/analyses/{analysis_id}", headers=auth)
    assert deleted.status_code == 204


async def test_trailing_slash_and_encoding_do_not_escape_key(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D14 sertleştirme: `%76` yazımı ve sondaki `/` (FastAPI 307'si) korumayı atlamaz."""
    monkeypatch.setenv(KEY_ENV, KEY)
    client = client_for(cfg=_with_key(settings))
    for path in (
        "/docs/",
        "/redoc/",
        "/openapi.json/",
        "/health/ready/",
        "/docs/oauth2-redirect/",
    ):
        without = await client.get(path)
        assert without.status_code == 401, f"{path} başlıksız 401 olmalı (307 değil)"
        with_key = await client.get(path, headers={"X-API-Key": KEY})
        assert with_key.status_code in {200, 307}, f"{path} başlıklı normal yanıt vermeli"
    # yüzde kodlamalı `/v1` yazımı da korunur (Starlette `scope["path"]`'i çözer)
    assert (await client.get("/%76%31/rules")).status_code == 401
    assert (await client.get("/%76%31/rules", headers={"X-API-Key": KEY})).status_code == 200
    # kodsuz yol varyantları rotaya ulaşmıyor (yönlendirme ile sızmıyor)
    assert (await client.get("//v1/rules")).status_code == 404
    # `/health` ve sondaki `/` yönlendirmesi açık kalır
    assert (await client.get("/health")).status_code == 200
    assert (await client.get("/health/")).status_code == 307


async def test_internal_endpoints_protected_with_key(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz E (E7, D14): Anahtarlı modda /health/ready, /docs, /redoc, /openapi.json korunur,
    /health açık kalır.
    """
    monkeypatch.setenv(KEY_ENV, KEY)
    cfg = settings.model_copy(
        update={
            "api": settings.api.model_copy(update={"api_key_env": KEY_ENV}),
            "providers": settings.providers.model_copy(update={"default": "anthropic"}),
        }
    )
    client_keyed = client_for(cfg=cfg)
    protected_paths = [
        "/health/ready",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/docs/oauth2-redirect",
    ]

    # Anahtarlı mod: başlıksız 401
    for path in protected_paths:
        resp = await client_keyed.get(path)
        assert resp.status_code == 401, f"{path} başlıksız 401 olmalı"

    # Anahtarlı mod: başlıklı normal (200)
    for path in protected_paths:
        resp = await client_keyed.get(path, headers={"X-API-Key": KEY})
        assert resp.status_code == 200, f"{path} başlıklı 200 olmalı"

    # /health her zaman açık
    assert (await client_keyed.get("/health")).status_code == 200

    # Anahtarsız mod: hepsi açık
    monkeypatch.delenv(KEY_ENV, raising=False)
    cfg_open = settings.model_copy(
        update={"providers": settings.providers.model_copy(update={"default": "anthropic"})}
    )
    client_open = client_for(cfg=cfg_open)
    for path in protected_paths:
        resp = await client_open.get(path)
        assert resp.status_code == 200, f"{path} anahtarsız modda açık olmalı"
