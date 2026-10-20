"""Faz K (ADR-0028): kullanıcı soruları — taslak, kimlik, depo, banka birleştirme, CLI."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
from pydantic import ValidationError
from typer.testing import CliRunner, Result

from codementor.cli.main import app
from codementor.config import CONFIG_FILE_ENV, DataSettings
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import (
    DEFAULT_USER_CONSTRAINT,
    DEFAULT_USER_HINTS,
    DEFAULT_USER_TAG,
    Question,
    QuestionPublic,
    UserQuestionDraft,
)
from codementor.questions.bank import QuestionBank
from codementor.questions.user_store import (
    UserQuestionError,
    delete_question,
    get_question,
    load_user_questions,
    new_question_id,
    save_question,
    slugify,
)

REPO = Path(__file__).resolve().parents[2]
BUILTIN = REPO / "data" / "questions"


def _draft(**kw: object) -> UserQuestionDraft:
    base: dict[str, object] = {
        "title": "Dizideki en büyük iki sayı",
        "prompt": "En büyük iki farklı değeri bulan fonksiyonu yazın.",
        "language": "c",
        "difficulty": "easy",
    }
    return UserQuestionDraft.model_validate(base | kw)


# --- taslak → soru ------------------------------------------------------------------------------


def test_minimal_draft_fills_defaults() -> None:
    question = _draft().to_question("kullanici-x")
    assert question.origin == "user"
    assert question.expected is None  # kullanıcı sorusunda hedef karmaşıklık isteğe bağlı
    assert question.constraints == [DEFAULT_USER_CONSTRAINT]
    assert question.concept_tags == [DEFAULT_USER_TAG]
    assert [question.hint_ladder[i] for i in (1, 2, 3)] == list(DEFAULT_USER_HINTS)
    assert question.reference_solution_path is None
    assert question.to_public().origin == "user"


def test_full_draft_kept() -> None:
    draft = _draft(
        constraints=["O(1) ek bellek", "", "  "],
        expected_time="O(n)",
        expected_space="1",
        concept_tags=["arrays", "edge-cases", "arrays"],
        hints=["İlk ipucu", "İkinci ipucu"],
    )
    question = draft.to_question("kullanici-x")
    assert question.constraints == ["O(1) ek bellek"]  # boş satırlar atılır
    assert question.expected is not None
    assert question.expected.space == "1"
    assert list(question.expected.time.values()) == ["n"]  # `O(...)` sarmalayıcısı atılır
    assert question.concept_tags == ["arrays", "edge-cases"]
    assert question.hint_ladder[1] == "İlk ipucu"
    assert question.hint_ladder[3] == DEFAULT_USER_HINTS[2]
    assert UserQuestionDraft.from_question(question) == draft.model_copy(
        update={"constraints": ["O(1) ek bellek"], "concept_tags": ["arrays", "edge-cases"]}
    )


def test_from_question_hides_only_pure_defaults() -> None:
    """Genel varsayılanlar formda boş görünür; kullanıcının açıkça yazdığı liste korunur (G6)."""
    question = _draft().to_question("kullanici-x")
    back = UserQuestionDraft.from_question(question)
    assert back.constraints == []
    assert back.concept_tags == []


def test_from_question_keeps_explicit_general_with_others() -> None:
    """`['genel', 'dizi']` düzenlemede 'dizi'ye indirgenmiyor; varsayılan kısıt atılmıyor (G6)."""
    draft = _draft(
        concept_tags=[DEFAULT_USER_TAG, "dizi"],
        constraints=[DEFAULT_USER_CONSTRAINT, "O(1) ek bellek"],
    )
    question = draft.to_question("kullanici-x")
    back = UserQuestionDraft.from_question(question)
    assert back.concept_tags == [DEFAULT_USER_TAG, "dizi"]
    assert back.constraints == [DEFAULT_USER_CONSTRAINT, "O(1) ek bellek"]
    assert back.to_question("kullanici-x") == question  # düzenle → kaydet kayıpsız


@pytest.mark.parametrize(
    "update",
    [
        {"title": "  "},
        {"prompt": ""},
        {"expected_time": "n"},  # bellek yok
        {"expected_space": "1"},  # zaman yok
        {"expected_time": "üstel", "expected_space": "1"},  # geçersiz Big-O
        {"language": "html", "expected_time": "n", "expected_space": "1"},  # HTML'de olmaz
        {"engine": "unity"},  # Unity yalnız C#
        {"concept_tags": ["Büyük Harf"]},
        {"hints": ["a", "b", "c", "d"]},
    ],
)
def test_invalid_draft_rejected(update: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        _draft(**update)


def test_builtin_still_requires_expected() -> None:
    data = _draft().to_question("kullanici-x").to_public().model_dump()
    with pytest.raises(ValidationError, match="hedef karmaşıklık"):
        QuestionPublic.model_validate(data | {"id": "c-easy-yeni", "origin": "builtin"})


def test_user_origin_requires_prefix() -> None:
    data = _draft().to_question("kullanici-x").to_public().model_dump()
    with pytest.raises(ValidationError, match="kullanici-"):
        QuestionPublic.model_validate(data | {"id": "c-easy-sahte"})


# --- kimlik -------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("title", "slug"),
    [
        ("Bağlı liste — tersine çevir", "bagli-liste-tersine-cevir"),
        ("İŞARETÇİ ÖĞRENİYORUM", "isaretci-ogreniyorum"),
        ("C++ / şablonlar (2)", "c-sablonlar-2"),
        ("!!!", "soru"),
        ("a" * 200, "a" * 48),
    ],
)
def test_slugify(title: str, slug: str) -> None:
    assert slugify(title) == slug


def test_new_id_avoids_existing_and_builtin(tmp_path: Path) -> None:
    first = save_question(_draft(), tmp_path)
    assert first.id == "kullanici-dizideki-en-buyuk-iki-sayi"
    assert new_question_id(_draft().title, tmp_path) == f"{first.id}-2"
    taken = {f"{first.id}-2"}
    assert new_question_id(_draft().title, tmp_path, taken) == f"{first.id}-3"


# --- depo ---------------------------------------------------------------------------------------


def test_save_load_update_delete(tmp_path: Path) -> None:
    saved = save_question(_draft(), tmp_path)
    assert (tmp_path / f"{saved.id}.yaml").is_file()
    loaded, warnings = load_user_questions(tmp_path)
    assert warnings == []
    assert loaded == [saved]
    updated = save_question(_draft(title="Yeni başlık"), tmp_path, question_id=saved.id)
    assert updated.id == saved.id  # kimlik değişmez
    assert updated.version == 2
    assert get_question(saved.id, tmp_path).title == "Yeni başlık"
    delete_question(saved.id, tmp_path)
    assert load_user_questions(tmp_path) == ([], [])


def test_atomic_write_leaves_no_temp_files(tmp_path: Path) -> None:
    save_question(_draft(), tmp_path)
    assert [p.suffix for p in tmp_path.iterdir()] == [".yaml"]


@pytest.mark.parametrize("question_id", ["c-easy-palindrome", "kullanici-../x", "kullanici-yok"])
def test_cannot_delete_builtin_or_missing(tmp_path: Path, question_id: str) -> None:
    with pytest.raises(UserQuestionError):
        delete_question(question_id, tmp_path)


def test_missing_directory_is_empty(tmp_path: Path) -> None:
    assert load_user_questions(tmp_path / "yok") == ([], [])


def test_broken_user_files_skipped_with_warning(tmp_path: Path) -> None:
    good = save_question(_draft(), tmp_path)
    (tmp_path / "kullanici-bozuk.yaml").write_text("title: [", encoding="utf-8")
    builtin = (BUILTIN / "c-easy-palindrome.yaml").read_text(encoding="utf-8")
    (tmp_path / "c-easy-palindrome.yaml").write_text(builtin, encoding="utf-8")  # origin user değil
    questions, warnings = load_user_questions(tmp_path)
    assert [q.id for q in questions] == [good.id]
    assert len(warnings) == 2
    assert all("atlandı" in w for w in warnings)


def test_save_error_is_user_question_error(tmp_path: Path) -> None:
    """Hedef dizin bir dosyanın altında: oluşturulamaz (her platformda)."""
    target = tmp_path / "dosya"
    target.write_text("dizin değil", encoding="utf-8")
    with pytest.raises(UserQuestionError, match="kaydedilemedi"):
        save_question(_draft(), target / "alt")


# --- banka birleştirme --------------------------------------------------------------------------


def _data(user_dir: Path) -> DataSettings:
    return DataSettings(questions_dir=BUILTIN, user_questions_dir=user_dir)


def test_load_all_merges_user_questions(tmp_path: Path) -> None:
    saved = save_question(_draft(), tmp_path)
    bank = QuestionBank.load_all(_data(tmp_path))
    builtin = QuestionBank.load(BUILTIN)
    assert len(bank) == len(builtin) + 1
    assert bank.get(saved.id) == saved
    assert [q.id for q in bank.filter(origin="user")] == [saved.id]
    assert len(bank.filter(Language.C, Engine.NONE, Difficulty.EASY)) == (
        len(builtin.filter(Language.C, Engine.NONE, Difficulty.EASY)) + 1
    )
    assert bank.warnings == []


def test_load_all_without_user_dir(tmp_path: Path) -> None:
    assert len(QuestionBank.load_all(_data(tmp_path / "yok"))) == len(QuestionBank.load(BUILTIN))


def test_load_all_reports_skipped(tmp_path: Path) -> None:
    (tmp_path / "kullanici-bozuk.yaml").write_text("{", encoding="utf-8")
    bank = QuestionBank.load_all(_data(tmp_path))
    assert len(bank.warnings) == 1


# --- CLI ----------------------------------------------------------------------------------------


@pytest.fixture
def cli_env(tmp_path: Path) -> dict[str, str]:
    return {
        "COLUMNS": "200",
        CONFIG_FILE_ENV: str(tmp_path / "yok.toml"),
        "CODEMENTOR_DATA__USER_QUESTIONS_DIR": str(tmp_path / "sorularim"),
    }


def _cli(env: dict[str, str], *args: str) -> Result:
    return CliRunner().invoke(app, ["questions", *args], env=env)


def test_cli_add_list_show_remove(tmp_path: Path, cli_env: dict[str, str]) -> None:
    source = tmp_path / "soru.yaml"
    source.write_text(
        "title: Dizideki en büyük iki sayı\n"
        "prompt: En büyük iki değeri bulun.\n"
        "language: c\n"
        "difficulty: easy\n"
        "expected_time: O(n)\n"
        "expected_space: O(1)\n",
        encoding="utf-8",
    )
    added = _cli(cli_env, "add", str(source))
    assert added.exit_code == 0, added.output
    question_id = "kullanici-dizideki-en-buyuk-iki-sayi"
    assert question_id in added.output
    listed = _cli(cli_env, "list", "--language", "c")
    assert question_id in listed.output
    assert "(kendi)" in listed.output
    shown = _cli(cli_env, "show", question_id)
    assert shown.exit_code == 0, shown.output
    assert "O(n)" in shown.output
    removed = _cli(cli_env, "remove", question_id)
    assert removed.exit_code == 0, removed.output
    assert question_id not in _cli(cli_env, "list").output


def test_cli_add_invalid_file(tmp_path: Path, cli_env: dict[str, str]) -> None:
    source = tmp_path / "soru.yaml"
    source.write_text("title: x\nlanguage: c\ndifficulty: easy\n", encoding="utf-8")  # prompt yok
    result = _cli(cli_env, "add", str(source))
    assert result.exit_code == 1
    assert "Hata" in result.output


def test_cli_remove_builtin_refused(cli_env: dict[str, str]) -> None:
    result = _cli(cli_env, "remove", "c-easy-palindrome")
    assert result.exit_code == 1
    assert "Yalnız kendi eklediğin" in result.output


def test_cli_validate_ignores_user_questions(tmp_path: Path, cli_env: dict[str, str]) -> None:
    save_question(_draft(), tmp_path / "sorularim")
    result = _cli(cli_env, "validate")
    assert result.exit_code == 0, result.output
    assert str(len(QuestionBank.load(BUILTIN))) in result.output


def test_question_model_round_trip_yaml(tmp_path: Path) -> None:
    saved = save_question(_draft(hints=["a"]), tmp_path)
    text = (tmp_path / f"{saved.id}.yaml").read_text(encoding="utf-8")
    assert "origin: user" in text
    assert "reference_solution_path" not in text
    assert isinstance(get_question(saved.id, tmp_path), Question)


def test_save_survives_transient_file_lock(
    tmp_path: Path, locked_replace: Callable[[int], list[int]]
) -> None:
    left = locked_replace(2)
    saved = save_question(_draft(), tmp_path)
    assert left == [0]
    assert get_question(saved.id, tmp_path) == saved
    assert [p.suffix for p in tmp_path.iterdir()] == [".yaml"]
