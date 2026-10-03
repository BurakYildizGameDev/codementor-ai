"""`codementor questions list|show` testleri (mimari §10)."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner, Result

from codementor.cli.main import app
from codementor.config import CONFIG_FILE_ENV
from codementor.questions.bank import QuestionBank

QUESTIONS = Path(__file__).resolve().parents[2] / "data" / "questions"


def _invoke(*args: str) -> Result:
    return CliRunner().invoke(app, ["questions", *args], env={"COLUMNS": "200"})


def _run(*args: str) -> tuple[int, str]:
    result = _invoke(*args)
    return result.exit_code, result.output


def test_list_all() -> None:
    code, out = _run("list", "--dir", str(QUESTIONS))
    assert code == 0, out
    for q in QuestionBank.load(QUESTIONS):
        assert q.id in out


def test_list_filters_c_hard() -> None:
    code, out = _run("list", "--language", "c", "--difficulty", "hard", "--dir", str(QUESTIONS))
    assert code == 0, out
    assert "c-hard-stack" in out
    assert "c-medium-linked-list" not in out
    assert "cpp-hard-lru-cache" not in out


def test_list_filters_engine() -> None:
    code, out = _run("list", "--engine", "unreal", "--dir", str(QUESTIONS))
    assert code == 0, out
    assert "unreal-hard-tarray-gc" in out
    assert "unity-hard-inventory" not in out


def test_list_empty_result_message() -> None:
    code, out = _run("list", "--language", "css", "--engine", "unreal", "--dir", str(QUESTIONS))
    assert code == 0
    assert "Eşleşen soru yok" in out


def test_list_invalid_choice() -> None:
    code, _ = _run("list", "--language", "rust", "--dir", str(QUESTIONS))
    assert code == 2


def test_show_question() -> None:
    code, out = _run("show", "unity-hard-inventory", "--dir", str(QUESTIONS))
    assert code == 0, out
    q = QuestionBank.load(QUESTIONS).get("unity-hard-inventory")
    assert q.title in out
    assert q.constraints[0] in out


def test_show_hides_reference_path_and_mentor_data() -> None:
    q = QuestionBank.load(QUESTIONS).get("c-hard-stack")
    code, out = _run("show", "c-hard-stack", "--dir", str(QUESTIONS))
    assert code == 0, out
    assert "private/" not in out
    assert "reference_solution" not in out
    for hint in q.hint_ladder.values():
        assert hint not in out
    for extra in q.checklist_extra:
        assert extra not in out


def test_show_expected_complexity_display() -> None:
    code, out = _run("show", "c-hard-stack", "--dir", str(QUESTIONS))
    assert code == 0, out
    assert "O(1) amortize" in out


def test_show_unknown_id_exit_code() -> None:
    result = _invoke("show", "yok-boyle-soru", "--dir", str(QUESTIONS))
    assert result.exit_code == 1
    assert "Soru bulunamadı" in result.stderr
    assert result.stdout == ""


def test_broken_bank_exit_code(tmp_path: Path) -> None:
    (tmp_path / "bozuk.yaml").write_text("id: [\n", encoding="utf-8")
    result = _invoke("list", "--dir", str(tmp_path))
    assert result.exit_code == 3
    assert "bozuk.yaml" in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize(
    "content", ["[data]\nfoo = [\n", "[data]\nquestions_dir = 5\n"], ids=["toml", "tip"]
)
def test_broken_config_exit_code(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, content: str
) -> None:
    config = tmp_path / "codementor.toml"
    config.write_text(content, encoding="utf-8")
    monkeypatch.setenv(CONFIG_FILE_ENV, str(config))
    result = _invoke("list")
    assert result.exit_code == 3
    assert "yapılandırma okunamadı" in result.stderr
    assert "Traceback" not in result.output


def test_default_dir_from_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = tmp_path / "codementor.toml"
    config.write_text(f"[data]\nquestions_dir = '{QUESTIONS.as_posix()}'\n", encoding="utf-8")
    monkeypatch.setenv(CONFIG_FILE_ENV, str(config))
    code, out = _run("list")
    assert code == 0, out
    assert "c-hard-stack" in out


def test_show_reflows_prompt_lines() -> None:
    code, out = _run("show", "c-hard-stack", "--dir", str(QUESTIONS))
    assert code == 0, out
    assert "işlemlerini destekleyen, kapasitesi dolduğunda iki katına çıkan" in out


def test_validate_real_bank() -> None:
    code, out = _run("validate", "--dir", str(QUESTIONS))
    assert code == 0, out
    assert f"{len(QuestionBank.load(QUESTIONS))} soru geçerli" in out


def test_validate_reports_missing_distribution(tmp_path: Path) -> None:
    for name in ("c-hard-stack", "c-easy-reverse-string"):
        (tmp_path / f"{name}.yaml").write_bytes((QUESTIONS / f"{name}.yaml").read_bytes())
    code, out = _run("validate", "--dir", str(tmp_path), "--solutions-root", str(tmp_path))
    assert code == 1
    assert "c: 2 soru var, en az 8 olmalı" in out
    assert "very_easy, medium" in out


def test_validate_warns_missing_solution(tmp_path: Path) -> None:
    code, out = _run(
        "validate",
        "--dir",
        str(QUESTIONS),
        "--solutions-root",
        str(tmp_path),
        "--min-per-group",
        "1",
    )
    assert code == 0, out
    assert "uyarı" in out
    assert "c-hard-stack: referans çözüm okunamıyor: dosya yok" in out


def test_validate_empty_dir_fails(tmp_path: Path) -> None:
    code, out = _run("validate", "--dir", str(tmp_path))
    assert code == 1
    assert "Soru bankası boş" in out
