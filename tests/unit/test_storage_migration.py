"""Faz 49 Ü9 / KALAN_ISLER İş 8: Şema göçü ve bozuk kayıt kurtarma testleri."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from sqlalchemy import text

from codementor.storage import cache
from codementor.storage.db import SCHEMA_DB_VERSION, AnalysisRow, Database, SessionRow


def test_schema_migration_adds_missing_columns(tmp_path: Path) -> None:
    """Eski şema (eksik sütunlar, user_version=0): Database açılışında sütunlar eklenir."""
    db_file = tmp_path / "legacy.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute(
        """
        CREATE TABLE analyses (
            id VARCHAR PRIMARY KEY,
            created_at TIMESTAMP,
            cache_key VARCHAR,
            language VARCHAR,
            engine VARCHAR
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE sessions (
            session_id VARCHAR,
            question_id VARCHAR,
            attempt_count INT,
            current_hint_level INT,
            PRIMARY KEY (session_id, question_id)
        )
        """
    )
    conn.execute("PRAGMA user_version = 0")
    conn.commit()
    conn.close()

    db = Database(db_file)
    try:
        with db.engine.connect() as connection:
            ver = connection.execute(text("PRAGMA user_version")).scalar()
            assert ver == SCHEMA_DB_VERSION

            cursor = connection.execute(text("PRAGMA table_info(analyses)"))
            cols = {row[1] for row in cursor.fetchall()}
            expected_cols = {
                "session_id",
                "question_id",
                "provider",
                "model",
                "early_exit",
                "report_json",
            }
            assert expected_cols <= cols

            cursor_sess = connection.execute(text("PRAGMA table_info(sessions)"))
            sess_cols = {row[1] for row in cursor_sess.fetchall()}
            assert "updated_at" in sess_cols

        # Yeni şemayla yazma/okuma hatasız çalışır
        with db.session() as s:
            s.add(
                AnalysisRow(
                    id="migrated_1",
                    cache_key="k1",
                    language="c",
                    engine="none",
                    question_id="q1",
                    session_id="s1",
                    report_json="{}",
                )
            )
            s.add(
                SessionRow(
                    session_id="s1",
                    question_id="q1",
                    attempt_count=1,
                    current_hint_level=1,
                )
            )
            s.commit()

        rows = cache.list_analyses(db)
        assert len(rows) == 1
        assert rows[0].id == "migrated_1"
        assert rows[0].session_id == "s1"
    finally:
        db.close()


def test_list_analyses_recovers_from_corrupt_created_at(tmp_path: Path) -> None:
    """created_at alanında bozuk ISO metni olan satır list_analyses'i düşürmez."""
    db_file = tmp_path / "corrupt.db"
    db = Database(db_file)
    try:
        with db.session() as s:
            s.add(
                AnalysisRow(
                    id="valid_1",
                    cache_key="k_valid",
                    language="c",
                    engine="none",
                    report_json="{}",
                )
            )
            s.commit()

        # Doğrudan bozuk bir created_at metni enjekte et
        with db.engine.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO analyses (id, created_at, cache_key, language, engine, "
                    "report_json, early_exit, degraded, tokens_in, tokens_out, latency_ms) "
                    "VALUES ('corrupt_1', 'bozuk-iso-tarih', 'k_bad', 'c', 'none', '{}', "
                    "0, 0, 0, 0, 0)"
                )
            )

        rows = cache.list_analyses(db)
        assert len(rows) == 2
        ids = {r.id for r in rows}
        assert ids == {"valid_1", "corrupt_1"}
    finally:
        db.close()


def test_list_analyses_page_recovers_from_corrupt_created_at(tmp_path: Path) -> None:
    """created_at alanında bozuk ISO metni olan satır list_analyses_page'i düşürmez."""
    db_file = tmp_path / "corrupt_page.db"
    db = Database(db_file)
    try:
        with db.session() as s:
            s.add(
                AnalysisRow(
                    id="valid_1",
                    cache_key="k_valid",
                    language="python",
                    engine="none",
                    report_json="{}",
                )
            )
            s.commit()

        with db.engine.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO analyses (id, created_at, cache_key, language, engine, "
                    "report_json, early_exit, degraded, tokens_in, tokens_out, latency_ms) "
                    "VALUES ('corrupt_1', 'invalid-date-format', 'k_bad', 'python', "
                    "'none', '{}', 0, 0, 0, 0, 0)"
                )
            )

        items, _ = cache.list_analyses_page(db, limit=10)
        assert len(items) == 2
        ids = {r.id for r in items}
        assert ids == {"valid_1", "corrupt_1"}
    finally:
        db.close()
