from pathlib import Path

import pytest

from codementor.config import CONFIG_FILE_ENV, load_settings


@pytest.fixture
def toml_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "codementor.toml"
    path.write_text('[limits]\nmax_lines = 300\n\n[providers]\ndefault = "gemini"\n')
    monkeypatch.setenv(CONFIG_FILE_ENV, str(path))
    monkeypatch.delenv("CODEMENTOR_LIMITS__MAX_LINES", raising=False)
    return path


def test_defaults_without_toml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(CONFIG_FILE_ENV, str(tmp_path / "yok.toml"))
    monkeypatch.delenv("CODEMENTOR_LIMITS__MAX_LINES", raising=False)
    settings = load_settings()
    assert settings.limits.max_lines == 600
    assert settings.pipeline.mode == "two_pass"


@pytest.mark.usefixtures("toml_file")
def test_toml_overrides_default() -> None:
    settings = load_settings()
    assert settings.limits.max_lines == 300
    assert settings.providers.default == "gemini"


@pytest.mark.usefixtures("toml_file")
def test_env_overrides_toml(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CODEMENTOR_LIMITS__MAX_LINES", "10")
    settings = load_settings()
    assert settings.limits.max_lines == 10
    # env yalnızca verilen alanı ezer, TOML'un geri kalanı korunur
    assert settings.providers.default == "gemini"


@pytest.mark.usefixtures("toml_file")
def test_cli_override_beats_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CODEMENTOR_LIMITS__MAX_LINES", "10")
    settings = load_settings(limits={"max_lines": 5})
    assert settings.limits.max_lines == 5


def test_rules_disabled_from_toml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "codementor.toml"
    path.write_text('[rules]\ndisabled = ["C-BUF-001", "UE-GC-001"]\n')
    monkeypatch.setenv(CONFIG_FILE_ENV, str(path))
    assert load_settings().rules.disabled == ["C-BUF-001", "UE-GC-001"]
    monkeypatch.setenv(CONFIG_FILE_ENV, str(tmp_path / "yok.toml"))
    assert load_settings().rules.disabled == []


def test_repo_config_default_provider_is_claude_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    """Hızlı başlangıç (README) claude_cli ile; Ollama isteğe bağlı alternatif (Faz 13)."""
    repo_toml = Path(__file__).resolve().parents[2] / "codementor.toml"
    monkeypatch.setenv(CONFIG_FILE_ENV, str(repo_toml))
    settings = load_settings()
    assert settings.providers.default == "claude_cli"
    assert settings.providers.fallback == []


# --- Yol çözümü (Faz 23, ADR-0016) ---------------------------------------------------------

REPO = Path(__file__).resolve().parents[2]


def _no_toml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(CONFIG_FILE_ENV, str(tmp_path / "yok.toml"))
    monkeypatch.delenv("CODEMENTOR_DATA__QUESTIONS_DIR", raising=False)


def test_default_paths_absolute_under_resource_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _no_toml(tmp_path, monkeypatch)
    settings = load_settings()
    assert settings.data.questions_dir == REPO / "data" / "questions"
    assert settings.prompts.dir == REPO / "prompts" / "v1"
    assert settings.validation.stub_header == REPO / "data" / "stubs" / "ue_stubs.h"
    assert settings.validation.roslyn_check_dll.is_absolute()
    assert settings.verify.common_identifiers_file.is_absolute()


def test_toml_relative_paths_resolve_against_toml_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_dir = tmp_path / "ayarlar"
    config_dir.mkdir()
    path = config_dir / "codementor.toml"
    path.write_text(
        '[data]\nquestions_dir = "sorular"\n\n[prompts]\ndir = "../istemler"\n'
        f'\n[validation]\nstub_header = "{(tmp_path / "s.h").as_posix()}"\n',
        encoding="utf-8",
    )
    monkeypatch.setenv(CONFIG_FILE_ENV, str(path))
    monkeypatch.delenv("CODEMENTOR_DATA__QUESTIONS_DIR", raising=False)
    settings = load_settings()
    assert settings.data.questions_dir == config_dir / "sorular"
    assert settings.prompts.dir == config_dir / ".." / "istemler"
    assert settings.validation.stub_header == tmp_path / "s.h"
    # toml'da verilmeyen alan varsayılan kökte kalır
    assert settings.data.checklists_dir == REPO / "data" / "checklists"


def test_env_relative_path_stays_cwd_relative(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _no_toml(tmp_path, monkeypatch)
    monkeypatch.setenv("CODEMENTOR_DATA__QUESTIONS_DIR", "benim/sorular")
    assert load_settings().data.questions_dir == Path("benim/sorular")


def test_settings_work_from_foreign_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Proje dışından çalıştırınca veri, şablon ve stub bulunur."""
    from codementor.desktop.connections import model_suggestions
    from codementor.prompts.templates import prompt_version
    from codementor.questions import Checklists, QuestionBank

    _no_toml(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    settings = load_settings()
    assert len(QuestionBank.load(settings.data.questions_dir)) > 0
    Checklists.load(settings.data.checklists_dir)
    assert prompt_version(settings.prompts.dir)
    assert settings.validation.stub_header.is_file()
    assert settings.data.call_costs_file.is_file()
    assert settings.data.mentor_templates_file.is_file()
    assert settings.verify.common_identifiers_file.is_file()
    assert "claude_cli" in model_suggestions()
