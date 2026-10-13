"""Faz D: tek kaynaklı sürüm (O18) ve exe duman testi (`--self-check`, O17)."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType

import pytest

import codementor
from codementor.desktop import launch, self_check

REPO = Path(__file__).resolve().parents[2]


def _build_exe() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_exe", REPO / "build_exe.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_version_single_source() -> None:
    version = codementor.__version__
    assert importlib.metadata.version("codementor") == version
    assert _build_exe().project_version() == version
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r"^version\s*=", pyproject, re.MULTILINE) is None  # ikinci kaynak yok
    assert 'dynamic = ["version"]' in pyproject


def test_changelog_top_entry_is_current_version() -> None:
    text = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    top = re.search(r"^## \[([^\]]+)\]", text, re.MULTILINE)
    assert top is not None
    assert top.group(1) == codementor.__version__


def test_self_check_passes_from_source(tmp_path: Path) -> None:
    out = tmp_path / "sonuc.json"
    assert self_check.self_check(out) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["ok"] is True
    assert data["version"] == codementor.__version__
    names = {c["name"] for c in data["checks"]}
    assert {"soru bankası", "tree-sitter sorguları", "olgu çıkarımı (C)"} <= names


def test_self_check_fails_without_queries(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Exe'de `.scm` eksikse (Faz 50 hatası) duman testi düşer."""
    empty = tmp_path / "queries"
    empty.mkdir()
    monkeypatch.setattr(self_check.queries_package, "__file__", str(empty / "__init__.py"))
    out = tmp_path / "sonuc.json"
    assert self_check.self_check(out) == 1
    checks = {c["name"]: c for c in json.loads(out.read_text(encoding="utf-8"))["checks"]}
    assert checks["tree-sitter sorguları"]["ok"] is False


def test_optional_check_does_not_fail(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CODEMENTOR_VALIDATION__ROSLYN_CHECK_EXE", str(tmp_path / "yok.exe"))
    out = tmp_path / "sonuc.json"
    assert self_check.self_check(out) == 0
    checks = {c["name"]: c for c in json.loads(out.read_text(encoding="utf-8"))["checks"]}
    assert checks["Roslyn denetleyicisi"]["ok"] is False
    assert checks["Roslyn denetleyicisi"]["required"] is False


def test_launch_flag_runs_without_window(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(launch.runtime, "prepare_environment", lambda: tmp_path)
    monkeypatch.setattr(launch, "App", None)  # pencere açılmaya kalkarsa test düşer
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["CodeMentor.exe", "--self-check", "rapor/sonuc.json"])
    with pytest.raises(SystemExit) as exit_info:
        launch.main()
    assert exit_info.value.code == 0
    assert json.loads((tmp_path / "rapor" / "sonuc.json").read_text(encoding="utf-8"))["ok"]
