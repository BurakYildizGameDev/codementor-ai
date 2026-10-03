"""Soru bankası bütünlük denetimi (Faz 30): `codementor questions validate`'in kütüphanesi."""

from __future__ import annotations

from pathlib import Path

from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import Question
from codementor.questions.bank import QuestionBank
from codementor.questions.checklists import Checklists
from codementor.questions.validate import validate_bank

DATA = Path(__file__).resolve().parents[2] / "data"


def _question(
    qid: str,
    difficulty: Difficulty = Difficulty.EASY,
    tags: tuple[str, ...] = ("strings", "edge-cases"),
    solution: str | None = None,
) -> Question:
    return Question.model_validate(
        {
            "id": qid,
            "version": 1,
            "language": Language.PYTHON,
            "engine": Engine.NONE,
            "difficulty": difficulty,
            "title": qid,
            "prompt": "Bir fonksiyon yazın.",
            "constraints": ["Doğru çalışmalı"],
            "expected": {"time": {"f": "n"}, "space": "1"},
            "concept_tags": list(tags),
            "hint_ladder": {1: "a", 2: "b", 3: "c"},
            "reference_solution_path": solution,
        }
    )


def _full_python_group(tmp_path: Path) -> list[Question]:
    questions = []
    for i, difficulty in enumerate([*Difficulty, *Difficulty]):
        rel = f"private/solutions/py-{i}.py"
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text("pass\n", encoding="utf-8")
        questions.append(_question(f"py-q{i}", difficulty, solution=rel))
    return questions


def test_real_bank_is_valid() -> None:
    report = validate_bank(
        QuestionBank.load(DATA / "questions"),
        Checklists.load(DATA / "checklists"),
        solutions_root=None,
    )
    assert report.errors == []


def test_too_few_questions_and_missing_difficulty_reported() -> None:
    bank = QuestionBank([_question("py-a"), _question("py-b", Difficulty.HARD)])
    report = validate_bank(bank, Checklists.load(DATA / "checklists"), min_per_group=8)
    assert any("python" in e and "2 soru" in e for e in report.errors)
    assert any("very_easy" in e and "medium" in e for e in report.errors)


def test_untagged_checklist_reported(tmp_path: Path) -> None:
    questions = _full_python_group(tmp_path)
    questions[0] = _question("py-q0", Difficulty.VERY_EASY, tags=("yok-boyle-etiket", "baska"))
    report = validate_bank(
        QuestionBank(questions), Checklists.load(DATA / "checklists"), min_per_group=8
    )
    assert any("py-q0" in e and "kontrol" in e for e in report.errors)


def test_missing_solution_is_warning_not_error(tmp_path: Path) -> None:
    questions = _full_python_group(tmp_path)
    questions[1] = _question("py-q1", Difficulty.EASY, solution="private/solutions/yok.py")
    report = validate_bank(
        QuestionBank(questions),
        Checklists.load(DATA / "checklists"),
        min_per_group=8,
        solutions_root=tmp_path,
    )
    assert report.errors == []
    assert any("py-q1" in w and "çözüm" in w for w in report.warnings)


def test_no_solution_check_without_root(tmp_path: Path) -> None:
    questions = _full_python_group(tmp_path)
    report = validate_bank(
        QuestionBank(questions), Checklists.load(DATA / "checklists"), min_per_group=8
    )
    assert report.warnings == []


def test_empty_bank_is_an_error() -> None:
    report = validate_bank(QuestionBank([]), Checklists.load(DATA / "checklists"))
    assert report.question_count == 0
    assert any("boş" in e for e in report.errors)


def test_unreadable_solution_reason_reported(tmp_path: Path) -> None:
    """Faz 31: validate yalnız `is_file()` değil, analizdeki çözücüyle (boyut, private/ sınırı)
    denetler; nedeni uyarıda söyler."""
    from codementor.questions.reference import MAX_REFERENCE_BYTES

    big = tmp_path / "private" / "solutions" / "big.py"
    big.parent.mkdir(parents=True)
    big.write_text("x" * (MAX_REFERENCE_BYTES + 1), encoding="utf-8")
    questions = _full_python_group(tmp_path)
    questions[1] = _question("py-q1", Difficulty.EASY, solution="private/solutions/big.py")
    report = validate_bank(
        QuestionBank(questions),
        Checklists.load(DATA / "checklists"),
        min_per_group=8,
        solutions_root=tmp_path,
    )
    assert any("py-q1" in w and "büyük" in w for w in report.warnings)
