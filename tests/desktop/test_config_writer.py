"""Masaüstü tercihlerini `codementor.toml`'a yazma (Faz 24)."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

import pytest

from codementor.config import CONFIG_FILE_ENV, load_settings
from codementor.desktop import runtime
from codementor.desktop.config_writer import write_provider_prefs
from codementor.models.desktop import DesktopPrefs, ProviderOverride

ORIGINAL = """# Kullanıcının yorumu
[limits]
max_lines = 300   # satır sonu yorumu

[providers]
default = "ollama"
fallback = []

[providers.ollama]
model = "eski-model"   # korunmalı mı? değer değişir, yorum kalır
num_ctx = 8192
"""

PREFS = DesktopPrefs(
    provider="claude_cli",
    providers={
        "ollama": ProviderOverride(model="qwen2.5-coder:14b", base_url="http://pc:11434"),
        "agy": ProviderOverride(allow_tool_agent=True),
        "claude_cli": ProviderOverride(),
    },
)


def test_writes_default_and_models_preserving_comments(tmp_path: Path) -> None:
    path = tmp_path / "codementor.toml"
    path.write_text(ORIGINAL, encoding="utf-8")
    write_provider_prefs(path, PREFS)
    text = path.read_text(encoding="utf-8")
    assert "# Kullanıcının yorumu" in text
    assert "# satır sonu yorumu" in text
    data = tomllib.loads(text)
    assert data["limits"]["max_lines"] == 300
    assert data["providers"]["default"] == "claude_cli"
    assert data["providers"]["ollama"] == {
        "model": "qwen2.5-coder:14b",
        "num_ctx": 8192,
        "base_url": "http://pc:11434",
    }
    assert data["providers"]["agy"] == {"allow_tool_agent": True}
    assert "claude_cli" not in data["providers"]  # boş geçersiz kılma bölüm açmaz


def test_never_writes_api_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-gizli-anahtar")
    path = tmp_path / "codementor.toml"
    write_provider_prefs(path, PREFS.model_copy(update={"provider": "anthropic"}))
    text = path.read_text(encoding="utf-8")
    assert "sk-ant" not in text
    written = {
        key
        for section in tomllib.loads(text)["providers"].values()
        if isinstance(section, dict)
        for key in section
    }
    assert written <= {"model", "base_url", "allow_tool_agent"}


def test_written_toml_round_trips_through_load_settings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "codementor.toml"
    path.write_text(ORIGINAL, encoding="utf-8")
    write_provider_prefs(path, PREFS)
    monkeypatch.setenv(CONFIG_FILE_ENV, str(path))
    settings = load_settings()  # CLI/API aynı modeli görür
    assert settings.providers.default == "claude_cli"
    assert settings.providers.ollama.model == "qwen2.5-coder:14b"
    assert settings.providers.ollama.base_url == "http://pc:11434"
    assert settings.providers.agy.allow_tool_agent is True


def test_frozen_copies_bundled_toml_next_to_exe(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    bundle, install = tmp_path / "bundle", tmp_path / "install"
    bundle.mkdir()
    install.mkdir()
    (bundle / "codementor.toml").write_text(ORIGINAL, encoding="utf-8")
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(bundle), raising=False)
    monkeypatch.setattr(sys, "executable", str(install / "CodeMentor.exe"))
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)

    target = runtime.writable_config_file()
    assert target == install / "codementor.toml"
    assert target.read_text(encoding="utf-8") == ORIGINAL  # paketteki varsayılanlar korunur
    (install / "codementor.toml").write_text("[limits]\nmax_lines = 5\n", encoding="utf-8")
    assert runtime.writable_config_file().read_text(encoding="utf-8").endswith("= 5\n")


def test_source_run_targets_active_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    active = tmp_path / "etkin.toml"
    monkeypatch.setenv(CONFIG_FILE_ENV, str(active))
    assert runtime.writable_config_file() == active
