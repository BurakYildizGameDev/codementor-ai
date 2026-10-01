"""Giriş noktası: `codementor-desktop`, `python -m codementor.desktop`, CodeMentor.exe."""

from __future__ import annotations

from tkinter import messagebox

from codementor.api.state import ApiState
from codementor.config import load_settings
from codementor.desktop import runtime
from codementor.desktop.app import App


def _close_splash() -> None:
    """PyInstaller açılış görseli (yalnızca exe'de vardır)."""
    # Doğrudan import şart: PyInstaller modülü statik analizle bulup pakete koyar
    try:
        import pyi_splash  # type: ignore[import-untyped,import-not-found,unused-ignore]
    except ImportError:
        return
    pyi_splash.close()


def main() -> None:
    """`codementor-desktop` / `python -m codementor.desktop` / CodeMentor.exe giriş noktası."""
    runtime.prepare_environment()
    try:
        settings = load_settings()
    except Exception as exc:
        _close_splash()
        messagebox.showerror("CodeMentor AI", f"Yapılandırma okunamadı:\n{exc}")
        raise SystemExit(3) from exc
    state = ApiState(settings)
    state.database()  # veritabanı ana thread'de açılır; worker'lar paylaşır
    app = App(state)
    _close_splash()
    app.mainloop()
