"""Kaynak kökü ve göreli yol çözümü (ADR-0016)."""

from __future__ import annotations

import sys
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
