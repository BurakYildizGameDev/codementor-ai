"""İstemci kopması ve beklenmeyen hata (Faz 48): senkron uç ve SSE analizi iptal eder,
yarıda kalan analiz kaydedilmez; SSE'nin genel hata dalı loglanır."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable
from typing import Any

import pytest
from pydantic import BaseModel
from sqlmodel import select

from codementor.api.app import create_app
from codementor.api.disconnect import ClientDisconnectedError, run_until_disconnect
from codementor.api.sse import stream_analysis
from codementor.api.state import ApiState
from codementor.config import Settings
from codementor.models.provider import ChatMessage, GenerationOptions, ProviderResult
from codementor.models.request import AnalysisRequest
from codementor.pipeline.events import EventBus
from codementor.pipeline.orchestrator import Orchestrator
from codementor.providers.fake import FakeProvider
from codementor.storage.db import AnalysisRow, Database
from tests.api.test_api_auth import KEY, KEY_ENV
from tests.integration.conftest import LINKED_LIST

pytestmark = pytest.mark.anyio
BODY = {"code": LINKED_LIST, "question_id": "c-medium-linked-list"}


class HangingProvider(FakeProvider):
    """İptal gelene kadar bekler; başladığını ve iptal edildiğini kaydeder."""

    def __init__(self) -> None:
        super().__init__(script=[])
        self.started = asyncio.Event()
        self.cancelled = False

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> ProviderResult:
        self.started.set()
        try:
            await asyncio.sleep(30)
        except asyncio.CancelledError:
            self.cancelled = True
            raise
        raise AssertionError("iptal edilmeliydi")


def _saved(db: Database) -> int:
    with db.session() as session:
        return len(session.exec(select(AnalysisRow)).all())


# --- Senkron /v1/analyze ---


async def test_run_until_disconnect_returns_result_without_disconnect() -> None:
    never = asyncio.Event()

    async def receive() -> dict[str, Any]:
        await never.wait()
        return {"type": "http.disconnect"}

    async def work() -> int:
        return 42

    assert await run_until_disconnect(receive, work()) == 42


async def test_run_until_disconnect_cancels_work() -> None:
    cancelled = asyncio.Event()

    async def receive() -> dict[str, Any]:
        return {"type": "http.disconnect"}

    async def work() -> int:
        try:
            await asyncio.sleep(30)
        except asyncio.CancelledError:
            cancelled.set()
            raise
        return 0

    with pytest.raises(ClientDisconnectedError):
        await run_until_disconnect(receive, work())
    assert cancelled.is_set()


@pytest.mark.parametrize("with_key", [False, True], ids=["anahtarsiz", "api-anahtari"])
async def test_sync_analyze_cancelled_on_disconnect(
    settings: Settings, db: Database, monkeypatch: pytest.MonkeyPatch, with_key: bool
) -> None:
    """ASGI düzeyinde: gövde gelir, sağlayıcı beklerken istemci kopar → analiz iptal, yuva boş,
    kayıt yok. API anahtarı açıkken `BaseHTTPMiddleware` `receive`'i sarar; yine çalışmalı."""
    provider = HangingProvider()
    headers = [
        (b"host", b"127.0.0.1"),
        (b"content-type", b"application/json"),
    ]
    if with_key:
        monkeypatch.setenv(KEY_ENV, KEY)
        settings = settings.model_copy(
            update={"api": settings.api.model_copy(update={"api_key_env": KEY_ENV})}
        )
        headers.append((b"x-api-key", KEY.encode()))
    app = create_app(settings, db=db, provider_factory=lambda _n: provider)
    state: ApiState = app.state.codementor
    body = json.dumps(BODY).encode()
    sent: list[dict[str, Any]] = []
    first = True

    async def receive() -> dict[str, Any]:
        nonlocal first
        if first:
            first = False
            return {"type": "http.request", "body": body, "more_body": False}
        await provider.started.wait()
        return {"type": "http.disconnect"}

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/v1/analyze",
        "raw_path": b"/v1/analyze",
        "query_string": b"",
        "root_path": "",
        "headers": [*headers, (b"content-length", str(len(body)).encode())],
        "client": ("127.0.0.1", 50000),
        "server": ("127.0.0.1", 8000),
    }
    await asyncio.wait_for(app(scope, receive, send), 10)  # iptal edilmezse 30 sn asılı kalır
    assert provider.cancelled
    assert sent[0]["status"] == 499
    assert state.slots.active == 0
    assert _saved(db) == 0


# --- SSE ---


def _maker(settings: Settings, db: Database, provider: Any) -> Callable[[EventBus], Orchestrator]:
    return lambda bus: Orchestrator(settings, db, provider_factory=lambda _n: provider, bus=bus)


async def test_sse_disconnect_cancels_analysis(settings: Settings, db: Database) -> None:
    """Kabul: SSE akışı kapanınca (istemci koptu) analiz görevi iptal edilir, kayıt olmaz."""
    provider = HangingProvider()
    request = AnalysisRequest.model_validate(BODY)
    stream = stream_analysis(_maker(settings, db, provider), request, "/v1/analyze/stream")
    assert (await anext(stream)).startswith("event: stage")
    await asyncio.wait_for(provider.started.wait(), 10)
    await stream.aclose()  # StreamingResponse kopmada üreteci kapatır
    assert provider.cancelled
    assert _saved(db) == 0


class _Boom(Orchestrator):
    async def analyze(self, request: AnalysisRequest) -> Any:
        raise RuntimeError("gizli kullanıcı kodu: int main")


async def test_sse_unexpected_error_logged_and_500_event(
    settings: Settings, captured_logs: Callable[[], list[dict[str, Any]]]
) -> None:
    request = AnalysisRequest.model_validate(BODY)
    chunks = [
        chunk
        async for chunk in stream_analysis(
            lambda bus: _Boom(settings, None, bus=bus), request, "/v1/analyze/stream"
        )
    ]
    assert chunks[-1].startswith("event: error")
    assert '"status": 500' in chunks[-1]
    logs = [e for e in captured_logs() if e["event"] == "analysis_stream_failed"]
    assert [e["error"] for e in logs] == ["RuntimeError"]
    assert "int main" not in json.dumps(captured_logs())  # mesaj (kod parçası olabilir) yazılmaz


async def test_disconnect_watch_failure_logged(
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    """`receive` hata verirse analiz iptal edilir ve izleyicinin istisnası loglanır."""

    async def receive() -> dict[str, Any]:
        raise OSError("kanal kapandı")

    async def work() -> int:
        await asyncio.sleep(30)
        return 0

    with pytest.raises(ClientDisconnectedError):
        await run_until_disconnect(receive, work())
    events = [e for e in captured_logs() if e["event"] == "disconnect_watch_failed"]
    assert [e["error"] for e in events] == ["OSError"]
