"""Dosya işlemleri (Faz 24): aç, son dosyalar ve sürükle-bırak.

Sürükle-bırak `tkinterdnd2` (tkdnd) ile; kütüphane ya da yerel eklenti yüklenemezse özellik
sessizce kapanır, uygulamanın geri kalanı etkilenmez.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any

from codementor.desktop import runtime
from codementor.desktop.viewmodel import SOURCE_PATTERNS, language_for_path
from codementor.ingest.errors import InvalidEncodingError
from codementor.ingest.normalize import decode_source
from codementor.log import get_logger
from codementor.models.desktop import DesktopPrefs
from codementor.models.enums import Engine

if TYPE_CHECKING:
    from codementor.desktop.app import App

log = get_logger("codementor.desktop")

MAX_LABEL = 70
MAX_FOLDER_FILES = 50  # bırakılan klasörde menüye en fazla bu kadar dosya (Faz 33)


def parse_drop_data(data: str) -> list[str]:
    """tkdnd'nin Tcl listesi biçimindeki yolları: boşluklu yollar `{...}` içindedir."""
    paths: list[str] = []
    index, size = 0, len(data)
    while index < size:
        if data[index].isspace():
            index += 1
            continue
        if data[index] == "{":
            end = data.find("}", index + 1)
            end = size if end == -1 else end
            paths.append(data[index + 1 : end])
            index = end + 1
        else:
            end = index
            while end < size and not data[end].isspace():
                end += 1
            paths.append(data[index:end])
            index = end
    return [p for p in paths if p]


def folder_sources(folder: Path, limit: int = MAX_FOLDER_FILES) -> list[str]:
    """Klasördeki (alt klasörler hariç) tanınan dildeki kaynak dosyaları, ada göre sıralı."""
    try:
        entries = sorted(folder.iterdir(), key=lambda p: p.name.lower())
    except OSError:
        return []
    found = [str(p) for p in entries if p.is_file() and language_for_path(p) is not None]
    return found[:limit]


def recent_label(path: str) -> str:
    """Menü metni: `ad  —  klasör` (uzun klasör baştan kısaltılır)."""
    folder, _, name = path.replace("\\", "/").rpartition("/")
    room = MAX_LABEL - len(name) - 5
    if len(folder) > room:
        folder = "…" + folder[-(room - 1) :] if room > 1 else "…"
    return f"{name}  —  {folder}" if folder else name


class FileController:
    """Ana pencerenin dosya işlemleri; tercihler ve bildirimler `App` üzerinden."""

    def __init__(self, app: App) -> None:
        self.app = app
        self.drop_enabled = False

    def open_dialog(self) -> None:
        from tkinter import filedialog  # Tk'siz Python'da modül yine içe aktarılabilsin (CI)

        path = filedialog.askopenfilename(
            title="Kaynak dosyası aç",
            filetypes=[("Kaynak dosyaları", SOURCE_PATTERNS), ("Tüm dosyalar", "*.*")],
        )
        if path:
            self.load(path)

    def recent(self) -> list[str]:
        return list(self.app.prefs.recent_files)

    def open_recent(self, path: str) -> None:
        """Son dosyalardan açar; dosya artık yoksa listeden düşer."""
        if not Path(path).is_file():
            self._update_prefs(runtime.forget_file(self.app.prefs, path))
            self.app.toast(f"{Path(path).name} artık yok; listeden kaldırıldı.")
            return
        self.load(path)

    def load(self, path: str) -> None:
        app, limit = self.app, self.app.settings.limits.max_bytes
        try:
            size = os.path.getsize(path)
            if size > limit:
                app.toast(f"Dosya çok büyük ({size // 1024} KB); sınır {limit // 1024} KB.")
                return
            # metin kipindeki gibi satır sonları `\n` (editör ve analiz aynı kodu görür)
            code = decode_source(Path(path).read_bytes()).replace("\r\n", "\n").replace("\r", "\n")
        except OSError as exc:
            app.toast(f"Dosya okunamadı: {exc.strerror or exc}")
            return
        except InvalidEncodingError as exc:  # U+FFFD'li kod editöre düşmesin (Faz 50)
            app.toast(f"{Path(path).name}: {exc}")
            return
        view = app.analyze_view
        language = language_for_path(path) or view.language
        if language is not view.language:
            view.select(language, Engine.NONE, view.question.id if view.question else None)
        view.editor.set(code, language)
        view.reset_results()
        self._update_prefs(runtime.remember_file(app.prefs, path))
        app.toast(f"{Path(path).name} açıldı")

    def on_drop(self, data: str) -> None:
        """Bırakılan ilk dosyayı açar; klasörse içindeki kaynak dosyalarını seçtirir (Faz 33)."""
        dropped = parse_drop_data(data)
        paths = [p for p in dropped if Path(p).is_file()]
        if not paths:
            folder = next((Path(p) for p in dropped if Path(p).is_dir()), None)
            if folder is not None:
                self._offer_folder(folder)
            else:
                self.app.toast("Bırakılan öğe bir dosya değil.")
            return
        self.load(paths[0])
        if len(paths) > 1:
            self.app.toast(f"{Path(paths[0]).name} açıldı; aynı anda tek dosya açılır.")

    def _offer_folder(self, folder: Path) -> None:
        sources = folder_sources(folder)
        if not sources:
            self.app.toast(f"{folder.name} klasöründe tanınan kaynak dosya yok.")
            return
        if len(sources) == 1:
            self.load(sources[0])
            return
        items: list[tuple[str, Callable[[], None]]] = [
            (recent_label(p), partial(self.load, p)) for p in sources
        ]
        self.app.analyze_view.show_file_menu(items)

    def enable_drop(self, widget: Any) -> bool:
        """`widget`'ı dosya bırakma hedefi yapar; tkdnd yoksa False."""
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD

            TkinterDnD._require(self.app)
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>", self._drop_event)
        except Exception as exc:  # ImportError, TclError (eklenti yok), mimari uyumsuzluğu
            log.warning("drag_drop_unavailable", error=type(exc).__name__)
            return False
        self.drop_enabled = True
        return True

    def _drop_event(self, event: Any) -> str:
        self.on_drop(str(getattr(event, "data", "")))
        return str(getattr(event, "action", "copy"))

    def _update_prefs(self, prefs: DesktopPrefs) -> None:
        self.app.prefs = prefs
        runtime.save_prefs(prefs, self.app.prefs_dir)
