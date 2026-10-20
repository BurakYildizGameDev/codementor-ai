"""`test_storage.py` için ortak düzenek: sabitler, yardımcılar, fixture'lar."""

from __future__ import annotations

from datetime import timedelta

import pytest

from codementor.models.report import AnalysisReport
from codementor.pipeline.ids import new_ulid
from codementor.storage.db import (
    MEMORY,
    AnalysisRow,
    Database,
)
from tests.unit.test_report_render import _report

BASE = {
    "normalized_code": "int x;",
    "language": "c",
    "engine": "none",
    "question_id": "c-easy",
    "hint_level": 1,
    "provider": "ollama",
    "model": "m",
    "prompt_version": "v1+a",
    "rules_version": "r1+b",
    "schema_version": "1.0",
    "pipeline": "two_pass",  # Faz 35: mod + doğrulama geçişi
}


@pytest.fixture
def db() -> Database:
    return Database(MEMORY)


# --- Faz 49: saklama ve uyumsuz kayıt ---


def _numbered(index: int) -> AnalysisReport:
    report = _report()
    created = report.created_at + timedelta(seconds=index)
    return report.model_copy(update={"analysis_id": new_ulid(), "created_at": created})


def _store_raw(db: Database, analysis_id: str, key: str, report_json: str) -> None:
    with db.session() as session:
        session.add(
            AnalysisRow(
                id=analysis_id, cache_key=key, language="c", engine="none", report_json=report_json
            )
        )
        session.commit()
