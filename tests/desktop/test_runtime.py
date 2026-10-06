"""Masaüstü çalışma ortamı: kaynak kökü, tercihler, saklanan kod."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from codementor.config import CONFIG_FILE_ENV
from codementor.desktop import runtime
from codementor.models.desktop import MAX_RECENT_FILES, DesktopPrefs
from codementor.models.enums import Engine, Language

REPO = Path(__file__).resolve().parents[2]


def test_resource_root_is_repo_when_not_frozen() -> None:
    assert not runtime.is_frozen()
    root = runtime.resource_root()
    assert root == REPO
    assert (root / "data" / "questions").is_dir()
    assert (root / "prompts").is_dir()


def test_frozen_root_and_user_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    bundle, install = tmp_path / "bundle", tmp_path / "install"
    bundle.mkdir()
    install.mkdir()
    (install / "codementor.toml").write_text("", encoding="utf-8")
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(bundle), raising=False)
    monkeypatch.setattr(sys, "executable", str(install / "CodeMentor.exe"))
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)
    monkeypatch.chdir(tmp_path)

    assert runtime.resource_root() == bundle
    assert runtime.prepare_environment() == bundle
    assert Path.cwd() == bundle
    assert os.environ[CONFIG_FILE_ENV] == str(install / "codementor.toml")


def test_prepare_environment_keeps_explicit_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv(CONFIG_FILE_ENV, "benim.toml")
    monkeypatch.chdir(tmp_path)
    runtime.prepare_environment()
    assert Path.cwd() == REPO
    assert os.environ[CONFIG_FILE_ENV] == "benim.toml"


def test_windowed_exe_streams_go_to_log(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(runtime, "user_dir", lambda: tmp_path)
    monkeypatch.setattr(sys, "stdout", None)
    monkeypatch.setattr(sys, "stderr", None)
    monkeypatch.chdir(tmp_path)
    runtime.prepare_environment()
    print("merhaba", file=sys.stderr)
    sys.stderr.close()
    assert "merhaba" in (tmp_path / runtime.LOG_FILE).read_text(encoding="utf-8")


def test_prefs_round_trip(tmp_path: Path) -> None:
    prefs = DesktopPrefs(provider="claude_cli", language=Language.CPP, engine=Engine.UNREAL)
    runtime.save_prefs(prefs, tmp_path)
    assert runtime.load_prefs(tmp_path) == prefs


def test_missing_or_corrupt_prefs_fall_back_to_defaults(tmp_path: Path) -> None:
    assert runtime.load_prefs(tmp_path) == DesktopPrefs()
    (tmp_path / runtime.PREFS_FILE).write_text("{bozuk", encoding="utf-8")
    assert runtime.load_prefs(tmp_path) == DesktopPrefs()
    (tmp_path / runtime.PREFS_FILE).write_text('{"bilinmeyen": 1}', encoding="utf-8")
    assert runtime.load_prefs(tmp_path) == DesktopPrefs()


def test_remember_file_moves_to_front_without_duplicates() -> None:
    prefs = DesktopPrefs()
    for i in range(MAX_RECENT_FILES + 3):
        prefs = runtime.remember_file(prefs, f"f{i}.c")
    prefs = runtime.remember_file(prefs, "f5.c")
    assert prefs.recent_files[0] == "f5.c"
    assert len(prefs.recent_files) == MAX_RECENT_FILES
    assert len(set(prefs.recent_files)) == MAX_RECENT_FILES


def test_source_round_trip_and_unsafe_ids(tmp_path: Path) -> None:
    runtime.save_source("01J9ABC", "int x;\n", tmp_path)
    assert runtime.load_source("01J9ABC", tmp_path) == "int x;\n"
    assert runtime.load_source("01J9XYZ", tmp_path) is None
    assert runtime.load_source("../desktop", tmp_path) is None


# --- Faz 49: saklama ---


def test_prune_sources_keeps_newest(tmp_path: Path) -> None:
    folder = tmp_path / runtime.SOURCES_DIR
    folder.mkdir()
    for i in range(5):
        path = folder / f"A{i}.txt"
        path.write_text(str(i), encoding="utf-8")
        os.utime(path, (1_000_000 + i, 1_000_000 + i))
    (folder / "not.md").write_text("x", encoding="utf-8")  # .txt dışı dosyaya dokunulmaz
    runtime.prune_sources(2, tmp_path)
    assert sorted(p.name for p in folder.iterdir()) == ["A3.txt", "A4.txt", "not.md"]
    runtime.prune_sources(None, tmp_path)  # sınırsız: bir şey silinmez
    runtime.prune_sources(2, tmp_path / "yok")  # klasör yoksa sessiz


def test_log_rotates_over_limit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(runtime, "user_dir", lambda: tmp_path)
    monkeypatch.setattr(runtime, "LOG_MAX_BYTES", 10)
    log = tmp_path / runtime.LOG_FILE
    log.write_text("eski günlük satırları", encoding="utf-8")
    (tmp_path / (runtime.LOG_FILE + ".1")).write_text("daha eski", encoding="utf-8")
    stream = runtime._log_stream()
    stream.write("yeni\n")
    stream.close()
    assert log.read_text(encoding="utf-8") == "yeni\n"
    assert (tmp_path / (runtime.LOG_FILE + ".1")).read_text(encoding="utf-8") == (
        "eski günlük satırları"
    )
    small = runtime._log_stream()  # sınır altında: eklemeye devam
    small.write("ek\n")
    small.close()
    assert log.read_text(encoding="utf-8") == "yeni\nek\n"


def test_save_prefs_atomic_keeps_old_on_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime.save_prefs(DesktopPrefs(recent_files=["a.c"]), tmp_path)

    def broken_replace(_src: object, _dst: object) -> None:
        raise OSError("disk dolu")

    monkeypatch.setattr(runtime.os, "replace", broken_replace)
    runtime.save_prefs(DesktopPrefs(recent_files=["b.c"]), tmp_path)  # sessizce geçer
    assert runtime.load_prefs(tmp_path).recent_files == ["a.c"]  # eski dosya bozulmadı
    assert [p.name for p in tmp_path.iterdir()] == [runtime.PREFS_FILE]  # geçici dosya kalmadı


def test_save_source_prunes_with_keep(tmp_path: Path) -> None:
    for i in range(3):
        runtime.save_source(f"A{i}", "kod", tmp_path, keep=2)
        path = tmp_path / runtime.SOURCES_DIR / f"A{i}.txt"
        os.utime(path, (1_000_000 + i, 1_000_000 + i))
    runtime.save_source("A3", "kod", tmp_path, keep=2)
    names = sorted(p.name for p in (tmp_path / runtime.SOURCES_DIR).iterdir())
    assert names == ["A2.txt", "A3.txt"]


def test_delete_source(tmp_path: Path) -> None:
    """Faz 62: delete_source dosyayı siler; olmayan ya da geçersiz id False döner."""
    runtime.save_source("01VALIDID", "print(1)", tmp_path)
    assert runtime.load_source("01VALIDID", tmp_path) == "print(1)"

    # Başarılı silme
    assert runtime.delete_source("01VALIDID", tmp_path) is True
    assert runtime.load_source("01VALIDID", tmp_path) is None

    # Zaten silinmiş
    assert runtime.delete_source("01VALIDID", tmp_path) is False

    # Path traversal koruması (. / \ vb.)
    assert runtime.delete_source("../outside", tmp_path) is False
    assert runtime.delete_source("foo/bar", tmp_path) is False
    assert runtime.delete_source("foo\\bar", tmp_path) is False
    assert runtime.delete_source("foo.txt", tmp_path) is False


def test_clear_sources(tmp_path: Path) -> None:
    """Faz 62: clear_sources tüm .txt kaynak dosyalarını siler ve sayısını döner."""
    runtime.save_source("A1", "kod1", tmp_path)
    runtime.save_source("A2", "kod2", tmp_path)
    sources_dir = tmp_path / runtime.SOURCES_DIR
    assert len(list(sources_dir.glob("*.txt"))) == 2

    count = runtime.clear_sources(tmp_path)
    assert count == 2
    assert len(list(sources_dir.glob("*.txt"))) == 0
    assert runtime.clear_sources(tmp_path) == 0
