"""Soru bankası yükleyici testleri (mimari §7.1)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import MENTOR_FIELDS, Question, QuestionPublic
from codementor.questions.bank import QuestionBank, QuestionBankError, QuestionNotFoundError


def _question(qid: str = "c-hard-stack", **kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "id": qid,
        "version": 1,
        "language": "c",
        "engine": "none",
        "difficulty": "hard",
        "title": "Dinamik büyüyen yığın",
        "prompt": "push, pop, peek ve destroy işlemlerini destekleyen bir yığın yazın.\n",
        "constraints": ["push amortize O(1) olmalı"],
        "expected": {"time": {"push": "1*", "pop": "1"}, "space": "n"},
        "concept_tags": ["realloc", "memory-safety"],
        "checklist_extra": ["realloc dönüşü kontrol ediliyor mu?"],
        "reference_solution_path": f"private/solutions/{qid}.c",
        "hint_ladder": {1: "Birinci", 2: "İkinci", 3: "Üçüncü"},
    }
    return base | kw


def _write(directory: Path, data: dict[str, Any], name: str | None = None) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{name or data['id']}.yaml"
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


# ---------------------------------------------------------------- yükleme


def test_load_valid_dir(tmp_path: Path) -> None:
    _write(tmp_path, _question())
    _write(
        tmp_path,
        _question(
            "unity-easy-trigger-events",
            language="csharp",
            engine="unity",
            difficulty="easy",
            reference_solution_path=None,
        ),
    )
    bank = QuestionBank.load(tmp_path)
    assert len(bank) == 2
    assert "c-hard-stack" in bank
    q = bank.get("c-hard-stack")
    assert isinstance(q, Question)
    assert q.language is Language.C
    assert q.hint_ladder[3] == "Üçüncü"


def test_load_accepts_yml_extension(tmp_path: Path) -> None:
    _write(tmp_path, _question())
    (tmp_path / "c-hard-stack.yaml").rename(tmp_path / "c-hard-stack.yml")
    assert len(QuestionBank.load(tmp_path)) == 1


def test_missing_dir_error(tmp_path: Path) -> None:
    with pytest.raises(QuestionBankError, match="bulunamadı"):
        QuestionBank.load(tmp_path / "yok")


def test_duplicate_id_error(tmp_path: Path) -> None:
    _write(tmp_path, _question())
    (tmp_path / "c-hard-stack.yml").write_text(
        (tmp_path / "c-hard-stack.yaml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    with pytest.raises(QuestionBankError, match=r"Yinelenen soru kimliği 'c-hard-stack'") as exc:
        QuestionBank.load(tmp_path)
    assert "c-hard-stack.yaml" in str(exc.value)
    assert "c-hard-stack.yml" in str(exc.value)


def test_duplicate_id_error_from_constructor() -> None:
    q = Question.model_validate(_question())
    with pytest.raises(QuestionBankError, match="Yinelenen"):
        QuestionBank([q, q])


def test_id_filename_mismatch(tmp_path: Path) -> None:
    _write(tmp_path, _question(), name="baska-ad")
    with pytest.raises(QuestionBankError, match="dosya adıyla eşleşmiyor"):
        QuestionBank.load(tmp_path)


def test_yaml_syntax_error_message(tmp_path: Path) -> None:
    (tmp_path / "bozuk.yaml").write_text("id: [kapanmamış\n", encoding="utf-8")
    with pytest.raises(QuestionBankError, match=r"bozuk\.yaml: YAML sözdizimi hatası"):
        QuestionBank.load(tmp_path)


def test_non_mapping_yaml_error(tmp_path: Path) -> None:
    (tmp_path / "liste.yaml").write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(QuestionBankError, match="eşleme"):
        QuestionBank.load(tmp_path)


def test_validation_error_message_has_file_and_field(tmp_path: Path) -> None:
    data = _question()
    del data["title"]
    data["difficulty"] = "impossible"
    data["surprise"] = 1
    _write(tmp_path, data)
    with pytest.raises(QuestionBankError) as exc:
        QuestionBank.load(tmp_path)
    msg = str(exc.value)
    assert "c-hard-stack.yaml" in msg
    assert "title: alan zorunlu" in msg
    assert "difficulty: geçersiz değer" in msg
    assert "surprise: tanımsız alan" in msg


@pytest.mark.parametrize(
    "ladder",
    [
        {1: "a", 2: "b"},
        {1: "a", 2: "b", 3: "c", 4: "d"},
        {1: "a", 2: "   ", 3: "c"},
        {0: "a", 1: "b", 2: "c"},
    ],
)
def test_hint_ladder_must_have_three_levels(tmp_path: Path, ladder: dict[int, str]) -> None:
    _write(tmp_path, _question(hint_ladder=ladder))
    with pytest.raises(QuestionBankError, match="hint_ladder"):
        QuestionBank.load(tmp_path)


@pytest.mark.parametrize(
    ("language", "engine"),
    [("c", "unity"), ("cpp", "unity"), ("csharp", "unreal"), ("c", "unreal")],
)
def test_engine_language_mismatch(tmp_path: Path, language: str, engine: str) -> None:
    _write(tmp_path, _question(language=language, engine=engine))
    with pytest.raises(QuestionBankError, match="motoru"):
        QuestionBank.load(tmp_path)


def test_expected_amortized_accepted() -> None:
    q = Question.model_validate(_question())
    assert q.expected.time["push"] == "1*"


@pytest.mark.parametrize("bad", ["çok hızlı", "O(", "1**"])
def test_invalid_bigo_rejected(bad: str) -> None:
    with pytest.raises(ValueError, match="ayrıştırılamadı"):
        Question.model_validate(_question(expected={"time": {"push": bad}, "space": "n"}))


@pytest.mark.parametrize(
    "path",
    [
        "solutions/x.c",
        "/etc/passwd",
        "private/../secret.c",
        "private/a/../../x.c",
        "C:\\private\\x.c",
        "private",
        "private/",
        "private/\x00x.c",
        "private/C:/x.c",
        "private/x.c:stream",
        "",
    ],
)
def test_reference_path_must_stay_in_private(path: str) -> None:
    with pytest.raises(ValueError, match="private/"):
        Question.model_validate(_question(reference_solution_path=path))


def test_reference_path_is_normalized() -> None:
    q = Question.model_validate(_question(reference_solution_path="./private//solutions/x.c"))
    assert q.reference_solution_path == "private/solutions/x.c"


def test_duplicate_tags_rejected() -> None:
    with pytest.raises(ValueError, match="yinelenen öğe: realloc"):
        Question.model_validate(_question(concept_tags=["realloc", "gc", "realloc"]))


def test_empty_operation_name_rejected() -> None:
    with pytest.raises(ValueError, match=r"expected\.time"):
        Question.model_validate(_question(expected={"time": {"  ": "1"}, "space": "n"}))


def test_yaml_duplicate_key_rejected(tmp_path: Path) -> None:
    text = yaml.safe_dump(_question(), allow_unicode=True, sort_keys=False)
    (tmp_path / "c-hard-stack.yaml").write_text(text + "title: ikinci\n", encoding="utf-8")
    with pytest.raises(QuestionBankError, match=r"c-hard-stack\.yaml: yinelenen anahtar 'title'"):
        QuestionBank.load(tmp_path)


def test_uppercase_extension_loaded(tmp_path: Path) -> None:
    _write(tmp_path, _question())
    (tmp_path / "c-hard-stack.yaml").rename(tmp_path / "c-hard-stack.YAML")
    assert "c-hard-stack" in QuestionBank.load(tmp_path)


def test_pattern_error_message_is_readable(tmp_path: Path) -> None:
    _write(tmp_path, _question("C_Hard"), name="C_Hard")
    with pytest.raises(QuestionBankError, match=r"id: biçim geçersiz \(.*ör\. c-hard-stack\)"):
        QuestionBank.load(tmp_path)


def test_unmapped_error_types_are_turkish(tmp_path: Path) -> None:
    _write(tmp_path, _question(version=True, concept_tags=[True]))
    with pytest.raises(QuestionBankError) as exc:
        QuestionBank.load(tmp_path)
    msg = str(exc.value)
    assert "concept_tags.0: metin olmalı" in msg
    assert "Input should" not in msg  # pydantic'in İngilizce metni sızmamalı


def test_error_message_does_not_echo_values(tmp_path: Path) -> None:
    _write(tmp_path, _question(reference_solution_path="private/../gizli-yol.c"))
    with pytest.raises(QuestionBankError) as exc:
        QuestionBank.load(tmp_path)
    assert "gizli-yol" not in str(exc.value)


@pytest.mark.parametrize("qid", ["C-Hard-Stack", "c_hard_stack", "stack", "c--x"])
def test_invalid_id_format(qid: str) -> None:
    with pytest.raises(ValueError, match="id"):
        Question.model_validate(_question(qid))


@pytest.mark.parametrize("field", ["constraints", "concept_tags"])
def test_required_lists_not_empty(field: str) -> None:
    with pytest.raises(ValueError, match=field):
        Question.model_validate(_question(**{field: []}))


# ---------------------------------------------------------------- erişim


def _bank() -> QuestionBank:
    specs = [
        ("c-veryeasy-calculator", "c", "none", "very_easy"),
        ("c-hard-stack", "c", "none", "hard"),
        ("cpp-hard-lru-cache", "cpp", "none", "hard"),
        ("cs-easy-fizzbuzz-alloc", "csharp", "none", "easy"),
        ("unity-hard-inventory", "csharp", "unity", "hard"),
        ("unreal-medium-actor-component", "cpp", "unreal", "medium"),
    ]
    return QuestionBank(
        Question.model_validate(
            _question(qid, language=lang, engine=eng, difficulty=diff, reference_solution_path=None)
        )
        for qid, lang, eng, diff in specs
    )


def test_get_unknown_raises() -> None:
    with pytest.raises(QuestionNotFoundError, match="Soru bulunamadı: 'yok'"):
        _bank().get("yok")


def test_not_found_is_lookup_error() -> None:
    assert issubclass(QuestionNotFoundError, LookupError)


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        ({}, 6),
        ({"language": Language.C}, 2),
        ({"language": Language.C, "difficulty": Difficulty.HARD}, 1),
        ({"engine": Engine.NONE}, 4),
        ({"language": Language.CSHARP}, 2),
        ({"language": Language.CSHARP, "engine": Engine.UNITY}, 1),
        ({"difficulty": Difficulty.HARD}, 3),
        ({"engine": Engine.UNREAL, "difficulty": Difficulty.EASY}, 0),
    ],
)
def test_filter_combinations(kwargs: dict[str, Any], expected: int) -> None:
    result = _bank().filter(**kwargs)
    assert len(result) == expected
    for q in result:
        for key, value in kwargs.items():
            assert getattr(q, key) == value


def test_filter_returns_public_models_in_stable_order() -> None:
    result = _bank().filter()
    assert all(type(q) is QuestionPublic for q in result)
    ids = [q.id for q in result]
    assert ids[:2] == ["c-veryeasy-calculator", "c-hard-stack"]  # dil, sonra zorluk sırası
    assert ids == [q.id for q in _bank().filter()]


def test_iteration_yields_internal_questions() -> None:
    assert all(isinstance(q, Question) for q in _bank())


# ---------------------------------------------------------------- Public model (§12)


HIDDEN_FIELDS = ["reference_solution_path", "concept_tags", "checklist_extra", "hint_ladder"]


@pytest.mark.parametrize("field", HIDDEN_FIELDS)
def test_public_model_has_no_reference_path(field: str) -> None:
    """Referans çözüm yolu (§12) ve mentorluk verisi Public modelde hiç yok."""
    assert field not in QuestionPublic.model_fields
    assert field not in str(QuestionPublic.model_json_schema())
    q = Question.model_validate(_question())
    public = q.to_public()
    assert type(public) is QuestionPublic
    assert field not in public.model_dump()


def test_public_dump_has_no_mentor_text() -> None:
    q = Question.model_validate(_question())
    dumped = q.to_public().model_dump_json()
    assert "private/" not in dumped
    assert "Üçüncü" not in dumped  # ipucu metni
    assert "realloc dönüşü" not in dumped  # checklist_extra
    assert set(MENTOR_FIELDS) < set(Question.model_fields)


def test_public_model_rejects_mentor_fields() -> None:
    with pytest.raises(ValueError, match="hint_ladder"):
        QuestionPublic.model_validate(_question())


def test_bank_public_accessor() -> None:
    bank = QuestionBank([Question.model_validate(_question())])
    public = bank.public("c-hard-stack")
    assert type(public) is QuestionPublic
    assert not hasattr(public, "reference_solution_path")


def test_filter_accepts_plain_strings() -> None:
    """StrEnum değerleri düz metinle de eşleşmeli (ör. API sorgu parametreleri)."""
    result = _bank().filter(language="c", difficulty="hard")  # type: ignore[arg-type]
    assert [q.id for q in result] == ["c-hard-stack"]
