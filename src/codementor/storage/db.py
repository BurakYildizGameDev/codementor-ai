"""SQLite depolama (mimari §11): SQLModel tabloları ve bağlantı.

Tablolar veritabanı şemasıdır (API/rapor şeması değil); rapor JSON olarak `report_json`'da
saklanır, doğruluk kaynağı `models/report.py`'dir.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, event, text
from sqlalchemy.pool import StaticPool
from sqlmodel import Field, Session, SQLModel, create_engine

from codementor.config import Settings

DB_PATH_ENV = "CODEMENTOR_DB_PATH"
DEFAULT_DB_PATH = Path.home() / ".codementor" / "codementor.db"
MEMORY = ":memory:"
# Oturum denemesi `INSERT … ON CONFLICT DO UPDATE … RETURNING` kullanır (Faz 49)
MIN_SQLITE = (3, 35)
SCHEMA_DB_VERSION = 2


def _migrate(connection: Any, current: int) -> None:
    """Veritabanı şema göçü (Faz F, D19; Faz 49 Ü9)."""
    cursor = connection.execute(text("PRAGMA table_info(analyses)"))
    existing_cols = {row[1] for row in cursor.fetchall()}
    if existing_cols:  # Tablo zaten varsa eksik sütunları ekle
        expected = {
            "question_id": "VARCHAR",
            "session_id": "VARCHAR",
            "provider": "VARCHAR",
            "model": "VARCHAR",
            "early_exit": "BOOLEAN DEFAULT 0",
            "degraded": "BOOLEAN DEFAULT 0",
            "tokens_in": "INTEGER DEFAULT 0",
            "tokens_out": "INTEGER DEFAULT 0",
            "latency_ms": "INTEGER DEFAULT 0",
            "report_json": "TEXT DEFAULT '{}'",
        }
        for col_name, col_type in expected.items():
            if col_name not in existing_cols:
                connection.execute(text(f"ALTER TABLE analyses ADD COLUMN {col_name} {col_type}"))

    cursor_sessions = connection.execute(text("PRAGMA table_info(sessions)"))
    existing_sessions_cols = {row[1] for row in cursor_sessions.fetchall()}
    if existing_sessions_cols and "updated_at" not in existing_sessions_cols:
        connection.execute(text("ALTER TABLE sessions ADD COLUMN updated_at TIMESTAMP"))

    connection.execute(text(f"PRAGMA user_version = {SCHEMA_DB_VERSION}"))


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

        @event.listens_for(self.engine, "connect")
        def _sqlite_connect(dbapi_connection: Any, connection_record: Any) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA secure_delete = ON")
            cursor.execute("PRAGMA busy_timeout = 5000")
            if path != MEMORY:
                cursor.execute("PRAGMA journal_mode = WAL")
            cursor.close()

        try:
            SQLModel.metadata.create_all(self.engine)
            with self.engine.begin() as connection:  # create_all eski tabloya indeks eklemez
                connection.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS ix_analyses_created_at ON analyses (created_at)"
                    )
                )
                current_v = connection.execute(text("PRAGMA user_version")).scalar() or 0
                if current_v < SCHEMA_DB_VERSION:
                    _migrate(connection, current_v)
        except Exception:
            self.engine.dispose()
            raise

    @classmethod
    def from_settings(cls, settings: Settings) -> Database:
        db = cls(resolve_db_path(settings))
        if settings.storage.session_retention_days is not None:
            from codementor.storage.sessions import prune_old_sessions

            prune_old_sessions(db, settings.storage.session_retention_days)
        return db

    def session(self) -> Session:
        return Session(self.engine)

    def close(self) -> None:
        self.engine.dispose()
