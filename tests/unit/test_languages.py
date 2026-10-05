"""Dil ↔ uzantı eşlemesi tek yerde (Faz 50): API, CLI, masaüstü, eval aynı tabloyu kullanır."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.desktop.services import render_export
from codementor.desktop.viewmodel import language_for_path
from codementor.eval.dataset import code_suffix
from codementor.languages import CANONICAL_SUFFIX, SUFFIXES, language_for_suffix
from codementor.models.enums import Language
from tests.unit.test_report_render import _report


def test_every_language_has_canonical_suffix() -> None:
    assert set(CANONICAL_SUFFIX) == set(Language)
    for language, suffix in CANONICAL_SUFFIX.items():
        assert SUFFIXES[suffix] is language  # kanonik uzantı tanınan uzantılar arasında


@pytest.mark.parametrize(("suffix", "language"), list(SUFFIXES.items()))
def test_desktop_uses_shared_table(suffix: str, language: Language) -> None:
    assert language_for_path(Path(f"a{suffix.upper()}")) is language
    assert language_for_suffix(suffix) is language


def test_unknown_suffix_is_none() -> None:
    assert language_for_suffix(".txt") is None
    assert language_for_path("README") is None


@pytest.mark.parametrize("language", list(Language))
def test_eval_dataset_suffix_from_shared_table(language: Language) -> None:
    assert code_suffix(language.value) == CANONICAL_SUFFIX[language]


@pytest.mark.parametrize("language", list(Language))
def test_desktop_sarif_export_has_language_suffix(language: Language) -> None:
    import json

    report = _report().model_copy(update={"language": language})
    log = json.loads(render_export(report, "sarif"))
    uri = log["runs"][0]["artifacts"][0]["location"]["uri"]
    assert uri.endswith(CANONICAL_SUFFIX[language])
