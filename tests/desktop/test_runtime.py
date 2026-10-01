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
