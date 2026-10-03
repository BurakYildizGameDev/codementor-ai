"""Faz 28: kaldırılmış model adları ağa çıkmadan yakalanır (`data/retired_models.yaml`).

DeepSeek `deepseek-chat` / `deepseek-reasoner` adlarını 24 Temmuz 2026'da kapattı; bu adlarla
istek 400 döner. Bağlantılar ekranı ve `providers check` bunu anahtar denetiminden önce söyler.
"""

from __future__ import annotations

import pytest

from codementor.config import ProvidersSettings
from codementor.providers.health import check_providers, load_retired_models

pytestmark = pytest.mark.anyio


def _providers(model: str) -> ProvidersSettings:
    providers = ProvidersSettings()
    providers.deepseek.model = model
    return providers


@pytest.mark.parametrize("model", ["deepseek-chat", "deepseek-reasoner"])
async def test_retired_deepseek_alias_not_ready(model: str) -> None:
    (status,) = await check_providers(["deepseek"], _providers(model))
    assert not status.ready
    assert "kaldırıldı" in status.detail
    assert "deepseek-flash" in status.detail


async def test_current_model_passes_to_key_check(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-ds-SECRET-0123456789")
    (status,) = await check_providers(["deepseek"], _providers("deepseek-flash"))
    assert status.ready


def test_retired_file_loads_and_is_keyed_by_provider() -> None:
    retired = load_retired_models()
    assert set(retired["deepseek"]) >= {"deepseek-chat", "deepseek-reasoner"}
    assert all(isinstance(v, str) and v for models in retired.values() for v in models.values())


def test_missing_retired_file_is_empty(tmp_path: object) -> None:
    from pathlib import Path

    assert load_retired_models(Path(str(tmp_path)) / "yok.yaml") == {}
