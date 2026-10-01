"""Masaüstü testleri: ağsız FakeProvider, geçici SQLite ve geçici tercih dizini."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from codementor.api.state import ApiState
from codementor.config import Settings
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.storage.db import Database
from tests.integration.conftest import (  # noqa: F401
    analysis_reply,
    db,
    settings,
    socratic_reply,
)

StateFactory = Callable[..., ApiState]


def scripted() -> FakeProvider:
    """Bağlı liste kodu için iki geçişlik gerçekçi yanıt (her analizde yeni sağlayıcı)."""
    return FakeProvider(
        script=[FakeReply(data=analysis_reply()), FakeReply(data=socratic_reply())],
        retry=RetryPolicy(max_retries=0),
    )


@pytest.fixture
def core(settings: Settings, db: Database) -> ApiState:  # noqa: F811
    return ApiState(settings, db=db, provider_factory=lambda _name: scripted())


@pytest.fixture
def prefs_dir(tmp_path: Path) -> Path:
    folder = tmp_path / "user"
    folder.mkdir()
    return folder
