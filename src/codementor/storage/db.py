"""SQLite depolama (mimari §11): SQLModel tabloları ve bağlantı.

Tablolar veritabanı şemasıdır (API/rapor şeması değil); rapor JSON olarak `report_json`'da
saklanır, doğruluk kaynağı `models/report.py`'dir.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import Engine, text
from sqlalchemy.pool import StaticPool
from sqlmodel import Field, Session, SQLModel, create_engine

from codementor.config import Settings

DB_PATH_ENV = "CODEMENTOR_DB_PATH"
DEFAULT_DB_PATH = Path.home() / ".codementor" / "codementor.db"
MEMORY = ":memory:"
# Oturum denemesi `INSERT … ON CONFLICT DO UPDATE … RETURNING` kullanır (Faz 49)
MIN_SQLITE = (3, 35)


def utcnow() -> datetime:
    return datetime.now(UTC)


class AnalysisRow(SQLModel, table=True):
    __tablename__ = "analyses"

    id: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=utcnow, index=True)  # budama sırası (Faz 49)
    cache_key: str = Field(index=True)
    language: str
    engine: str
    question_id: str | None = None
    session_id: str | None = None
    provider: str | None = None
    model: str | None = None
    early_exit: bool = False
    degraded: bool = False
    tokens_in: int = 0
    tokens_out: int = 0
    latency_ms: int = 0
    report_json: str


class SessionRow(SQLModel, table=True):
    """İpucu merdiveni: aynı oturum + soru için gönderim sayısı (mimari §5.4.3)."""

    __tablename__ = "sessions"

    session_id: str = Field(primary_key=True)
    question_id: str = Field(primary_key=True)
    attempt_count: int = 0
    current_hint_level: int = 1
    updated_at: datetime = Field(default_factory=utcnow)


class EvalRunRow(SQLModel, table=True):
    """Faz 12 (eval) için; şema §11'de tanımlı olduğu için şimdiden oluşturulur."""

    __tablename__ = "eval_runs"

    id: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    split: str
    provider: str
    model: str
    prompt_version: str
    metrics_json: str


class EvalResultRow(SQLModel, table=True):
    __tablename__ = "eval_results"

    run_id: str = Field(primary_key=True, foreign_key="eval_runs.id")
    sample_id: str = Field(primary_key=True)
    passed_checks_json: str
    report_json: str


def resolve_db_path(settings: Settings) -> Path | str:
    """Öncelik: `[storage] db_path` > `CODEMENTOR_DB_PATH` > `~/.codementor/codementor.db`."""
    if settings.storage.db_path is not None:
        return settings.storage.db_path
    env = os.environ.get(DB_PATH_ENV)
    if env:
        return env if env == MEMORY else Path(env)
    return DEFAULT_DB_PATH


class Database:
    """Motor + tablo oluşturma; her işlem kendi kısa `Session`'ını açar."""

    def __init__(self, path: Path | str) -> None:
        if sqlite3.sqlite_version_info < MIN_SQLITE:
            raise RuntimeError(
                f"SQLite {sqlite3.sqlite_version} çok eski; en az "
                f"{'.'.join(map(str, MIN_SQLITE))} gerekli (Python'u güncelleyin)."
            )
        if isinstance(path, Path):
            path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        # FastAPI senkron rotaları başka iş parçacığında çalışır; `:memory:` tek bağlantı paylaşır
        self.engine: Engine = create_engine(
            f"sqlite:///{path}",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool if path == MEMORY else None,
        )
        SQLModel.metadata.create_all(self.engine)
        with self.engine.begin() as connection:  # create_all eski tabloya indeks eklemez
            connection.execute(
                text("CREATE INDEX IF NOT EXISTS ix_analyses_created_at ON analyses (created_at)")
            )

    @classmethod
    def from_settings(cls, settings: Settings) -> Database:
        return cls(resolve_db_path(settings))

    def session(self) -> Session:
        return Session(self.engine)

    def close(self) -> None:
        self.engine.dispose()
