"""Giriş noktası: `codementor-desktop`, `python -m codementor.desktop`, CodeMentor.exe."""

from __future__ import annotations

import sys
from pathlib import Path
from tkinter import messagebox

from codementor.api.state import ApiState
from codementor.config import load_settings
from codementor.desktop import runtime
from codementor.desktop.app import App
from codementor.desktop.self_check import self_check

SELF_CHECK_FLAG = "--self-check"


def _close_splash() -> None:
    """PyInstaller açılış görseli (yalnızca exe'de vardır)."""
    # Doğrudan import şart: PyInstaller modülü statik analizle bulup pakete koyar
    try:
        import pyi_splash  # type: ignore[import-untyped,import-not-found,unused-ignore]
    except Exception:  # yok (kaynaktan) ya da açılış görseline bağlanılamadı (konsoldan açılış)
        return
    pyi_splash.close()


def main() -> None:
    """`codementor-desktop` / `python -m codementor.desktop` / CodeMentor.exe giriş noktası.

    `--self-check <sonuc.json>`: pencere açmadan paket duman testi (Faz D, release iş akışı).
    """
    if len(sys.argv) >= 2 and sys.argv[1] == SELF_CHECK_FLAG:
        _close_splash()
        # göreli yol, çalışma dizini kaynak köküne alınmadan önce mutlaklaştırılır
        target = Path(sys.argv[2] if len(sys.argv) >= 3 else "self-check.json").absolute()
        runtime.prepare_environment()
        raise SystemExit(self_check(target))
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
