"""Faz 22B: precision için prompt kuralları ("sorun" ölçütü, kategori tanımları, bulgu sınırı)."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint
from codementor.prompts.builder import (
    build_analysis_messages,
    build_markup_analysis_messages,
    build_single_pass_messages,
)
from codementor.prompts.fewshot import load_fewshots, select_fewshots
from tests.unit.prompt_helpers import (
    REPO_PROMPTS,
    analysis_input,
    prompt_settings,
    system_text,
    user_text,
)

ISSUE_RULE_PHRASES = [
    'Hata (kind "issue") yalnızca gerçek sorundur',
    'kind "suggestion" ve severity "low"',  # Faz 36: öneri ayrı sınıf, yalnız low
    "soru gereksinimi ihlali öneri değil hatadır",
    '"input_handling" yalnızca',
    '"edge_case" yalnızca',
    '"design" yalnızca',
    "kuramsal uç değer",
    "kendi kategorisini",
    '"low" önemde en fazla 2 hata',
    "ilk sınıf ya da fonksiyon bildiriminin satırını",
]

HTML = """\
<!DOCTYPE html>
<html lang="tr">
<body><img src="a.png"></body>
</html>
"""


@pytest.mark.parametrize("builder", [build_analysis_messages, build_single_pass_messages])
def test_code_prompts_define_issue_criterion_and_categories(
    tmp_path: Path, builder: object
) -> None:
    built = builder(analysis_input(tmp_path), settings=prompt_settings())  # type: ignore[operator]
    system = system_text(built.messages)
    for phrase in ISSUE_RULE_PHRASES:
        assert phrase in system, phrase


@pytest.mark.parametrize("builder", [build_analysis_messages, build_single_pass_messages])
def test_code_task_asks_for_at_most_six_findings(tmp_path: Path, builder: object) -> None:
    built = builder(analysis_input(tmp_path), settings=prompt_settings())  # type: ignore[operator]
    assert "en fazla 6 hatayı ve varsa en fazla 2 öneriyi" in user_text(built.messages)


def test_markup_prompt_separates_issue_from_suggestion(tmp_path: Path) -> None:
    code = normalize(HTML, LanguageHint(language=Language.HTML, engine=Engine.NONE))
    inp = analysis_input(tmp_path, code=code, hint=None, function_hints=[])
    built = build_markup_analysis_messages(inp, settings=prompt_settings())
    system = system_text(built.messages)
    assert "Yalnızca gerçek sorunları raporla" in system
    assert 'kind "suggestion" ve severity "low"' in system
    assert '"design" yalnızca' in system
    assert '"low" önemde en fazla 2 hata' in system
    assert "en fazla 6 hatayı ve varsa en fazla 2 öneriyi" in user_text(built.messages)


def test_mentoring_rules_ignore_suggestions(tmp_path: Path) -> None:
    """Faz 36: tek geçişte de Sokratik sorular önerilerden üretilmez."""
    built = build_single_pass_messages(analysis_input(tmp_path), settings=prompt_settings())
    assert 'öneri (kind "suggestion") olarak işaretlenmiş bulgulardan soru üretme' in (
        system_text(built.messages)
    )


def test_python_fewshot_selected() -> None:
    examples = load_fewshots(REPO_PROMPTS / "fewshots")
    (chosen,) = select_fewshots(examples, Language.PYTHON, Engine.NONE, limit=1)
    assert chosen.language is Language.PYTHON


CATEGORY_BOUNDARY_PHRASES = [
    "sarkan işaretçi/referans",
    "geçersizleşmiş yineleyici",
    "Instantiate/Destroy",
    "olay aboneliği",
    "Motor API'sinin yanlış kullanımı",
    "bellek erişimi olmayan",
]


@pytest.mark.parametrize("builder", [build_analysis_messages, build_single_pass_messages])
def test_category_boundaries_in_code_prompts(tmp_path: Path, builder: object) -> None:
    """Faz 51: kategori sınırları (rehberle ortak metin) kod prompt'larında."""
    built = builder(analysis_input(tmp_path), settings=prompt_settings())  # type: ignore[operator]
    system = system_text(built.messages)
    for phrase in CATEGORY_BOUNDARY_PHRASES:
        assert phrase in system, phrase


def test_markup_prompt_has_no_code_category_rules(tmp_path: Path) -> None:
    code = normalize(HTML, LanguageHint(language=Language.HTML, engine=Engine.NONE))
    inp = analysis_input(tmp_path, code=code, hint=None, function_hints=[])
    system = system_text(build_markup_analysis_messages(inp, settings=prompt_settings()).messages)
    assert "geçersizleşmiş yineleyici" not in system
