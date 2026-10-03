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
    "llm_verify.schema.json",
    # Web UI tipleri bunlardan üretilir (Faz 13, web/scripts/gen-types.mjs)
    "request.schema.json",
    "stage_event.schema.json",
    "question_public.schema.json",
    "problem.schema.json",
    "provider_status.schema.json",
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
    version = schema["properties"]["schema_version"]
    assert version["default"] == "1.1"  # Faz 36
    assert version["enum"] == ["1.0", "1.1"]  # eski raporlar okunur


def test_llm_schema_excludes_system_fields() -> None:
    schemas = build_schemas()
    for name in ("llm_analysis.schema.json", "llm_socratic.schema.json", "llm_verify.schema.json"):
        text = json.dumps(schemas[name])
        for field in ("compilation", "meta", '"source"', "confidence", "analysis_id"):
            assert field not in text, (name, field)


def test_ui_schemas_exported() -> None:
    schemas = build_schemas()
    titles = {
        "request.schema.json": "AnalysisRequest",
        "stage_event.schema.json": "StageEvent",
        "question_public.schema.json": "QuestionPublic",
        "problem.schema.json": "Problem",
    }
    for name, title in titles.items():
        assert schemas[name]["title"] == title
    # soru şeması referans çözümü ve mentorluk verisini taşımaz (§12)
    question = json.dumps(schemas["question_public.schema.json"])
    for field in ("reference_solution", "hint_ladder"):
        assert field not in question


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
