"""Depolama (mimari §11): önbellek anahtarı, önbellek, oturumlar, veritabanı yolu, ULID."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from codementor.config import load_settings
from codementor.pipeline.ids import new_ulid
from codementor.storage import cache, sessions
from codementor.storage.db import MEMORY, Database, resolve_db_path
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
