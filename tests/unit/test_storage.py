"""Depolama (mimari §11): önbellek anahtarı, önbellek, oturumlar, veritabanı yolu, ULID."""

from __future__ import annotations

import re
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from codementor.config import load_settings
from codementor.models.report import AnalysisReport
from codementor.pipeline.ids import new_ulid
from codementor.storage import cache, sessions
from codementor.storage.db import (
    MEMORY,
    SCHEMA_DB_VERSION,
    AnalysisRow,
    Database,
    SessionRow,
    resolve_db_path,
    utcnow,
)
from tests.unit.test_report_render import _report

BASE = {
    "normalized_code": "int x;",
    "language": "c",
    "engine": "none",
    "question_id": "c-easy",
    "hint_level": 1,
    "provider": "ollama",
    "model": "m",
    "prompt_version": "v1+a",
    "rules_version": "r1+b",
    "schema_version": "1.0",
    "pipeline": "two_pass",  # Faz 35: mod + doğrulama geçişi
}


def test_cache_key_is_deterministic_hex() -> None:
    assert cache.cache_key(**BASE) == cache.cache_key(**BASE)  # type: ignore[arg-type]
    assert re.fullmatch(r"[0-9a-f]{64}", cache.cache_key(**BASE))  # type: ignore[arg-type]


@pytest.mark.parametrize("field", sorted(BASE))
def test_every_field_changes_the_key(field: str) -> None:
    changed = dict(BASE)
    changed[field] = 2 if field == "hint_level" else f"{BASE[field]}x"
    assert cache.cache_key(**changed) != cache.cache_key(**BASE)  # type: ignore[arg-type]


def test_field_boundaries_do_not_collide() -> None:
    a = dict(BASE, normalized_code="ab", language="c")
    b = dict(BASE, normalized_code="a", language="bc")
    assert cache.cache_key(**a) != cache.cache_key(**b)  # type: ignore[arg-type]


def test_none_question_distinct_from_empty_provider() -> None:
    assert cache.cache_key(**dict(BASE, question_id=None)) == cache.cache_key(  # type: ignore[arg-type]
        **dict(BASE, question_id="")
    )


@pytest.fixture
def db() -> Database:
    return Database(MEMORY)


def test_cache_roundtrip_skips_degraded(db: Database) -> None:
    report = _report()
    assert cache.find_cached(db, "k") is None
    cache.save_analysis(db, report, key="k", session_id=None, latency_ms=5)
    found = cache.find_cached(db, "k")
    assert found == report
    degraded = report.model_copy(
        update={
            "analysis_id": new_ulid(),
            "meta": report.meta.model_copy(update={"degraded": True}),
        }
    )
    cache.save_analysis(db, degraded, key="d", session_id=None, latency_ms=5)
    assert cache.find_cached(db, "d") is None


def test_sessions_count_per_session_and_question(db: Database) -> None:
    assert sessions.next_attempt(db, None, "q") == 1
    assert sessions.next_attempt(db, "s", "q") == 1
    sessions.record_attempt(db, "s", "q", attempt=1, hint_level=1)
    sessions.record_attempt(db, "s", "q", attempt=2, hint_level=2)
    assert sessions.next_attempt(db, "s", "q") == 3
    assert sessions.next_attempt(db, "s", "baska") == 1
    assert sessions.next_attempt(db, "baska", "q") == 1
    sessions.record_attempt(db, "s", None, attempt=1, hint_level=1)  # serbest mod
    assert sessions.next_attempt(db, "s", None) == 2
    sessions.record_attempt(db, None, "q", attempt=5, hint_level=3)  # oturumsuz: yok sayılır


def test_db_path_resolution(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEMENTOR_CONFIG_FILE", str(tmp_path / "yok.toml"))
    monkeypatch.delenv("CODEMENTOR_DB_PATH", raising=False)
    assert resolve_db_path(load_settings()) == Path.home() / ".codementor" / "codementor.db"
    monkeypatch.setenv("CODEMENTOR_DB_PATH", str(tmp_path / "env.db"))
    assert resolve_db_path(load_settings()) == tmp_path / "env.db"
    configured = load_settings(storage={"db_path": tmp_path / "cfg.db"})
    assert resolve_db_path(configured) == tmp_path / "cfg.db"


def test_database_creates_parent_dir(tmp_path: Path) -> None:
    path = tmp_path / "a" / "b" / "cm.db"
    Database(path).close()
    assert path.exists()


def test_ulid_format_and_order() -> None:
    first, second = new_ulid(1_000), new_ulid(2_000)
    assert re.fullmatch(r"[0-9A-HJKMNP-TV-Z]{26}", first)
    assert first < second
    assert new_ulid() != new_ulid()


# --- Faz 49: atomik deneme ayırma ---


def test_reserve_attempt_increments_atomically(tmp_path: Path) -> None:
    """İş parçacıklarından eşzamanlı ayırma: her gönderim farklı deneme alır, istisna yok."""
    database = Database(tmp_path / "yaris.db")
    with ThreadPoolExecutor(max_workers=10) as pool:
        attempts = list(
            pool.map(lambda _i: sessions.reserve_attempt(database, "s", "q"), range(10))
        )
    database.close()
    assert sorted(attempts) == list(range(1, 11))


def test_reserve_attempt_without_session_is_always_first(db: Database) -> None:
    assert sessions.reserve_attempt(db, None, "q") == 1
    assert sessions.reserve_attempt(db, None, "q") == 1
    assert sessions.reserve_attempt(db, "s", None) == 1  # serbest mod da sayılır
    assert sessions.reserve_attempt(db, "s", None) == 2


def test_release_attempt_only_latest(db: Database) -> None:
    first = sessions.reserve_attempt(db, "s", "q")
    sessions.release_attempt(db, "s", "q", first)
    assert sessions.next_attempt(db, "s", "q") == 1  # geri alındı
    one = sessions.reserve_attempt(db, "s", "q")
    two = sessions.reserve_attempt(db, "s", "q")
    sessions.release_attempt(db, "s", "q", one)  # arada yeni ayırma oldu: geri alınmaz
    assert (one, two) == (1, 2)
    assert sessions.next_attempt(db, "s", "q") == 3
    sessions.release_attempt(db, None, "q", 1)  # oturumsuz: bir şey yapmaz


def test_record_attempt_updates_hint_only(db: Database) -> None:
    attempt = sessions.reserve_attempt(db, "s", "q")
    sessions.record_attempt(db, "s", "q", attempt=attempt, hint_level=2)
    assert sessions.next_attempt(db, "s", "q") == 2  # kayıt sayacı artırmaz
    with db.session() as session:
        row = session.get(SessionRow, ("s", "q"))
    assert row is not None
    assert row.current_hint_level == 2


# --- Faz 49: saklama ve uyumsuz kayıt ---


def _numbered(index: int) -> AnalysisReport:
    report = _report()
    created = report.created_at + timedelta(seconds=index)
    return report.model_copy(update={"analysis_id": new_ulid(), "created_at": created})


def test_save_analysis_prunes_oldest(db: Database) -> None:
    reports = [_numbered(i) for i in range(5)]
    for report in reports:
        cache.save_analysis(db, report, key="k", session_id=None, latency_ms=1, max_analyses=3)
    kept = [row.id for row in cache.list_analyses(db)]
    assert kept == [r.analysis_id for r in reversed(reports[2:])]


def test_max_analyses_none_keeps_all(db: Database) -> None:
    for i in range(4):
        cache.save_analysis(db, _numbered(i), key="k", session_id=None, latency_ms=1)
    assert len(cache.list_analyses(db)) == 4


def _store_raw(db: Database, analysis_id: str, key: str, report_json: str) -> None:
    with db.session() as session:
        session.add(
            AnalysisRow(
                id=analysis_id, cache_key=key, language="c", engine="none", report_json=report_json
            )
        )
        session.commit()


def test_incompatible_report_json_is_none_and_logged(
    db: Database, captured_logs: Callable[[], list[dict[str, Any]]]
) -> None:
    old_id = new_ulid()
    _store_raw(db, old_id, "eski", '{"schema_version": "0.1", "eski_alan": 1}')
    assert cache.get_analysis(db, old_id) is None
    assert [row.id for row in cache.list_analyses(db)] == [old_id]  # geçmiş listesi çökmez
    events = [e for e in captured_logs() if e["event"] == "stored_report_incompatible"]
    assert [e["analysis_id"] for e in events] == [old_id]


def test_get_row_returns_raw_record_even_when_incompatible(db: Database) -> None:
    """Faz 60: get_row, rapor JSON'ı uyumsuz olsa bile satırı döndürür."""
    old_id = new_ulid()
    _store_raw(db, old_id, "eski_key", '{"schema_version": "0.1"}')
    row = cache.get_row(db, old_id)
    assert row is not None
    assert row.id == old_id
    assert row.cache_key == "eski_key"
    assert cache.get_row(db, "olmayan_id") is None


def test_find_cached_skips_incompatible(db: Database) -> None:
    _store_raw(db, new_ulid(), "k", "{bozuk json")
    assert cache.find_cached(db, "k") is None


def test_old_sqlite_rejected_with_turkish_message(monkeypatch: pytest.MonkeyPatch) -> None:
    import sqlite3

    monkeypatch.setattr(sqlite3, "sqlite_version_info", (3, 31, 1))
    with pytest.raises(RuntimeError, match="çok eski"):
        Database(MEMORY)


def test_prune_stable_on_equal_created_at(db: Database) -> None:
    """Denetim Ü1: aynı `created_at`'te sıra kimlikle kararlı (en büyük ULID'ler kalır)."""
    base = _report()
    reports = [base.model_copy(update={"analysis_id": new_ulid()}) for _ in range(4)]
    for report in reports:
        cache.save_analysis(db, report, key="k", session_id=None, latency_ms=1, max_analyses=2)
    kept = sorted(row.id for row in cache.list_analyses(db))
    assert kept == sorted(r.analysis_id for r in reports)[-2:]


def test_hint_level_never_moves_back(db: Database) -> None:
    """Denetim Ü5: deneme 2 önce, deneme 1 sonra biterse seviye geri çekilmez."""
    one = sessions.reserve_attempt(db, "s", "q")
    two = sessions.reserve_attempt(db, "s", "q")
    sessions.record_attempt(db, "s", "q", attempt=two, hint_level=2)
    sessions.record_attempt(db, "s", "q", attempt=one, hint_level=1)
    with db.session() as session:
        row = session.get(SessionRow, ("s", "q"))
    assert row is not None
    assert row.current_hint_level == 2


def test_delete_analysis_success_and_missing(db: Database) -> None:
    """Faz 62: delete_analysis kaydı siler; bulunamazsa False döner."""
    report = _report()
    cache.save_analysis(db, report, key="k1", session_id="s1", latency_ms=10)
    assert cache.get_analysis(db, report.analysis_id) is not None

    # Silme başarılı
    assert cache.delete_analysis(db, report.analysis_id) is True
    assert cache.get_analysis(db, report.analysis_id) is None
    assert cache.get_row(db, report.analysis_id) is None

    # Olmayan id
    assert cache.delete_analysis(db, report.analysis_id) is False
    assert cache.delete_analysis(db, "olmayan_id") is False


def test_clear_analyses_removes_all_records(db: Database) -> None:
    """Faz 62: clear_analyses tüm analizleri siler ve silinen sayıyı döner."""
    base = _report()
    r1 = base.model_copy(update={"analysis_id": new_ulid()})
    r2 = base.model_copy(update={"analysis_id": new_ulid()})
    cache.save_analysis(db, r1, key="k1", session_id="s1", latency_ms=5)
    cache.save_analysis(db, r2, key="k2", session_id="s2", latency_ms=5)
    assert len(cache.list_analyses(db)) == 2

    count = cache.clear_analyses(db)
    assert count == 2
    assert cache.list_analyses(db) == []
    assert cache.clear_analyses(db) == 0


def test_clear_sessions_removes_all_sessions(db: Database) -> None:
    """Faz 62: clear_sessions tüm oturumları siler ve silinen sayıyı döner."""
    from sqlmodel import select

    sessions.reserve_attempt(db, "s1", "q1")
    sessions.reserve_attempt(db, "s2", "q2")
    with db.session() as session:
        rows = session.exec(select(SessionRow)).all()
        assert len(rows) == 2

    deleted = sessions.clear_sessions(db)
    assert deleted == 2
    with db.session() as session:
        rows = session.exec(select(SessionRow)).all()
        assert len(rows) == 0
    assert sessions.clear_sessions(db) == 0


def test_deleted_analysis_not_served_from_cache(db: Database) -> None:
    """Denetim O4: silinen analiz aynı önbellek anahtarıyla geri dönmez."""
    report = _report()
    cache.save_analysis(db, report, key="k", session_id=None, latency_ms=5)
    assert cache.find_cached(db, "k") is not None
    assert cache.delete_analysis(db, report.analysis_id) is True
    assert cache.find_cached(db, "k") is None


def test_single_delete_keeps_sessions(db: Database) -> None:
    """Denetim O4: tek analiz silmek ipucu merdivenine (sessions) dokunmaz."""
    sessions.reserve_attempt(db, "s1", "q1")
    report = _report()
    cache.save_analysis(db, report, key="k", session_id="s1", latency_ms=5)
    cache.delete_analysis(db, report.analysis_id)
    with db.session() as session:
        row = session.get(SessionRow, ("s1", "q1"))
    assert row is not None
    assert row.attempt_count == 1


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
    from codementor.config import load_settings

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
