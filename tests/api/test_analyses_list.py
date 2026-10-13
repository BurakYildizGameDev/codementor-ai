"""Analiz listesi ve silme uçları (Faz E: E1, E2)."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from codementor.config import Settings
from codementor.models.enums import CompilationStatus, Engine, Language
from codementor.models.findings import CompilationBlock
from codementor.models.report import AnalysisReport, ReportMeta
from codementor.pipeline.ids import new_ulid
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.storage import cache
from codementor.storage.db import Database, utcnow
from tests.api.conftest import ClientFactory
from tests.integration.conftest import LINKED_LIST, FakeFactory, analysis_reply, socratic_reply

pytestmark = pytest.mark.anyio

KEY_ENV = "CODEMENTOR_TEST_API_KEY"
KEY = "cm-test-anahtar-0123456789"


def _with_key(settings: Settings) -> Settings:
    return settings.model_copy(
        update={"api": settings.api.model_copy(update={"api_key_env": KEY_ENV})}
    )


def _make_dummy_report(
    analysis_id: str, code: str = "int x = 1;", created_at: datetime | None = None
) -> AnalysisReport:
    return AnalysisReport(
        analysis_id=analysis_id,
        language=Language.C,
        engine=Engine.NONE,
        created_at=created_at or utcnow(),
        compilation=CompilationBlock(status=CompilationStatus.SKIPPED, diagnostics=[]),
        complexity=None,
        findings=[],
        socratic=None,
        question_id=None,
        difficulty=None,
        meta=ReportMeta(
            provider="fake",
            model="fake-model",
            prompt_version="1.0",
            rules_version="1.0",
            schema_version="1.1",
            tokens_in=5,
            tokens_out=10,
            stage_latency_ms={},
            early_exit=False,
            cache_hit=False,
            degraded=False,
            repair_attempts=0,
            warnings=[],
        ),
    )


async def test_empty_list(client_for: ClientFactory) -> None:
    client = client_for()
    resp = await client.get("/v1/analyses")
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"items": [], "next_cursor": None}


async def test_order_newest_first(client_for: ClientFactory, db: Database) -> None:
    # 3 analiz kaydet (zaman sırasıyla)
    now = utcnow()
    id1, id2, id3 = new_ulid(), new_ulid(), new_ulid()
    r1 = _make_dummy_report(id1, created_at=now)
    r2 = _make_dummy_report(id2, created_at=now + timedelta(seconds=1))
    r3 = _make_dummy_report(id3, created_at=now + timedelta(seconds=2))
    cache.save_analysis(db, r1, key="k1", session_id=None, latency_ms=10)
    cache.save_analysis(db, r2, key="k2", session_id=None, latency_ms=10)
    cache.save_analysis(db, r3, key="k3", session_id=None, latency_ms=10)

    client = client_for()
    resp = await client.get("/v1/analyses")
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert len(items) == 3
    # En yeni önce (id3, id2, id1)
    assert [it["analysis_id"] for it in items] == [id3, id2, id1]


async def test_pagination(client_for: ClientFactory, db: Database) -> None:
    now = utcnow()
    id1, id2, id3 = new_ulid(), new_ulid(), new_ulid()
    cache.save_analysis(
        db, _make_dummy_report(id1, created_at=now), key="k1", session_id=None, latency_ms=10
    )
    cache.save_analysis(
        db,
        _make_dummy_report(id2, created_at=now + timedelta(seconds=1)),
        key="k2",
        session_id=None,
        latency_ms=10,
    )
    cache.save_analysis(
        db,
        _make_dummy_report(id3, created_at=now + timedelta(seconds=2)),
        key="k3",
        session_id=None,
        latency_ms=10,
    )

    client = client_for()
    resp1 = await client.get("/v1/analyses?limit=2")
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert len(data1["items"]) == 2
    assert [it["analysis_id"] for it in data1["items"]] == [id3, id2]
    cursor = data1["next_cursor"]
    assert cursor == id2

    resp2 = await client.get(f"/v1/analyses?limit=2&before={cursor}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert len(data2["items"]) == 1
    assert data2["items"][0]["analysis_id"] == id1
    assert data2["next_cursor"] is None


async def test_limit_bounds(client_for: ClientFactory) -> None:
    client = client_for()
    assert (await client.get("/v1/analyses?limit=0")).status_code == 422
    assert (await client.get("/v1/analyses?limit=101")).status_code == 422


async def test_list_requires_key_when_configured(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(KEY_ENV, KEY)
    client = client_for(cfg=_with_key(settings))
    resp = await client.get("/v1/analyses")
    assert resp.status_code == 401
    resp_with_key = await client.get("/v1/analyses", headers={"X-API-Key": KEY})
    assert resp_with_key.status_code == 200


async def test_list_has_no_code(client_for: ClientFactory, fake: FakeFactory) -> None:
    secret_code = "SECRET_TOKEN_UNIQUE_12345_XYZ"
    code_content = f"// {secret_code}\nint main() {{ return 0; }}"

    def provider(_name: str) -> FakeProvider:
        return fake(FakeReply(data=analysis_reply()), socratic_reply())

    client = client_for(provider=provider("fake"))
    res_post = await client.post(
        "/v1/analyze",
        json={"code": code_content, "language": "c", "engine": "none"},
    )
    assert res_post.status_code == 200

    resp = await client.get("/v1/analyses")
    assert resp.status_code == 200
    assert secret_code not in resp.text


async def test_delete_all_analyses(client_for: ClientFactory, db: Database) -> None:
    cache.save_analysis(
        db, _make_dummy_report(new_ulid()), key="k1", session_id=None, latency_ms=10
    )
    cache.save_analysis(
        db, _make_dummy_report(new_ulid()), key="k2", session_id=None, latency_ms=10
    )

    client = client_for()
    resp_list = await client.get("/v1/analyses")
    assert len(resp_list.json()["items"]) == 2

    resp_del = await client.delete("/v1/analyses")
    assert resp_del.status_code == 200
    assert resp_del.json() == {"deleted": 2}

    resp_after = await client.get("/v1/analyses")
    assert resp_after.json()["items"] == []


async def test_delete_all_requires_key(
    client_for: ClientFactory, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(KEY_ENV, KEY)
    client = client_for(cfg=_with_key(settings))
    assert (await client.delete("/v1/analyses")).status_code == 401
    assert (await client.delete("/v1/analyses", headers={"X-API-Key": KEY})).status_code == 200


async def test_delete_session(client_for: ClientFactory, fake: FakeFactory, db: Database) -> None:
    def provider(_name: str) -> FakeProvider:
        return fake(FakeReply(data=analysis_reply()), socratic_reply())

    client = client_for(provider=provider("fake"))
    body = {
        "code": LINKED_LIST,
        "question_id": "c-medium-linked-list",
        "session_id": "test-session-1",
        "options": {"use_cache": False},
    }
    r1 = await client.post("/v1/analyze", json=body)
    assert r1.status_code == 200
    assert r1.json()["socratic"]["hint_level"] == 1

    r2 = await client.post("/v1/analyze", json=body)
    assert r2.status_code == 200
    assert r2.json()["socratic"]["hint_level"] == 2

    # Oturumu sil
    resp_del = await client.delete("/v1/sessions/test-session-1")
    assert resp_del.status_code == 204

    # Aynı oturumla yeni analiz tekrar başlangıç ipucu seviyesinde olmalı
    r3 = await client.post("/v1/analyze", json=body)
    assert r3.status_code == 200
    assert r3.json()["socratic"]["hint_level"] == 1


async def test_delete_unknown_session_404(client_for: ClientFactory) -> None:
    client = client_for()
    resp = await client.delete("/v1/sessions/non-existent-session")
    assert resp.status_code == 404
