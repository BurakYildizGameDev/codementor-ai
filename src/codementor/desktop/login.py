"""Oturum açma penceresi (F12): sağlayıcı CLI'sini etkileşimli bir terminalde başlatır.

Windows'ta mevcut davranış korunur (yeni konsol penceresi, `CREATE_NEW_CONSOLE`). Linux ve
macOS'ta komut sistemin terminal öykünücüsüne devredilir; hiçbiri bulunamazsa hiçbir süreç
başlatılmaz, `LoginUnavailableError` yükseltilir ve arayüz kullanıcıya elle çalıştıracağı
komutu gösterir (sessizce hiçbir şey yapmamak kullanıcıyı çıkmazda bırakırdı).

Kullanıcı kodu güvenilmez veridir (mimari §12): argv her zaman liste olarak geçer, kabuk
kullanılmaz (`shell=True` yok); çalıştırılabilir yol `resolve_executable` ile PATH'in mutlak
dizinlerinden gelir. Oturum konsolu API anahtarı değişkenlerini miras almaz (Faz 50).

Bu modül GUI'ye dokunmaz ve Tk içe aktarmaz; saf `login_command` argv üretir, `open_login_console`
süreci `spawn` parametresiyle başlatır (testler sahte geçirir, gerçek süreç çalışmaz).
"""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from codementor.config import ProvidersSettings
from codementor.providers.base import ProviderError
from codementor.providers.cli_agent import resolve_executable
from codementor.validation.runner import find_on_path

__all__ = [
    "LoginUnavailableError",
    "login_argv",
    "login_command",
    "login_env",
    "manual_login_hint",
    "open_login_console",
]

# Linux'ta sırayla denenen terminal öykünücüleri ve komut ayırıcıları (F12).
_TERMINALS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("x-terminal-emulator", ("-e",)),
    ("gnome-terminal", ("--",)),
)

#: PATH'te bir aracı arayan fonksiyon: ad → mutlak yol ya da bulunamadıysa `None`.
Finder = Callable[[str], str | None]
#: Süreç başlatıcı (`subprocess.Popen` yerine testler sahte geçirir).
Spawn = Callable[..., Any]


class LoginUnavailableError(ProviderError):
    """Oturum açma pencere olarak başlatılamadı; kullanıcı komutu elle çalıştırmalı (F12)."""


def _default_finder(name: str) -> str | None:
    """Terminal aracını PATH'in mutlak dizinlerinde arar (Faz A2: çalışma dizinine bakılmaz)."""
    found = find_on_path(name, os.environ.get("PATH", ""))
    return str(found) if found is not None else None


def login_argv(name: str, providers: ProvidersSettings) -> list[str]:
    """Sağlayıcının oturum açma komutu (mutlak yol); `claude_cli` → `… auth login`."""
    executable = resolve_executable(name, getattr(providers, name).command)
    if name == "claude_cli":
        return [executable, "auth", "login"]
    return [executable, "login"] if name == "codex" else [executable]


def login_command(
    platform: str,
    cli_path: str,
    *,
    login_args: Sequence[str] = ("login",),
    find: Finder = _default_finder,
) -> list[str] | None:
    """Platforma göre oturum açma penceresinin argv'si; terminal bulunamazsa `None` (F12).

    Windows: CLI doğrudan yeni konsolda başlatılır (mevcut davranış, `CREATE_NEW_CONSOLE`).
    Linux: `x-terminal-emulator -e <cli> …`, yoksa `gnome-terminal -- <cli> …`.
    macOS: `open -a Terminal <cli>` — Terminal uygulaması ek argümanları belge yolu saydığı için
    `open` ile yalnız çalıştırılabilir yol geçirilir; CLI argümansız da kendi oturum açma akışını
    başlatır. Hiç süreç başlatılmaz, yalnız argv üretilir.
    """
    if platform.startswith("win"):
        return [cli_path, *login_args]
    if platform == "darwin":
        opener = find("open")
        return [opener, "-a", "Terminal", cli_path] if opener else None
    for name, separator in _TERMINALS:
        terminal = find(name)
        if terminal:
            return [terminal, *separator, cli_path, *login_args]
    return None


def manual_login_hint(argv: Sequence[str]) -> str:
    """Terminal bulunamadığında kullanıcıya gösterilen Türkçe komut ipucu (F12)."""
    return f"Terminalde şu komutu çalıştırın: {shlex.join(argv)}"


def open_login_console(
    name: str,
    providers: ProvidersSettings,
    *,
    platform: str = sys.platform,
    find: Finder = _default_finder,
    spawn: Spawn | None = None,
) -> None:
    """Oturum açma komutunu etkileşimli bir pencerede başlatır (F12).

    Windows'ta yeni konsol, Linux/macOS'ta sistem terminali kullanılır. Uygun terminal yoksa
    hiçbir süreç başlatılmaz ve `LoginUnavailableError` yükseltilir; arayüz kullanıcıya elle
    çalıştıracağı komutu bildirir. Süreç yalnız `spawn` ile başlatılır (varsayılan
    `subprocess.Popen`).
    """
    argv = login_argv(name, providers)
    window = login_command(platform, argv[0], login_args=argv[1:], find=find)
    if window is None:
        raise LoginUnavailableError(name, manual_login_hint(argv))
    kwargs: dict[str, Any] = {
        "cwd": Path.home(),
        "close_fds": True,
        "env": login_env(providers),
    }
    if platform.startswith("win"):
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    (spawn or subprocess.Popen)(window, **kwargs)


def login_env(providers: ProvidersSettings) -> dict[str, str]:
    """Oturum konsolunun ortamı: API anahtarı değişkenleri çıkarılır (Faz 50). Konsol
    etkileşimlidir ve kasadan yüklenen anahtarlar süreç ortamındadır; CLI yalnız kendi
    girişini kullanmalı, kullanıcı konsolda anahtarı da görmemeli."""
    configured = {
        str(env_name)
        for config in providers.model_dump().values()
        if isinstance(config, dict) and (env_name := config.get("api_key_env"))
    }
    return {
        key: value
        for key, value in os.environ.items()
        if key not in configured and not key.upper().endswith("_API_KEY")
    }
