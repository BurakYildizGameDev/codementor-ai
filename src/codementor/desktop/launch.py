"""Giriş noktası: `codementor-desktop`, `python -m codementor.desktop`, CodeMentor.exe."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from tkinter import messagebox

from sqlalchemy.exc import DatabaseError as SQLAlchemyDatabaseError

from codementor.api.state import ApiState
from codementor.config import load_settings
from codementor.desktop import runtime
from codementor.desktop.app import App
from codementor.desktop.self_check import self_check
from codementor.storage.db import resolve_db_path

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
    try:
        state.database()  # veritabanı ana thread'de açılır; worker'lar paylaşır
    except (sqlite3.DatabaseError, SQLAlchemyDatabaseError, OSError) as exc:
        _close_splash()
        state.close()
        import gc

        gc.collect()
        short_err = str(exc).splitlines()[0] if str(exc) else exc.__class__.__name__
        answer = messagebox.askyesno(
            "CodeMentor AI",
            f"Veritabanı açılamadı ({short_err}).\n\n"
            "Bozuk dosya yedeklenip yeni, boş bir veritabanıyla başlansın mı? "
            "(Geçmiş analizler yedek dosyada kalır.)",
        )
        if not answer:
            raise SystemExit(3) from exc
        try:
            db_target = resolve_db_path(settings)
            runtime.backup_corrupted_db(db_target)
        except OSError as backup_exc:
            messagebox.showerror(
                "CodeMentor AI",
                f"Bozuk veritabanı dosyası yedeklenemedi (dosya kilitli olabilir):\n{backup_exc}",
            )
            raise SystemExit(3) from backup_exc
        state = ApiState(settings)
        try:
            state.database()
        except Exception as retry_exc:
            messagebox.showerror("CodeMentor AI", f"Yeni veritabanı oluşturulamadı:\n{retry_exc}")
            raise SystemExit(3) from retry_exc
    app = App(state)
    _close_splash()
    app.mainloop()
