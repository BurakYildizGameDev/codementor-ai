"""D8: bozuk few-shot ya da bozuk şablon karşısında prompt kurma davranışı.

Kural (bkz. `docs/DEVIR_FAZ_E_J.md` D8): bozuk few-shot YAML, Jinja hatası ve eksik dizin ham
istisna olarak sızmaz; tek `PromptTemplateError` türüne döner. Çağıranlar (orchestrator/passes)
bunu bozulmaya (degraded) çevirir, analiz 500 ile düşmez.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from codementor.prompts.builder import build_analysis_messages
from codementor.prompts.templates import PromptTemplateError, prompt_version, render
from tests.unit.prompt_helpers import (
    REPO_PROMPTS,
    analysis_input,
    prompt_settings,
)


def _copy_prompts(tmp_path: Path) -> Path:
    directory = tmp_path / "v1"
    shutil.copytree(REPO_PROMPTS, directory)
    return directory


def test_broken_fewshot_is_typed(tmp_path: Path) -> None:
    """Bozuk YAML `FewShotError` olarak sızmaz; `PromptTemplateError`'a çevrilir."""
    directory = _copy_prompts(tmp_path)
    (directory / "fewshots" / "bozuk.yaml").write_text("id: [bozuk\n", encoding="utf-8")
    with pytest.raises(PromptTemplateError, match="Few-shot"):
        build_analysis_messages(analysis_input(tmp_path), settings=prompt_settings(directory))


def test_intact_fewshots_still_build(tmp_path: Path) -> None:
    """Denetim: bozuk dosya yoksa prompt kurulur (few-shot'lar yerinde)."""
    directory = _copy_prompts(tmp_path)
    built = build_analysis_messages(analysis_input(tmp_path), settings=prompt_settings(directory))
    assert built.prompt_version.startswith("v1+")


def test_template_syntax_error_is_typed(tmp_path: Path) -> None:
    """Bozuk şablon Jinja hatası değil `PromptTemplateError` verir (çağıran bozulmaya düşer)."""
    directory = _copy_prompts(tmp_path)
    (directory / "analysis.user.j2").write_text("{% if %}", encoding="utf-8")
    with pytest.raises(PromptTemplateError, match=r"analysis\.user\.j2"):
        render(directory, "analysis.user.j2")
    with pytest.raises(PromptTemplateError):
        build_analysis_messages(analysis_input(tmp_path), settings=prompt_settings(directory))


def test_missing_template_dir_is_typed(tmp_path: Path) -> None:
    missing = tmp_path / "yok"
    with pytest.raises(PromptTemplateError, match="bulunamadı"):
        prompt_version(missing)
    with pytest.raises(PromptTemplateError, match="bulunamadı"):
        render(missing, "analysis.user.j2")
