"""API testleri: httpx.AsyncClient + ASGI (ağsız), FakeProvider, geçici SQLite."""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from typing import Any

import httpx
import pytest

from codementor.api.app import create_app
from codementor.config import Settings
from codementor.providers.fake import FakeProvider
from codementor.storage.db import Database
from tests.integration.conftest import anyio_backend, db, fake, settings  # noqa: F401

ClientFactory = Callable[..., Any]


@pytest.fixture
async def client_for(
    settings: Settings,  # noqa: F811
    db: Database,  # noqa: F811
) -> AsyncIterator[ClientFactory]:
    """`client_for(provider)` → aynı veritabanını paylaşan AsyncClient."""
    clients: list[httpx.AsyncClient] = []

    def make(
        provider: FakeProvider | None = None, cfg: Settings | None = None
    ) -> httpx.AsyncClient:
        app = create_app(
            cfg or settings,
            db=db,
            provider_factory=(lambda _n: provider) if provider is not None else None,
        )
        client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")
        clients.append(client)
        return client

    yield make
    for client in clients:
        await client.aclose()
