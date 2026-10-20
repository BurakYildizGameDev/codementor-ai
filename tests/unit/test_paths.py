"""Kaynak kökü ve göreli yol çözümü (ADR-0016)."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

import pytest

from codementor import paths

REPO = Path(__file__).resolve().parents[2]


def test_resource_root_repo() -> None:
    assert paths.resource_root() == REPO
    assert (paths.resource_root() / "data" / "questions").is_dir()


def test_resource_root_packaged_resources(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    bundled = tmp_path / "_resources"
    (bundled / "data").mkdir(parents=True)
    monkeypatch.setattr(paths, "_package_resources", lambda: bundled)
    assert paths.resource_root() == bundled


def test_resource_root_frozen(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)
    assert paths.resource_root() == tmp_path


def test_resource_path_is_absolute() -> None:
    path = paths.resource_path("data/questions")
    assert path.is_absolute()
    assert path == REPO / "data" / "questions"


def test_resolve_relative_keeps_absolute(tmp_path: Path) -> None:
    absolute = tmp_path / "x.yaml"
    assert paths.resolve_relative(absolute, Path("/baska")) == absolute
    assert paths.resolve_relative(Path("a/b.yaml"), tmp_path) == tmp_path / "a" / "b.yaml"


def test_resolve_config_relative_prefers_toml_dir(tmp_path: Path) -> None:
    (tmp_path / "data" / "questions").mkdir(parents=True)
    resolved = paths.resolve_config_relative(Path("data/questions"), tmp_path)
    assert resolved == tmp_path / "data" / "questions"


def test_resolve_config_relative_falls_back_to_resource_root(tmp_path: Path) -> None:
    """Exe'nin yanına kopyalanan varsayılan toml paket verisini göstermeye devam eder (ADR-0027)."""
    resolved = paths.resolve_config_relative(Path("data/questions"), tmp_path)
    assert resolved == REPO / "data" / "questions"


def test_resolve_config_relative_missing_everywhere_stays_toml_dir(tmp_path: Path) -> None:
    resolved = paths.resolve_config_relative(Path("yeni/codementor.db"), tmp_path)
    assert resolved == tmp_path / "yeni" / "codementor.db"


def test_resolve_config_relative_keeps_absolute(tmp_path: Path) -> None:
    absolute = tmp_path / "yok.yaml"
    assert paths.resolve_config_relative(absolute, Path("/baska")) == absolute


# --- replace_file: Windows'taki geçici dosya kilidi ---------------------------------------------


def _pair(tmp_path: Path) -> tuple[Path, Path]:
    source, target = tmp_path / "yeni.tmp", tmp_path / "hedef.json"
    source.write_text("yeni", encoding="utf-8")
    target.write_text("eski", encoding="utf-8")
    return source, target


def test_replace_file_retries_transient_lock(
    tmp_path: Path, locked_replace: Callable[[int], list[int]]
) -> None:
    source, target = _pair(tmp_path)
    left = locked_replace(2)
    paths.replace_file(source, target)
    assert left == [0]
    assert target.read_text(encoding="utf-8") == "yeni"
    assert not source.exists()


def test_replace_file_persistent_lock_raises(
    tmp_path: Path, locked_replace: Callable[[int], list[int]]
) -> None:
    source, target = _pair(tmp_path)
    locked_replace(100)
    with pytest.raises(PermissionError):
        paths.replace_file(source, target)
    assert target.read_text(encoding="utf-8") == "eski"


def test_replace_file_no_retry_off_windows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, locked_replace: Callable[[int], list[int]]
) -> None:
    source, target = _pair(tmp_path)
    left = locked_replace(1)
    monkeypatch.setattr(paths, "_RETRY_REPLACE", False)
    with pytest.raises(PermissionError):
        paths.replace_file(source, target)
    assert left == [0]


def test_replace_file_other_errors_not_retried(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[int] = []

    def broken(_source: object, _target: object) -> None:
        calls.append(1)
        raise OSError("disk dolu")

    monkeypatch.setattr(paths, "_RETRY_REPLACE", True)
    monkeypatch.setattr(paths.os, "replace", broken)
    with pytest.raises(OSError, match="disk dolu"):
        paths.replace_file(*_pair(tmp_path))
    assert calls == [1]
