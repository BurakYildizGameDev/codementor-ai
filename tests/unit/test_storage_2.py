"""Depolama (mimari §11): önbellek anahtarı, önbellek, oturumlar, veritabanı yolu, ULID.

Bölüm 2/2.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from codementor.config import load_settings
from codementor.pipeline.ids import new_ulid
from codementor.storage import cache, sessions
from codementor.storage.db import (
    MEMORY,
    SCHEMA_DB_VERSION,
    AnalysisRow,
    Database,
    SessionRow,
    utcnow,
)
from tests.unit.test_report_render import _report


def test_new_analysis_saved_after_clear(db: Database) -> None:
    """Denetim O4: temizledikten sonra yeni analiz normal kaydedilir ve önbellekten döner."""
    cache.save_analysis(db, _report(), key="eski", session_id=None, latency_ms=5)
    cache.clear_analyses(db)
    fresh = _report().model_copy(update={"analysis_id": new_ulid()})
    cache.save_analysis(db, fresh, key="yeni", session_id=None, latency_ms=5)
    assert cache.get_analysis(db, fresh.analysis_id) == fresh
    assert cache.find_cached(db, "yeni") == fresh
    assert len(cache.list_analyses(db)) == 1


def test_clear_analyses_vacuums_and_removes_bytes(tmp_path: Path) -> None:
    """Faz F (O14): clear_analyses sonrası SQLite disk dosyasında silinen veri kalmaz."""
    db_file = tmp_path / "secure.db"
    db = Database(db_file)
    marker = "BENZERSIZ_ISARET_9f3a"
    report = _report().model_copy(update={"question_id": marker})
    cache.save_analysis(db, report, key="k", session_id=None, latency_ms=5)

    wal_file = tmp_path / "secure.db-wal"
    combined_before = db_file.read_bytes() + (wal_file.read_bytes() if wal_file.exists() else b"")
    assert marker.encode() in combined_before

    deleted = cache.clear_analyses(db)
    assert deleted == 1
    db.close()

    combined_after = db_file.read_bytes() + (wal_file.read_bytes() if wal_file.exists() else b"")
    assert marker.encode() not in combined_after


def test_database_pragmas_and_version(tmp_path: Path) -> None:
    """Faz F (D19): WAL, busy_timeout, user_version ve secure_delete pragmaları."""
    from sqlalchemy import text

    db_file = tmp_path / "pragmas.db"
    db = Database(db_file)
    with db.engine.connect() as conn:
        journal_mode = conn.execute(text("PRAGMA journal_mode")).scalar()
        user_version = conn.execute(text("PRAGMA user_version")).scalar()
        secure_delete = conn.execute(text("PRAGMA secure_delete")).scalar()
        busy_timeout = conn.execute(text("PRAGMA busy_timeout")).scalar()

    assert str(journal_mode).lower() == "wal"
    assert user_version == SCHEMA_DB_VERSION
    assert secure_delete == 1
    assert busy_timeout == 5000
    db.close()

    # Bellek veritabanında WAL atlanır, sürüm ve secure_delete geçerlidir
    mem_db = Database(MEMORY)
    with mem_db.engine.connect() as conn:
        mem_mode = conn.execute(text("PRAGMA journal_mode")).scalar()
        mem_ver = conn.execute(text("PRAGMA user_version")).scalar()
        mem_sec = conn.execute(text("PRAGMA secure_delete")).scalar()
    assert str(mem_mode).lower() == "memory"
    assert mem_ver == SCHEMA_DB_VERSION
    assert mem_sec == 1
    mem_db.close()


def test_prune_old_sessions_and_retention(tmp_path: Path) -> None:
    """Faz F (D19): session_retention_days ile eski oturumlar budanır."""

    db = Database(tmp_path / "sessions.db")
    now = utcnow()
    with db.session() as s:
        old_row = SessionRow(
            session_id="old_s",
            question_id="q1",
            attempt_count=1,
            current_hint_level=1,
            updated_at=now - timedelta(days=100),
        )
        recent_row = SessionRow(
            session_id="recent_s",
            question_id="q2",
            attempt_count=1,
            current_hint_level=1,
            updated_at=now - timedelta(days=10),
        )
        s.add(old_row)
        s.add(recent_row)
        s.commit()

    # 90 günden eskiler silinir: 1 satır silinmeli
    pruned = sessions.prune_old_sessions(db, days=90)
    assert pruned == 1

    with db.session() as s:
        assert s.get(SessionRow, ("old_s", "q1")) is None
        assert s.get(SessionRow, ("recent_s", "q2")) is not None
    db.close()

    # None retention_days olduğunda budama yapılmaz
    settings = load_settings(
        storage={"db_path": tmp_path / "sessions2.db", "session_retention_days": None}
    )
    db2 = Database.from_settings(settings)
    with db2.session() as s:
        s.add(
            SessionRow(
                session_id="old_s2",
                question_id="q1",
                attempt_count=1,
                current_hint_level=1,
                updated_at=now - timedelta(days=100),
            )
        )
        s.commit()
    # Tekrar from_settings ile açıldığında retention_days None olduğu için silinmez
    db3 = Database.from_settings(settings)
    with db3.session() as s:
        assert s.get(SessionRow, ("old_s2", "q1")) is not None
    db2.close()
    db3.close()


def test_list_analyses_page_pagination(db: Database) -> None:
    """Faz F (F6): list_analyses_page 60 kayıtta 50 + 10 olarak sayfalar."""
    now = datetime.now(UTC)
    with db.session() as s:
        for i in range(60):
            s.add(
                AnalysisRow(
                    id=f"a_{i:03d}",
                    created_at=now + timedelta(seconds=i),
                    cache_key=f"k_{i}",
                    language="c",
                    engine="none",
                    report_json="{}",
                )
            )
        s.commit()

    page1, cursor = cache.list_analyses_page(db, limit=50, before=None)
    assert len(page1) == 50
    assert cursor is not None
    assert cursor == page1[-1].id

    page2, cursor2 = cache.list_analyses_page(db, limit=50, before=cursor)
    assert len(page2) == 10
    assert cursor2 is None

    # Toplam 60 farklı kayıt çekildi
    all_ids = {r.id for r in page1} | {r.id for r in page2}
    assert len(all_ids) == 60


def test_list_analyses_page_search_and_escaping(db: Database) -> None:
    """Faz F (F6): Soru/dil/sağlayıcı araması büyük/küçük harf duyarsızdır.
    % ve _ karakterleri joker değildir.
    """
    now = datetime.now(UTC)
    with db.session() as s:
        s.add(
            AnalysisRow(
                id="1",
                created_at=now + timedelta(seconds=1),
                cache_key="k1",
                language="c",
                engine="none",
                question_id="c-medium-1",
                provider="ollama",
                report_json="{}",
            )
        )
        s.add(
            AnalysisRow(
                id="2",
                created_at=now + timedelta(seconds=2),
                cache_key="k2",
                language="cpp",
                engine="none",
                question_id="cpp-hard",
                provider="claude",
                report_json="{}",
            )
        )
        s.add(
            AnalysisRow(
                id="3",
                created_at=now + timedelta(seconds=3),
                cache_key="k3",
                language="c",
                engine="none",
                question_id="c_medium_underscore",
                provider="fake",
                report_json="{}",
            )
        )
        s.add(
            AnalysisRow(
                id="4",
                created_at=now + timedelta(seconds=4),
                cache_key="k4",
                language="python",
                engine="none",
                question_id="100%_complete",
                provider="openai",
                report_json="{}",
            )
        )
        s.commit()

    # "c-medium" araması büyük-küçük harf duyarsız tekil eşleşir
    rows, _ = cache.list_analyses_page(db, limit=10, search="C-Medium")
    assert [r.id for r in rows] == ["1"]

    # "_" karakteri joker olarak davranmaz: "c_medium" arandığında "c-medium-1" EŞLEŞMEZ
    rows, _ = cache.list_analyses_page(db, limit=10, search="c_medium")
    assert [r.id for r in rows] == ["3"]

    # "%" karakteri joker olarak davranmaz: "100%" arandığında yalnızca id="4" eşleşir
    rows, _ = cache.list_analyses_page(db, limit=10, search="100%")
    assert [r.id for r in rows] == ["4"]

    # Dil araması
    rows, _ = cache.list_analyses_page(db, limit=10, search="cpp")
    assert [r.id for r in rows] == ["2"]

    # Sağlayıcı araması
    rows, _ = cache.list_analyses_page(db, limit=10, search="ollama")
    assert [r.id for r in rows] == ["1"]
