"""Oturum açma (F12): platform başına argv, terminal yoksa Türkçe yönlendirme.

Hiçbir test gerçek süreç başlatmaz: `find` ve `spawn` sahte geçirilir (AGENTS.md kural 4 ve 7).
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from codementor.config import ProvidersSettings, Settings
from codementor.desktop.login import (
    LoginUnavailableError,
    login_argv,
    login_command,
    login_env,
    manual_login_hint,
    open_login_console,
)

# Var olan mutlak bir çalıştırılabilir (CLI yerine; çalıştırılmaz). `resolve_executable` sembolik
# bağlantıyı çözer: Linux venv'inde `.venv/bin/python` → `/usr/bin/python3.x`.
EXE = str(Path(sys.executable).resolve())
CLI = "/usr/local/bin/claude"
LOGIN_ARGS = ("auth", "login")


def cli_providers(settings: Settings) -> ProvidersSettings:
    """CLI komutlarını var olan mutlak bir dosyaya çevirir (test makinesinde kurulu olmasın)."""
    return settings.providers.model_copy(
        update={
            name: getattr(settings.providers, name).model_copy(update={"command": EXE})
            for name in ("claude_cli", "codex", "agy")
        }
    )


def finder(*available: str) -> Callable[[str], str | None]:
    """Yalnız verilen araçları 'bulur' — makinede kurulu olup olmadığından bağımsız test."""
    found = {name: f"/usr/bin/{name}" for name in available}
    return found.get


class FakeSpawn:
    """`subprocess.Popen` yerine geçer: süreç başlatmaz, çağrıyı kaydeder."""

    def __init__(self) -> None:
        self.calls: list[tuple[list[str], dict[str, Any]]] = []

    def __call__(self, argv: list[str], **kwargs: Any) -> None:
        self.calls.append((list(argv), kwargs))


# --- Sağlayıcı komutu --------------------------------------------------------------------------


def test_login_argv_per_provider(settings: Settings) -> None:
    providers = cli_providers(settings)
    assert login_argv("claude_cli", providers)[1:] == ["auth", "login"]
    assert login_argv("codex", providers)[1:] == ["login"]
    assert login_argv("agy", providers)[1:] == []
    assert Path(login_argv("agy", providers)[0]).is_absolute()


# --- Platforma göre komut (saf fonksiyon) ------------------------------------------------------


def test_windows_login_command_keeps_current_behaviour() -> None:
    """Windows: CLI doğrudan yeni konsolda başlar; terminal aranmaz."""
    calls: list[str] = []

    def find(name: str) -> str | None:
        calls.append(name)
        return None

    assert login_command("win32", CLI, login_args=LOGIN_ARGS, find=find) == [CLI, *LOGIN_ARGS]
    assert calls == []


def test_linux_login_command_prefers_x_terminal_emulator() -> None:
    argv = login_command(
        "linux", CLI, login_args=LOGIN_ARGS, find=finder("x-terminal-emulator", "gnome-terminal")
    )
    assert argv == ["/usr/bin/x-terminal-emulator", "-e", CLI, *LOGIN_ARGS]


def test_linux_login_command_falls_back_to_gnome_terminal() -> None:
    argv = login_command("linux", CLI, login_args=LOGIN_ARGS, find=finder("gnome-terminal"))
    assert argv == ["/usr/bin/gnome-terminal", "--", CLI, *LOGIN_ARGS]


def test_macos_login_command_opens_terminal_app() -> None:
    argv = login_command("darwin", CLI, login_args=LOGIN_ARGS, find=finder("open"))
    assert argv == ["/usr/bin/open", "-a", "Terminal", CLI]


def test_login_command_is_none_when_no_terminal_tool_exists() -> None:
    """Araç yoksa liste değil `None` döner; çağıran kullanıcıya komutu söyler (F12)."""
    assert login_command("linux", CLI, login_args=LOGIN_ARGS, find=finder()) is None
    assert login_command("darwin", CLI, login_args=LOGIN_ARGS, find=finder()) is None


# --- Pencerenin başlatılması ------------------------------------------------------------------


def test_windows_login_spawns_new_console(settings: Settings) -> None:
    spawn = FakeSpawn()
    open_login_console("claude_cli", cli_providers(settings), platform="win32", spawn=spawn)
    (argv, kwargs) = spawn.calls[0]
    assert argv == [EXE, "auth", "login"]
    assert kwargs["creationflags"] == getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    assert kwargs["cwd"] == Path.home()
    assert kwargs["close_fds"] is True


def test_linux_login_spawns_terminal_without_windows_flags(settings: Settings) -> None:
    spawn = FakeSpawn()
    open_login_console(
        "codex",
        cli_providers(settings),
        platform="linux",
        find=finder("x-terminal-emulator"),
        spawn=spawn,
    )
    (argv, kwargs) = spawn.calls[0]
    assert argv == ["/usr/bin/x-terminal-emulator", "-e", EXE, "login"]
    assert "creationflags" not in kwargs  # POSIX'te geçersiz argüman olurdu


def test_default_spawn_is_subprocess_popen(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Varsayılan başlatıcı gerçek `subprocess.Popen`'dır; testte sahtesiyle değiştirilir."""
    seen: list[list[str]] = []

    def fake(argv: list[str], **_: Any) -> None:
        seen.append(list(argv))

    monkeypatch.setattr(subprocess, "Popen", fake)
    open_login_console("claude_cli", cli_providers(settings), platform="win32")
    assert seen == [[EXE, "auth", "login"]]


def test_no_terminal_raises_with_manual_command_and_spawns_nothing(settings: Settings) -> None:
    """F12: terminal yoksa süreç başlatılmaz; kullanıcıya çalıştıracağı komut söylenir."""
    spawn = FakeSpawn()
    with pytest.raises(LoginUnavailableError) as info:
        open_login_console(
            "claude_cli", cli_providers(settings), platform="linux", find=finder(), spawn=spawn
        )
    assert spawn.calls == []
    assert info.value.provider == "claude_cli"
    assert str(info.value) == f"claude_cli: {manual_login_hint([EXE, 'auth', 'login'])}"


def test_manual_login_hint_quotes_paths_with_spaces() -> None:
    hint = manual_login_hint(["/opt/Claude Code/claude", "auth", "login"])
    assert hint == "Terminalde şu komutu çalıştırın: '/opt/Claude Code/claude' auth login"


# --- Ortam ------------------------------------------------------------------------------------


def test_login_env_strips_api_keys(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    """Faz 50: oturum açma konsolu API anahtarlarını miras almaz (yalnız CLI'nin kendi girişi)."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-gizli")
    monkeypatch.setenv("GEMINI_API_KEY", "gizli")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-gizli")
    monkeypatch.setenv("CODEMENTOR_TEST_OZEL_ANAHTAR", "gizli")
    monkeypatch.setenv("PATH_DISINDA_KALAN", "kalir")
    providers = settings.providers.model_copy(
        update={
            "ollama": settings.providers.ollama.model_copy(
                update={"api_key_env": "CODEMENTOR_TEST_OZEL_ANAHTAR"}
            )
        }
    )
    env = login_env(providers)
    for name in (
        "ANTHROPIC_API_KEY",
        "GEMINI_API_KEY",
        "OPENAI_API_KEY",
        "CODEMENTOR_TEST_OZEL_ANAHTAR",
    ):
        assert name not in env
    assert env["PATH_DISINDA_KALAN"] == "kalir"
    assert "PATH" in env or "Path" in env
