from pathlib import Path

import pytest

from codementor.config import CONFIG_FILE_ENV, load_settings


@pytest.fixture
def toml_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "codementor.toml"
    path.write_text('[limits]\nmax_lines = 300\n\n[providers]\ndefault = "deepseek"\n')
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
    assert settings.providers.default == "deepseek"


@pytest.mark.usefixtures("toml_file")
def test_env_overrides_toml(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CODEMENTOR_LIMITS__MAX_LINES", "10")
    settings = load_settings()
    assert settings.limits.max_lines == 10
    # env yalnızca verilen alanı ezer, TOML'un geri kalanı korunur
    assert settings.providers.default == "deepseek"


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
