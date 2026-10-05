"""API depolama tutarlılığı (Faz 49): aynı oturumda eşzamanlı gönderim, uyumsuz eski kayıt,
bozuk soru bankası, bankanın süreç başına bir kez yüklenmesi."""

from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
import pytest

from codementor.api.app import create_app
from codementor.api.state import ApiState
from codementor.config import Settings
from codementor.pipeline.ids import new_ulid
from codementor.providers.fake import FakeReply
from codementor.questions import QuestionBank
from codementor.storage import sessions
from codementor.storage.db import AnalysisRow, Database
from tests.integration.conftest import LINKED_LIST, FakeFactory, analysis_reply, socratic_reply

pytestmark = pytest.mark.anyio
QUESTION = "c-medium-linked-list"
BODY = {
    "code": LINKED_LIST,
    "question_id": QUESTION,
    "session_id": "api-oturum",
    "options": {"use_cache": False},
}


def _client(app: object) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),  # type: ignore[arg-type]
        base_url="http://127.0.0.1",
    )


async def test_concurrent_session_posts_no_500(
    settings: Settings, db: Database, fake: FakeFactory
) -> None:
    """Kabul: `asyncio.gather` ile iki gönderim deneme 1 ve 2 alır, 500 yok."""

    def provider(_name: str) -> object:
        return fake(FakeReply(data=analysis_reply(), delay_ms=50), socratic_reply())

    app = create_app(settings, db=db, provider_factory=provider)  # type: ignore[arg-type]
    async with _client(app) as client:
        first, second = await asyncio.gather(
            client.post("/v1/analyze", json=BODY), client.post("/v1/analyze", json=BODY)
        )
    assert (first.status_code, second.status_code) == (200, 200)
    levels = sorted(r.json()["socratic"]["hint_level"] for r in (first, second))
    assert levels == [1, 2]  # orta zorluk: deneme 1 → ipucu 1, deneme 2 → ipucu 2
    assert sessions.next_attempt(db, "api-oturum", QUESTION) == 3


async def test_stored_incompatible_report_404(settings: Settings, db: Database) -> None:
    old_id = new_ulid()
    with db.session() as session:
        session.add(
            AnalysisRow(
                id=old_id, cache_key="eski", language="c", engine="none", report_json='{"v": 0}'
            )
        )
        session.commit()
    async with _client(create_app(settings, db=db)) as client:
        response = await client.get(f"/v1/analyses/{old_id}")
    assert response.status_code == 404


def _broken_bank(settings: Settings, tmp_path: Path) -> Settings:
    bank = tmp_path / "sorular"
    bank.mkdir()
    (bank / "bozuk.yaml").write_text("id: [kapanmamış\n", encoding="utf-8")
    data = settings.data.model_copy(update={"questions_dir": bank})
    return settings.model_copy(update={"data": data})


async def test_question_bank_error_503(
    settings: Settings, db: Database, fake: FakeFactory, tmp_path: Path
) -> None:
    app = create_app(_broken_bank(settings, tmp_path), db=db, provider_factory=lambda _n: fake())
    async with _client(app) as client:
        analyze = await client.post("/v1/analyze", json=BODY)
        listing = await client.get("/v1/questions")
    for response in (analyze, listing):
        assert response.status_code == 503
        assert response.headers["content-type"].startswith("application/problem+json")
    assert "Soru bankası" in analyze.json()["detail"]


async def test_bank_loaded_once_per_state(
    settings: Settings, db: Database, fake: FakeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    loads: list[Path] = []
    original = QuestionBank.load

    def counting(directory: Path) -> QuestionBank:
        loads.append(directory)
        return original(directory)

    monkeypatch.setattr(QuestionBank, "load", staticmethod(counting))

    def provider(_name: str) -> object:
        return fake(analysis_reply(), socratic_reply())

    app = create_app(settings, db=db, provider_factory=provider)  # type: ignore[arg-type]
    state: ApiState = app.state.codementor
    async with _client(app) as client:
        for _ in range(3):
            assert (await client.post("/v1/analyze", json=BODY)).status_code == 200
    assert len(loads) == 1
    assert state.questions() is state.questions()
