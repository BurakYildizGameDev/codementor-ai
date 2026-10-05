"""SARIF dışa aktarımı her dilde (Faz 50): Python/HTML/CSS raporları 500 vermez."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from jsonschema import Draft4Validator

from codementor.api.app import create_app
from codementor.config import Settings
from codementor.languages import CANONICAL_SUFFIX
from codementor.models.enums import Engine, Language
from codementor.pipeline.ids import new_ulid
from codementor.storage import cache
from codementor.storage.db import Database
from tests.unit.test_report_render import _report

pytestmark = pytest.mark.anyio
SCHEMA = json.loads(
    (Path(__file__).resolve().parents[1] / "fixtures" / "sarif-schema-2.1.0.json").read_text(
        encoding="utf-8"
    )
)


@pytest.mark.parametrize("language", list(Language))
async def test_sarif_200_for_every_language(
    settings: Settings, db: Database, language: Language
) -> None:
    """Kabul: altı dilde `/v1/analyses/{id}/sarif` 200 ve şemaya uygun."""
    report = _report().model_copy(
        update={"analysis_id": new_ulid(), "language": language, "engine": Engine.NONE}
    )
    cache.save_analysis(db, report, key=f"k-{language}", session_id=None, latency_ms=1)
    transport = httpx.ASGITransport(app=create_app(settings, db=db))
    async with httpx.AsyncClient(transport=transport, base_url="http://127.0.0.1") as client:
        response = await client.get(f"/v1/analyses/{report.analysis_id}/sarif")
    assert response.status_code == 200
    log = response.json()
    Draft4Validator(SCHEMA).validate(log)
    uri = log["runs"][0]["artifacts"][0]["location"]["uri"]
    assert uri == f"{report.analysis_id}{CANONICAL_SUFFIX[language]}"
