"""API güven sınırı (Faz 47, ADR-0023): Host, sağlayıcı izin listesi, girdi ve eşzamanlılık
sınırları. İstemci sunucu yapılandırmasını aşamaz."""

from __future__ import annotations

from collections.abc import AsyncIterator

import httpx
import pytest

from codementor.api.app import create_app
from codementor.api.guard import host_of
from codementor.api.state import ApiState
from codementor.config import Settings
from codementor.storage.db import Database
from tests.api.conftest import ClientFactory
from tests.integration.conftest import FakeFactory, analysis_reply, socratic_reply

pytestmark = pytest.mark.anyio
PROBLEM = "application/problem+json"
SMALL = {"code": "int x;", "language": "c"}


def _with_api(settings: Settings, **api: object) -> Settings:
    return settings.model_copy(update={"api": settings.api.model_copy(update=api)})


# --- Host (DNS rebinding) ---


async def test_foreign_host_header_rejected_400(client_for: ClientFactory) -> None:
    response = await client_for().get("/health", headers={"Host": "evil.example"})
    assert response.status_code == 400
    assert response.headers["content-type"] == PROBLEM


async def test_foreign_host_with_port_rejected(client_for: ClientFactory) -> None:
    response = await client_for().get("/v1/rules", headers={"Host": "evil.example:8000"})
    assert response.status_code == 400


@pytest.mark.parametrize(
    "host", ["127.0.0.1", "127.0.0.1:8000", "localhost:8000", "LOCALHOST", "[::1]:8000"]
)
async def test_loopback_hosts_accepted(client_for: ClientFactory, host: str) -> None:
    response = await client_for().get("/health", headers={"Host": host})
    assert response.status_code == 200


async def test_configured_allowed_hosts_used(client_for: ClientFactory, settings: Settings) -> None:
    client = client_for(cfg=_with_api(settings, allowed_hosts=["mentor.lan"]))
    assert (await client.get("/health", headers={"Host": "mentor.lan:8000"})).status_code == 200
    assert (await client.get("/health", headers={"Host": "127.0.0.1"})).status_code == 200
    assert (await client.get("/health", headers={"Host": "evil.example"})).status_code == 400


@pytest.mark.parametrize(
    ("header", "host"),
    [
        ("Example.com:80", "example.com"),
        ("[::1]:8000", "[::1]"),
        ("[::1]", "[::1]"),
        ("", None),
        ("[::1", None),
    ],
)
def test_host_of(header: str, host: str | None) -> None:
    assert host_of(header) == host


# --- Sağlayıcı izin listesi ---


async def test_unlisted_provider_422(client_for: ClientFactory, fake: FakeFactory) -> None:
    provider = fake()
    response = await client_for(provider).post(
        "/v1/analyze", json={**SMALL, "provider": "claude_cli"}
    )
    assert response.status_code == 422
    assert response.headers["content-type"] == PROBLEM
    assert "claude_cli" in response.json()["detail"]
    assert provider.calls == []


async def test_unlisted_provider_422_on_stream(client_for: ClientFactory) -> None:
    response = await client_for().post("/v1/analyze/stream", json={**SMALL, "provider": "codex"})
    assert response.status_code == 422


async def test_fallback_provider_allowed(
    client_for: ClientFactory, settings: Settings, fake: FakeFactory
) -> None:
    cfg = settings.model_copy(
        update={"providers": settings.providers.model_copy(update={"fallback": ["ollama"]})}
    )
    client = client_for(fake(analysis_reply(), socratic_reply()), cfg=cfg)
    response = await client.post("/v1/analyze", json={**SMALL, "provider": "ollama"})
    assert response.status_code == 200


async def test_explicit_allowed_providers(
    client_for: ClientFactory, settings: Settings, fake: FakeFactory
) -> None:
    cfg = _with_api(settings, allowed_providers=["gemini"])
    client = client_for(fake(), cfg=cfg)
    assert (await client.post("/v1/analyze", json={**SMALL, "provider": "fake"})).status_code == 422
    assert (
        await client.post("/v1/analyze", json={**SMALL, "provider": "gemini"})
    ).status_code != 422


async def test_request_without_provider_uses_default(
    client_for: ClientFactory, fake: FakeFactory
) -> None:
    response = await client_for(fake()).post("/v1/analyze", json=SMALL)
    assert response.status_code == 200


# --- Girdi sınırları ---


async def test_body_over_limit_413(client_for: ClientFactory) -> None:
    body = b'{"code": "' + b"x" * (2 * 1024 * 1024) + b'"}'
    response = await client_for().post(
        "/v1/analyze", content=body, headers={"content-type": "application/json"}
    )
    assert response.status_code == 413
    assert response.headers["content-type"] == PROBLEM


async def test_chunked_body_over_limit_413(client_for: ClientFactory, settings: Settings) -> None:
    async def chunks() -> AsyncIterator[bytes]:
        yield b'{"code": "'
        for _ in range(8):
            yield b"x" * 1024
        yield b'"}'

    client = client_for(cfg=_with_api(settings, max_body_bytes=4096))
    response = await client.post(
        "/v1/analyze", content=chunks(), headers={"content-type": "application/json"}
    )
    assert response.status_code == 413


async def test_body_under_limit_passes(client_for: ClientFactory, fake: FakeFactory) -> None:
    response = await client_for(fake()).post("/v1/analyze", json=SMALL)
    assert response.status_code == 200


async def test_code_over_four_times_max_bytes_413(
    client_for: ClientFactory, settings: Settings, fake: FakeFactory
) -> None:
    cfg = settings.model_copy(
        update={"limits": settings.limits.model_copy(update={"max_bytes": 100})}
    )
    provider = fake()
    response = await client_for(provider, cfg=cfg).post(
        "/v1/analyze", json={"code": "x" * 401, "language": "c"}
    )
    assert response.status_code == 413
    assert provider.calls == []


async def test_session_id_129_chars_422(client_for: ClientFactory) -> None:
    response = await client_for().post("/v1/analyze", json={**SMALL, "session_id": "s" * 129})
    assert response.status_code == 422
    assert response.headers["content-type"] == PROBLEM


@pytest.mark.parametrize("field", ["session_id", "question_id", "provider"])
@pytest.mark.parametrize("value", ["a/b", "a b", "../x", "", "ç"])
async def test_identifier_pattern_rejected(
    client_for: ClientFactory, field: str, value: str
) -> None:
    response = await client_for().post("/v1/analyze", json={**SMALL, field: value})
    assert response.status_code == 422


# --- Eşzamanlılık ---


async def test_concurrency_limit_returns_503(settings: Settings, db: Database) -> None:
    app = create_app(_with_api(settings, max_concurrent_analyses=1), db=db)
    state: ApiState = app.state.codementor
    assert state.slots.try_acquire()  # süren bir analiz gibi yuvayı tut
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://127.0.0.1") as client:
        busy = await client.post("/v1/analyze", json=SMALL)
        busy_stream = await client.post("/v1/analyze/stream", json=SMALL)
    assert busy.status_code == 503
    assert busy.headers["content-type"] == PROBLEM
    assert busy_stream.status_code == 503
    state.slots.release()
    assert state.slots.active == 0


async def test_slots_released_after_analyses(
    client_for: ClientFactory, settings: Settings, fake: FakeFactory
) -> None:
    client = client_for(fake(), cfg=_with_api(settings, max_concurrent_analyses=1))
    for _ in range(2):
        assert (await client.post("/v1/analyze", json=SMALL)).status_code == 200
    # akış da yuvasını bırakır; ardından yine kabul edilir
    stream = await client.post("/v1/analyze/stream", json=SMALL)
    assert stream.status_code == 200
    assert "event: report" in stream.text
    assert (await client.post("/v1/analyze", json=SMALL)).status_code == 200


async def test_rejected_request_does_not_hold_slot(
    client_for: ClientFactory, settings: Settings, fake: FakeFactory
) -> None:
    client = client_for(fake(), cfg=_with_api(settings, max_concurrent_analyses=1))
    assert (
        await client.post("/v1/analyze", json={**SMALL, "provider": "codex"})
    ).status_code == 422
    assert (await client.post("/v1/analyze", json=SMALL)).status_code == 200


# --- `serve` uyarısı ---


def test_exposure_warning(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    from codementor.cli.serve import exposure_warning

    assert exposure_warning(settings, "127.0.0.1") is None
    bare = exposure_warning(settings, "0.0.0.0")
    assert bare is not None
    assert "API anahtarı tanımlı değil" in bare
    assert "allowed_hosts" in bare
    assert "kimlik doğrulaması yok" not in bare  # eski, koşulsuz metin
    monkeypatch.setenv("CM_TEST_KEY", "gizli")
    guarded = exposure_warning(
        _with_api(settings, api_key_env="CM_TEST_KEY", allowed_hosts=["mentor.lan"]), "0.0.0.0"
    )
    assert guarded is not None
    assert "API anahtarı tanımlı değil" not in guarded
    assert "allowed_hosts" not in guarded


async def test_providers_endpoint_lists_allowed(
    client_for: ClientFactory, settings: Settings
) -> None:
    """Web arayüzü seçimi `/v1/providers`'tan yapar; liste izin listesiyle aynı olmalı."""
    cfg = _with_api(settings, allowed_providers=["gemini", "anthropic"])
    response = await client_for(cfg=cfg).get("/v1/providers")
    assert [s["name"] for s in response.json()] == ["gemini", "anthropic"]
