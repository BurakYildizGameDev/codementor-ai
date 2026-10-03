"""Faz 28: kaldırılmış model adları ağa çıkmadan yakalanır (`data/retired_models.yaml`).

Sağlayıcı bir model adını kapattığında bu adla istek 400 döner. Bağlantılar ekranı ve
`providers check` bunu anahtar denetiminden önce söyler. DeepSeek girdileri sağlayıcıyla
birlikte kaldırıldı (ADR-0021); mekanizma geçici dosyayla sınanır.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.config import ProvidersSettings
from codementor.providers import health
from codementor.providers.health import check_providers, load_retired_models

pytestmark = pytest.mark.anyio

RETIRED = 'gemini:\n  gemini-eski: "gemini-eski kaldırıldı; gemini-3.8-flash kullan"\n'


@pytest.fixture
def retired_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "retired_models.yaml"
    path.write_text(RETIRED, encoding="utf-8")
    monkeypatch.setattr(health, "RETIRED_MODELS_FILE", path)
    return path


def _providers(model: str) -> ProvidersSettings:
    providers = ProvidersSettings()
    providers.gemini.model = model
    return providers


@pytest.mark.usefixtures("retired_file")
async def test_retired_model_not_ready() -> None:
    (status,) = await check_providers(["gemini"], _providers("gemini-eski"))
    assert not status.ready
    assert "kaldırıldı" in status.detail
    assert "gemini-3.8-flash" in status.detail


@pytest.mark.usefixtures("retired_file")
async def test_current_model_passes_to_key_check(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "gm-test-SECRET-0123456789")
    (status,) = await check_providers(["gemini"], _providers("gemini-3.8-flash"))
    assert status.ready
    assert "deneysel" in status.detail  # ADR-0021: Gemini canlı doğrulanmadı


def test_retired_file_loads_and_is_keyed_by_provider(retired_file: Path) -> None:
    retired = load_retired_models(retired_file)
    assert retired == {"gemini": {"gemini-eski": "gemini-eski kaldırıldı; gemini-3.8-flash kullan"}}


def test_repo_retired_file_is_valid() -> None:
    """Paketteki dosya boş eşleme olabilir ama okunabilir olmalı."""
    retired = load_retired_models()
    assert all(isinstance(v, str) and v for models in retired.values() for v in models.values())


def test_missing_retired_file_is_empty(tmp_path: Path) -> None:
    assert load_retired_models(tmp_path / "yok.yaml") == {}
