"""Depodaki gerçek soru bankası ve kontrol listesi içeriğinin bütünlük testleri."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from codementor.models.bigo import parse_bigo
from codementor.models.enums import Difficulty, Engine, Language, has_complexity
from codementor.questions.bank import QuestionBank
from codementor.questions.checklists import CORE_TAG, Checklists
from tests.unit.question_tables import MATRIX, METHOD_LEAKS

DATA = Path(__file__).resolve().parents[2] / "data"


@pytest.fixture(scope="module")
def bank() -> QuestionBank:
    return QuestionBank.load(DATA / "questions")


@pytest.fixture(scope="module")
def checklists() -> Checklists:
    return Checklists.load(DATA / "checklists")


MIN_PER_GROUP = 8  # Faz 30: dil/motor başına asgari soru


def _groups(bank: QuestionBank) -> dict[tuple[Language, Engine], list[Difficulty]]:
    groups: dict[tuple[Language, Engine], list[Difficulty]] = {}
    for q in bank:
        groups.setdefault((q.language, q.engine), []).append(q.difficulty)
    return groups


def test_bank_size(bank: QuestionBank) -> None:
    assert len(bank) == len(MATRIX)  # yeni soru: question_tables.py'ye satır ekle


def test_every_language_engine_has_enough_questions_at_every_difficulty(
    bank: QuestionBank,
) -> None:
    groups = _groups(bank)
    expected = {
        (Language.C, Engine.NONE),
        (Language.CPP, Engine.NONE),
        (Language.CPP, Engine.UNREAL),
        (Language.CSHARP, Engine.NONE),
        (Language.CSHARP, Engine.UNITY),
        (Language.PYTHON, Engine.NONE),
        (Language.HTML, Engine.NONE),
        (Language.CSS, Engine.NONE),
    }
    assert set(groups) == expected
    for group, difficulties in groups.items():
        assert len(difficulties) >= MIN_PER_GROUP, group
        assert set(difficulties) == set(Difficulty), f"{group}: eksik zorluk"


def test_ids_unique_and_prefixed_by_difficulty(bank: QuestionBank) -> None:
    ids = [q.id for q in bank]
    assert len(ids) == len(set(ids))
    for q in bank:
        assert f"-{q.difficulty.value.replace('_', '')}-" in q.id, q.id


def test_titles_unique(bank: QuestionBank) -> None:
    titles = [q.title.casefold() for q in bank]
    assert len(titles) == len(set(titles))


def test_ids_match_matrix_7_2(bank: QuestionBank) -> None:
    assert {q.id for q in bank} == set(MATRIX)
    for q in bank:
        assert (q.language, q.engine, q.difficulty) == MATRIX[q.id], q.id


def test_every_question_complete(bank: QuestionBank) -> None:
    for q in bank:
        assert len(q.prompt.strip()) >= 80, q.id
        assert len(q.constraints) >= 2, q.id
        assert len(q.concept_tags) >= 2, q.id
        assert len(q.checklist_extra) >= 2, q.id
        assert sorted(q.hint_ladder) == [1, 2, 3], q.id
        assert all(len(h.strip()) >= 20 for h in q.hint_ladder.values()), q.id
        assert q.expected.time if q.expected is not None else not has_complexity(q.language), q.id


def test_hint_ladder_ends_with_concept_name(bank: QuestionBank) -> None:
    """3. seviye ipucu kavramı adlandırır (mimari §7.1 örneği)."""
    for q in bank:
        assert "olarak bilinir" in q.hint_ladder[3], q.id


def test_reference_paths_point_to_private(bank: QuestionBank) -> None:
    extensions = {
        Language.C: ".c",
        Language.CPP: ".cpp",
        Language.CSHARP: ".cs",
        Language.PYTHON: ".py",
        Language.HTML: ".html",
        Language.CSS: ".css",
    }
    for q in bank:
        assert q.reference_solution_path == f"private/solutions/{q.id}{extensions[q.language]}"


@pytest.mark.parametrize("question_id", sorted(MATRIX))
def test_prompts_do_not_reveal_method(bank: QuestionBank, question_id: str) -> None:
    q = bank.get(question_id)
    text = " ".join([q.title, q.prompt, *q.constraints]).lower()
    assert q.method_leaks, f"{question_id}: soru verisinde method_leaks tanımlı olmalı"
    for term in q.method_leaks:
        assert term.lower() not in text, f"{question_id}: '{term}' yöntemi ele veriyor"


def test_leak_table_covers_all_questions(bank: QuestionBank) -> None:
    assert set(METHOD_LEAKS) == set(MATRIX)
    for q in bank:
        assert len(q.method_leaks) >= 1, f"{q.id} method_leaks boş olamaz"


def test_sample_io_structure_and_coverage(bank: QuestionBank) -> None:
    with_samples = [q for q in bank if q.sample_io]
    assert len(with_samples) >= 6, "En az 6 soruda sample_io tanımlı olmalı"
    for q in with_samples:
        for s in q.sample_io:
            assert s.input.strip(), f"{q.id}: örnek girdi boş olamaz"
            assert s.output.strip(), f"{q.id}: örnek çıktı boş olamaz"


def test_reference_solution_uses_hidden_method(bank: QuestionBank) -> None:
    """Yöntem işaretleri gerçekten çözümün yöntemini izliyor: en az biri çözümde geçer.

    `private/` depoda yok (CI); çözüm dosyası yoksa test atlanır.
    """
    root = DATA.parent
    checked = 0
    for q in bank:
        assert q.reference_solution_path is not None, q.id
        path = root / q.reference_solution_path
        if not path.is_file():
            continue
        solution = path.read_text(encoding="utf-8").lower()
        terms = q.method_leaks or METHOD_LEAKS[q.id]
        assert any(term.lower() in solution for term in terms), q.id
        checked += 1
    if checked == 0:
        pytest.skip("private/solutions yok (CI)")


def test_complexity_variables_are_defined(bank: QuestionBank) -> None:
    """`n` dışındaki Big-O değişkenleri (k, d ...) prompt veya kısıtlarda tanımlanmalı."""
    for q in bank:
        if q.expected is None:  # HTML/CSS
            continue
        text = " ".join([q.prompt, *q.constraints])
        values = [*q.expected.time.values(), q.expected.space]
        variables = set().union(*(parse_bigo(v.removesuffix("*")).variables for v in values))
        for var in variables - {"n"}:
            assert re.search(rf"\b{var}\b", text), f"{q.id}: '{var}' tanımsız"


def test_prompts_contain_no_code_blocks(bank: QuestionBank) -> None:
    for q in bank:
        assert "```" not in q.prompt, q.id


def test_checklist_files_exist(checklists: Checklists) -> None:
    assert {f.stem for f in (DATA / "checklists").glob("*.yaml")} == {
        "c",
        "cpp",
        "csharp",
        "unity",
        "unreal",
        "python",
        "html",
        "css",
    }
    assert len(checklists) >= 8


def test_llm_detected_rules_present(checklists: Checklists) -> None:
    """§8.2'de 'LLM' tespitli kurallar kontrol listesinde yaşar."""
    ids = {item.id for item in checklists.all_items()}
    assert {"CPP-UB-001", "UNITY-SO-001", "UE-PTR-001"} <= ids


def test_each_question_gets_tagged_checklist_items(
    bank: QuestionBank, checklists: Checklists
) -> None:
    for q in bank:
        items = checklists.select_items(q.language, q.engine, q.concept_tags)
        tagged = [i for i in items if CORE_TAG not in i.tags]
        assert tagged, f"{q.id}: concept_tags hiçbir kontrol maddesiyle kesişmiyor"
        assert len(items) <= 12


def test_core_items_exist_for_every_language(checklists: Checklists) -> None:
    for language in Language:
        items = checklists.select_items(language, Engine.NONE, [])
        assert items, language
        assert all(CORE_TAG in i.tags for i in items)
