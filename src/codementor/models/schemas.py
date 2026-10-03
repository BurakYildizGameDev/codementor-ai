"""JSON Schema üretimi (mimari §6.6)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from codementor.models.api import Problem
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMSinglePassOutput,
    LLMSocraticOutput,
    LLMVerifyOutput,
)
from codementor.models.pipeline import StageEvent
from codementor.models.provider import ProviderStatus
from codementor.models.questions import QuestionPublic
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest

JSON_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"

SCHEMA_MODELS: dict[str, type[BaseModel]] = {
    "report.schema.json": AnalysisReport,
    "llm_analysis.schema.json": LLMAnalysisOutput,
    "llm_socratic.schema.json": LLMSocraticOutput,
    "llm_single_pass.schema.json": LLMSinglePassOutput,
    "llm_verify.schema.json": LLMVerifyOutput,  # bulgu doğrulama geçişi (Faz 35)
    # Web UI tipleri bunlardan üretilir (web/scripts/gen-types.mjs)
    "request.schema.json": AnalysisRequest,
    "stage_event.schema.json": StageEvent,
    "question_public.schema.json": QuestionPublic,
    "problem.schema.json": Problem,
    "provider_status.schema.json": ProviderStatus,  # web sağlayıcı seçimi (Faz 26)
}


def build_schemas() -> dict[str, dict[str, Any]]:
    """Dosya adı → JSON Schema sözlüğü."""
    return {
        name: {"$schema": JSON_SCHEMA_DIALECT, "$id": name, **model.model_json_schema()}
        for name, model in SCHEMA_MODELS.items()
    }


def export_schemas(out_dir: Path) -> list[Path]:
    """Şemaları `out_dir` altına yazar; yazılan dosyaları döndürür."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name, schema in build_schemas().items():
        path = out_dir / name
        text = json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        path.write_text(text, encoding="utf-8", newline="\n")
        written.append(path)
    return written
