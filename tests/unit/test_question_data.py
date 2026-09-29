"""Depodaki gerçek soru bankası ve kontrol listesi içeriğinin bütünlük testleri."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from codementor.models.bigo import parse_bigo
from codementor.models.enums import Difficulty, Engine, Language
from codementor.questions.bank import QuestionBank
from codementor.questions.checklists import CORE_TAG, Checklists

DATA = Path(__file__).resolve().parents[2] / "data"

# Mimari §7.2 başlangıç matrisi
MATRIX: dict[str, tuple[Language, Engine, Difficulty]] = {
    "c-veryeasy-calculator": (Language.C, Engine.NONE, Difficulty.VERY_EASY),
    "c-easy-reverse-string": (Language.C, Engine.NONE, Difficulty.EASY),
    "c-medium-linked-list": (Language.C, Engine.NONE, Difficulty.MEDIUM),
    "c-hard-stack": (Language.C, Engine.NONE, Difficulty.HARD),
    "cpp-easy-rule-of-zero": (Language.CPP, Engine.NONE, Difficulty.EASY),
    "cpp-medium-tree-smartptr": (Language.CPP, Engine.NONE, Difficulty.MEDIUM),
    "cpp-hard-lru-cache": (Language.CPP, Engine.NONE, Difficulty.HARD),
    "cs-easy-fizzbuzz-alloc": (Language.CSHARP, Engine.NONE, Difficulty.EASY),
    "cs-hard-span-parser": (Language.CSHARP, Engine.NONE, Difficulty.HARD),
    "unity-easy-trigger-events": (Language.CSHARP, Engine.UNITY, Difficulty.EASY),
    "unity-medium-object-pool": (Language.CSHARP, Engine.UNITY, Difficulty.MEDIUM),
    "unity-hard-inventory": (Language.CSHARP, Engine.UNITY, Difficulty.HARD),
    "unreal-medium-actor-component": (Language.CPP, Engine.UNREAL, Difficulty.MEDIUM),
    "unreal-hard-tarray-gc": (Language.CPP, Engine.UNREAL, Difficulty.HARD),
}

# Soru metni (başlık + prompt + kısıtlar) problemi tanımlar, yöntemi söylemez.
# Hedef kavramın çözümünü ele veren terimler metinde geçmemeli (büyük/küçük harf duyarsız).
METHOD_LEAKS: dict[str, list[str]] = {
    "c-veryeasy-calculator": ["fflush", "getchar", "while ((c"],
    "c-easy-reverse-string": ["strlen"],
    "c-medium-linked-list": ["**", "pointer to pointer", "çift pointer"],
    "c-hard-stack": ["tmp", "geçici pointer"],
    "cpp-easy-rule-of-zero": ["rule of", "unique_ptr", "std::vector<double>"],
    "cpp-medium-tree-smartptr": ["weak_ptr", "shared_ptr", "unique_ptr"],
    "cpp-hard-lru-cache": ["unordered_map", "std::list", "splice", "bağlı liste"],
    "cs-easy-fizzbuzz-alloc": ["stringbuilder", "string.join", "string.concat"],
    "cs-hard-span-parser": ["span", "memory<", "stackalloc", "readonlyspan", "tryparse"],
    "unity-easy-trigger-events": ["ondisable", "ondestroy", "-=", "action", "unityevent"],
    "unity-medium-object-pool": ["havuz", "pool", "setactive", "yeniden kullan"],
    "unity-hard-inventory": ["hashset", "dictionary", "instantiate(", "event"],
    "unreal-medium-actor-component": ["bcanevertick", "setcomponenttickenabled", "timer"],
    "unreal-hard-tarray-gc": ["uproperty", "reserve", "tweakobjectptr", "tobjectptr", "isvalid"],
}


@pytest.fixture(scope="module")
def bank() -> QuestionBank:
    return QuestionBank.load(DATA / "questions")


@pytest.fixture(scope="module")
def checklists() -> Checklists:
    return Checklists.load(DATA / "checklists")


def test_all_14_questions_load(bank: QuestionBank) -> None:
    assert len(bank) == 14


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
        assert q.expected.time, q.id


def test_hint_ladder_ends_with_concept_name(bank: QuestionBank) -> None:
    """3. seviye ipucu kavramı adlandırır (mimari §7.1 örneği)."""
    for q in bank:
        assert "olarak bilinir" in q.hint_ladder[3], q.id


def test_reference_paths_point_to_private(bank: QuestionBank) -> None:
    extensions = {Language.C: ".c", Language.CPP: ".cpp", Language.CSHARP: ".cs"}
    for q in bank:
        assert q.reference_solution_path == f"private/solutions/{q.id}{extensions[q.language]}"


@pytest.mark.parametrize("question_id", sorted(METHOD_LEAKS))
def test_prompts_do_not_reveal_method(bank: QuestionBank, question_id: str) -> None:
    q = bank.get(question_id)
    text = " ".join([q.title, q.prompt, *q.constraints]).lower()
    for term in METHOD_LEAKS[question_id]:
        assert term.lower() not in text, f"{question_id}: '{term}' yöntemi ele veriyor"


def test_leak_table_covers_all_questions() -> None:
    assert set(METHOD_LEAKS) == set(MATRIX)


def test_complexity_variables_are_defined(bank: QuestionBank) -> None:
    """`n` dışındaki Big-O değişkenleri (k, d ...) prompt veya kısıtlarda tanımlanmalı."""
    for q in bank:
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
    }
    assert len(checklists) >= 5


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
