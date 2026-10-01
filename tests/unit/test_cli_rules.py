"""`codementor rules list|doc` testleri (mimari §10) ve katalog güncelliği."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner, Result

from codementor.cli.main import app
from codementor.models.enums import Engine, Language
from codementor.rules.catalog import render_catalog, rule_catalog

CATALOG = Path(__file__).resolve().parents[2] / "docs" / "rules-catalog.md"


def _invoke(*args: str) -> Result:
    return CliRunner().invoke(app, ["rules", *args], env={"COLUMNS": "200"})


def test_rules_list_engine_unity() -> None:
    result = _invoke("list", "--engine", "unity")
    assert result.exit_code == 0, result.output
    for rule_id in ("UNITY-GC-001", "UNITY-PERF-001", "UNITY-EVT-001", "CS-PERF-001"):
        assert rule_id in result.output
    assert "UE-GC-001" not in result.output
    assert "C-BUF-001" not in result.output


def test_rules_list_language_filter() -> None:
    result = _invoke("list", "--language", "c")
    assert result.exit_code == 0, result.output
    assert "C-BUF-001" in result.output
    assert "CPP-OWN-001" not in result.output


def test_rules_list_all() -> None:
    result = _invoke("list")
    assert result.exit_code == 0, result.output
    assert "Kurallar (34)" in result.output  # 20 C ailesi (Faz 6 + 17) + 14 Python/HTML/CSS


def test_rules_list_engine_none_is_engine_agnostic() -> None:
    ids = {r.id for r in rule_catalog(engine=Engine.NONE)}
    assert ids == {
        *(f"C-{k}" for k in ("BUF-001", "IO-001", "UB-001", "MEM-001", "MEM-002", "MEM-003")),
        "C-PERF-001",
        *(f"CPP-{k}" for k in ("OWN-001", "SP-001", "PERF-001")),
        *(f"CS-{k}" for k in ("ALLOC-001", "ALLOC-002", "PERF-001")),
        *(f"PY-{k}" for k in ("DESIGN-001", "DESIGN-002", "EDGE-001", "PERF-001", "RES-001")),
        *(f"HTML-{k}" for k in ("ACC-001", "ACC-002", "ACC-003", "STD-001", "STD-002", "STD-003")),
        *(f"CSS-{k}" for k in ("MAINT-001", "MAINT-002", "STD-001")),
    }
    assert {r.id for r in rule_catalog(Language.CPP, Engine.UNREAL)} == {
        "CPP-OWN-001",
        "CPP-SP-001",
        "CPP-PERF-001",
        "UE-GC-001",
        "UE-MEM-001",
        "UE-PERF-001",
    }


def test_rules_list_invalid_engine() -> None:
    assert _invoke("list", "--engine", "godot").exit_code == 2


def test_rules_doc_writes_catalog(tmp_path: Path) -> None:
    out = tmp_path / "docs" / "catalog.md"
    result = _invoke("doc", "--out", str(out))
    assert result.exit_code == 0, result.output
    assert out.read_text(encoding="utf-8") == render_catalog()


def test_committed_catalog_up_to_date() -> None:
    assert CATALOG.read_text(encoding="utf-8") == render_catalog(), (
        "docs/rules-catalog.md güncel değil: make rules-doc"
    )
