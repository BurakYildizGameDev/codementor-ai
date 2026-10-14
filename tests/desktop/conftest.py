"""Masaüstü testleri: ağsız FakeProvider, geçici SQLite ve geçici tercih dizini."""

from __future__ import annotations

import asyncio
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from pydantic import BaseModel

from codementor.api.state import ApiState
from codementor.config import Settings
from codementor.desktop.connections import KeyStore
from codementor.models.provider import ChatMessage, GenerationOptions, ProviderResult
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

# Tk'siz Python'larda (ör. Linux CI'daki uv Python'u) pencere testleri toplanmaz; Tk gerektirmeyen
# masaüstü testleri (görünüm modeli, köprü, bağlantılar, renklendirme) yine koşar.
try:
    import tkinter  # noqa: F401
except ImportError:
    collect_ignore = [
        "test_app.py",
        "test_user_questions_app.py",
        "test_faz_c_app.py",
        "test_launch_db.py",
    ]


def scripted() -> FakeProvider:
    """Bağlı liste kodu için iki geçişlik gerçekçi yanıt (her analizde yeni sağlayıcı)."""
    return FakeProvider(
        script=[FakeReply(data=analysis_reply()), FakeReply(data=socratic_reply())],
        retry=RetryPolicy(max_retries=0),
    )


@pytest.fixture
def core(settings: Settings, db: Database) -> ApiState:  # noqa: F811
    return ApiState(settings, db=db, provider_factory=lambda _name: scripted())


@dataclass
class StallingProvider(FakeProvider):
    """LLM çağrısında takılır (30 sn); iptal edilirse `cancelled` olayını işaretler (Faz 19)."""

    started: threading.Event = field(default_factory=threading.Event)
    cancelled: threading.Event = field(default_factory=threading.Event)

    async def generate_structured(
        self, messages: list[ChatMessage], output_model: type[BaseModel], options: GenerationOptions
    ) -> ProviderResult:
        self.started.set()
        try:
            await asyncio.sleep(30)
        except asyncio.CancelledError:
            self.cancelled.set()
            raise
        raise AssertionError("iptal edilmeliydi")


@pytest.fixture
def stalling() -> StallingProvider:
    return StallingProvider(script=[], retry=RetryPolicy(max_retries=0))


@pytest.fixture
def stalled_core(settings: Settings, db: Database, stalling: StallingProvider) -> ApiState:  # noqa: F811
    return ApiState(settings, db=db, provider_factory=lambda _name: stalling)


@pytest.fixture
def prefs_dir(tmp_path: Path) -> Path:
    folder = tmp_path / "user"
    folder.mkdir()
    return folder


API_KEY_ENVS = ("ANTHROPIC_API_KEY", "GEMINI_API_KEY")


class FakeVault:
    """`keyring` yerine bellek içi kasa (testler gerçek Windows kasasına dokunmaz)."""

    def __init__(self) -> None:
        self.items: dict[tuple[str, str], str] = {}
        self.broken = False

    def get_password(self, service_name: str, username: str) -> str | None:
        if self.broken:
            raise RuntimeError("kasa kilitli")
        return self.items.get((service_name, username))

    def set_password(self, service_name: str, username: str, password: str) -> None:
        if self.broken:
            raise RuntimeError("kasa kilitli")
        self.items[(service_name, username)] = password

    def delete_password(self, service_name: str, username: str) -> None:
        if (service_name, username) not in self.items:
            raise type("PasswordDeleteError", (Exception,), {})()
        del self.items[(service_name, username)]


@pytest.fixture(autouse=True)
def _clean_key_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Uygulama anahtarı `os.environ`'a koyar; test sonunda eski hâline döner."""
    for env in API_KEY_ENVS:
        monkeypatch.delenv(env, raising=False)


@pytest.fixture
def vault() -> FakeVault:
    return FakeVault()


@pytest.fixture
def store(vault: FakeVault) -> KeyStore:
    return KeyStore(vault)
