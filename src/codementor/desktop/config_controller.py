"""Yapılandırma denetleyicisi — Faz F (F0) bölmesi (`app.py`'den).

Konumları listeleme, tercihleri kaydetme ve yapılandırmayı yeniden yükleme.
Tkinter/CustomTkinter en üstte içe aktarılmaz; Linux CI'da tkinter'sız içe aktarılabilir.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from codementor.config import config_file, load_settings
from codementor.desktop import runtime
from codementor.desktop.config_writer import write_provider_prefs
from codementor.storage.db import resolve_db_path

if TYPE_CHECKING:
    from codementor.desktop.app import App


def open_folder(path: str) -> None:
    """Verilen yol bir dizinse onu, dosyaysa üst dizinini sistem gezgininde açar."""
    target = Path(path)
    folder = target if target.is_dir() else target.parent
    if sys.platform == "win32" and folder.is_dir():
        os.startfile(folder)


def provider_name(app: App) -> str:
    """Aktif sağlayıcı adı (tercih yoksa varsayılan)."""
    return app.prefs.provider or app.settings.providers.default


def base_default(app: App) -> str:
    """`codementor.toml`'daki varsayılan sağlayıcı."""
    return app.base_settings.providers.default


def current_model(app: App) -> str:
    """Aktif sağlayıcının modeli."""
    config = getattr(app.settings.providers, provider_name(app), None)
    return str(config.model) if config is not None else ""


def apply_settings(app: App) -> None:
    """Arayüz seçimlerini (model, adres) ayarlara uygular; sonraki analizler bunu kullanır."""
    from codementor.desktop.connections import apply_overrides

    app.settings = apply_overrides(app.base_settings, app.prefs)
    app.core.settings = app.settings
    app.tracker.slow_hint_s = app.settings.pipeline.slow_llm_hint_s


def locations(app: App) -> list[tuple[str, str]]:
    """Uygulamanın kullandığı dosya ve dizin konumlarını listeler."""
    # Faz C (Y8): okunan dosyanın kendisi (exe'de geçici paket dizini değil)
    return [
        ("Yapılandırma", str(config_file().resolve())),
        ("Veritabanı", str(resolve_db_path(app.settings))),
        ("Kullanıcı verisi", str(runtime.user_dir())),
    ]


def write_config(app: App) -> None:
    """Model ve varsayılan sağlayıcı seçimlerini `codementor.toml`'a işler (anahtar hariç)."""
    try:
        path = write_provider_prefs(runtime.writable_config_file(), app.prefs)
    except (OSError, ValueError) as exc:  # salt okunur konum, bozuk toml
        app.toast(f"codementor.toml yazılamadı: {exc}")
        return
    app.toast(f"Seçimler yazıldı: {path}")


def reload_config(app: App) -> None:
    """`codementor.toml`'u (ve ortamı) yeniden okur; arayüz seçimleri yine üstüne uygulanır.

    Bozuk dosya uygulanmaz. Veritabanı yolu gibi açılışta kurulanlar yeniden başlatma ister.
    """
    try:
        base = load_settings()
    except Exception as exc:  # bozuk toml, geçersiz değer, okunamayan dosya
        app.toast(f"codementor.toml okunamadı: {exc}")
        return
    app.base_settings = base
    app.apply_settings()
    app.connections.refresh_all()
    app.toast("codementor.toml yeniden yüklendi")
