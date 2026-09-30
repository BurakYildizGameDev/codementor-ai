"""`codementor schema export` komutu testleri (mimari §6.6)."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from codementor.cli.main import app
from codementor.models.schemas import SCHEMA_MODELS, build_schemas

EXPECTED = {
    "report.schema.json",
    "llm_analysis.schema.json",
    "llm_socratic.schema.json",
    "llm_single_pass.schema.json",
}
REPO_SCHEMAS = Path(__file__).resolve().parents[2] / "schemas"


def test_schema_export_writes_all_files(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "schemas"
    result = CliRunner().invoke(app, ["schema", "export", "--out", str(out)])
    assert result.exit_code == 0, result.output
    assert {p.name for p in out.iterdir()} == EXPECTED
    for name in EXPECTED:
        assert name in result.output


def test_exported_schemas_are_valid_json(tmp_path: Path) -> None:
    CliRunner().invoke(app, ["schema", "export", "--out", str(tmp_path)])
    for name in EXPECTED:
        schema = json.loads((tmp_path / name).read_text(encoding="utf-8"))
        assert schema["type"] == "object"
        assert "$schema" in schema
        assert schema["$id"] == name


def test_report_schema_title_and_version(tmp_path: Path) -> None:
    CliRunner().invoke(app, ["schema", "export", "--out", str(tmp_path)])
    schema = json.loads((tmp_path / "report.schema.json").read_text(encoding="utf-8"))
    assert schema["title"] == "AnalysisReport"
    assert schema["properties"]["schema_version"]["const"] == "1.0"


def test_llm_schema_excludes_system_fields() -> None:
    schemas = build_schemas()
    for name in ("llm_analysis.schema.json", "llm_socratic.schema.json"):
        text = json.dumps(schemas[name])
        for field in ("compilation", "meta", '"source"', "confidence", "analysis_id"):
            assert field not in text, (name, field)


def test_schema_models_mapping() -> None:
    assert set(SCHEMA_MODELS) == EXPECTED


def test_export_is_deterministic(tmp_path: Path) -> None:
    a, b = tmp_path / "a", tmp_path / "b"
    runner = CliRunner()
    runner.invoke(app, ["schema", "export", "--out", str(a)])
    runner.invoke(app, ["schema", "export", "--out", str(b)])
    for name in EXPECTED:
        assert (a / name).read_bytes() == (b / name).read_bytes()


def test_committed_schemas_up_to_date() -> None:
    """Depodaki `schemas/` dosyaları modellerle senkron olmalı (`make schema`)."""
    schemas = build_schemas()
    for name, schema in schemas.items():
        committed = REPO_SCHEMAS / name
        assert committed.exists(), f"{name} eksik; `make schema` çalıştırın"
        assert json.loads(committed.read_text(encoding="utf-8")) == schema, (
            f"{name} güncel değil; `make schema` çalıştırın"
        )
