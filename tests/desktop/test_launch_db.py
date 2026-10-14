"""Bozuk veritabanı açılış kurtarma testleri — Faz F (F1)."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import pytest

from codementor.desktop import launch, runtime


class DummyApp:
    def __init__(self, state: Any) -> None:
        self.state = state

    def mainloop(self) -> None:
        pass


def test_corrupted_db_recovery_yes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_file = tmp_path / "codementor.db"
    db_file.write_bytes(b"THIS_IS_NOT_A_VALID_SQLITE_DATABASE_BYTES")

    monkeypatch.setenv("CODEMENTOR_DB_PATH", str(db_file))
    asked: list[str] = []

    def fake_askyesno(title: str, msg: str) -> bool:
        asked.append(msg)
        return True

    monkeypatch.setattr(launch.messagebox, "askyesno", fake_askyesno)
    monkeypatch.setattr(launch.messagebox, "showerror", lambda *a, **k: None)
    monkeypatch.setattr(launch, "App", DummyApp)

    launch.main()

    assert len(asked) == 1
    assert "Veritabanı açılamadı" in asked[0]
    backups = list(tmp_path.glob("codementor.db.bozuk-*"))
    assert len(backups) == 1
    assert backups[0].read_bytes() == b"THIS_IS_NOT_A_VALID_SQLITE_DATABASE_BYTES"

    # Yeni veritabanı açılabilmeli
    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    conn.close()
    assert "analyses" in tables


def test_corrupted_db_recovery_no(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_file = tmp_path / "codementor.db"
    db_file.write_bytes(b"CORRUPT_BYTES_REJECTED")

    monkeypatch.setenv("CODEMENTOR_DB_PATH", str(db_file))

    def fake_askyesno(title: str, msg: str) -> bool:
        return False

    monkeypatch.setattr(launch.messagebox, "askyesno", fake_askyesno)

    with pytest.raises(SystemExit) as exc:
        launch.main()

    assert exc.value.code == 3
    assert db_file.read_bytes() == b"CORRUPT_BYTES_REJECTED"
    assert list(tmp_path.glob("codementor.db.bozuk-*")) == []


def test_backup_corrupted_db_with_wal_and_shm(tmp_path: Path) -> None:
    db = tmp_path / "test.db"
    wal = tmp_path / "test.db-wal"
    shm = tmp_path / "test.db-shm"
    db.write_text("main", encoding="utf-8")
    wal.write_text("wal", encoding="utf-8")
    shm.write_text("shm", encoding="utf-8")

    backed = runtime.backup_corrupted_db(db)
    assert backed.is_file()
    assert backed.read_text(encoding="utf-8") == "main"
    assert backed.with_name(backed.name + "-wal").read_text(encoding="utf-8") == "wal"
    assert backed.with_name(backed.name + "-shm").read_text(encoding="utf-8") == "shm"
    assert not db.exists()
    assert not wal.exists()
    assert not shm.exists()


def test_corrupted_db_recovery_rename_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db_file = tmp_path / "codementor.db"
    db_file.write_bytes(b"CORRUPT_BYTES")

    monkeypatch.setenv("CODEMENTOR_DB_PATH", str(db_file))
    monkeypatch.setattr(launch.messagebox, "askyesno", lambda *a, **k: True)

    errors: list[str] = []

    def fake_showerror(title: str, msg: str) -> None:
        errors.append(msg)

    monkeypatch.setattr(launch.messagebox, "showerror", fake_showerror)

    def failing_backup(_path: Any) -> Any:
        raise OSError("Dosya kilitli")

    monkeypatch.setattr(runtime, "backup_corrupted_db", failing_backup)

    with pytest.raises(SystemExit) as exc:
        launch.main()

    assert exc.value.code == 3
    assert len(errors) == 1
    assert "kilitli" in errors[0]
