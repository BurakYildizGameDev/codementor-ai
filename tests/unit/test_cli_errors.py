"""CLI sistem hatalarının kullanıcıya dönük metni (Faz C, Y9/O12; ağ hataları: Faz G6)."""

from __future__ import annotations

import pytest
import typer
from rich.console import Console

from codementor.cli.errors import EXIT_SYSTEM_ERROR, describe, system_errors


def test_file_error_names_file_operation() -> None:
    """G6 öncesi davranış korunur: dosya hataları `ağ hatası` diye anılmaz."""
    exc = FileNotFoundError(2, "No such file or directory", "veri.json")
    assert describe(exc) == "dosya işlemi başarısız (veri.json): No such file or directory"


def test_connection_refused_names_network() -> None:
    """Ağ hatası `OSError` alt sınıfıdır ama kullanıcıya dosya hatası gibi gösterilmez."""
    exc = ConnectionRefusedError(10061, "Bağlantı reddedildi", "api.ornek.com")
    assert describe(exc) == "ağ hatası (api.ornek.com): Bağlantı reddedildi"


def test_timeout_without_detail_uses_default_phrase() -> None:
    """Ayrıntısız zaman aşımında da boş mesaj yerine okunur bir cümle çıkar."""
    assert describe(TimeoutError()) == "ağ hatası: bağlantı kurulamadı ya da zaman aşımı"


def test_timeout_detail_is_shown() -> None:
    assert describe(TimeoutError("30 sn sonra vazgeçildi")) == "ağ hatası: 30 sn sonra vazgeçildi"


def test_system_errors_exits_three_with_network_message() -> None:
    """Sarmalayıcı (`system_errors`) ağ hatasını traceback'siz, çıkış 3 ile bildirir."""
    console = Console(record=True, width=120, force_terminal=False)
    with pytest.raises(typer.Exit) as info, system_errors(console, "analiz"):
        raise ConnectionResetError(104, "Bağlantı kesildi")
    assert info.value.exit_code == EXIT_SYSTEM_ERROR
    text = console.export_text()
    assert "analiz: ağ hatası: Bağlantı kesildi" in text
    assert "dosya işlemi" not in text
