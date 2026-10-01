"""Masaüstü çalışma ortamı: kaynak kökü, kullanıcı dizini, tercihler ve kaynak kod arşivi.

Yapılandırmadaki göreli yollar (`data/`, `prompts/`, `tools/`) çalışma dizinine göredir
(`config.DataSettings`). Exe'de bu dosyalar PyInstaller'ın açtığı `sys._MEIPASS` altındadır;
kaynaktan çalışırken depo köküdür. Uygulama açılırken çalışma dizini bu köke alınır.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TextIO

from pydantic import ValidationError

from codementor.config import CONFIG_FILE_ENV, DEFAULT_CONFIG_FILE
from codementor.models.desktop import MAX_RECENT_FILES, DesktopPrefs

PREFS_FILE = "desktop.json"
LOG_FILE = "desktop.log"
SOURCES_DIR = "desktop-sources"


def is_frozen() -> bool:
    """PyInstaller paketinin içinden mi çalışıyoruz."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def resource_root() -> Path:
    """`data/`, `prompts/` ve varsayılan `codementor.toml`'un bulunduğu kök."""
    if is_frozen():
        bundle: str = sys._MEIPASS  # type: ignore[attr-defined]
        return Path(bundle)
    # src/codementor/desktop/runtime.py → depo kökü
    return Path(__file__).resolve().parents[3]


def user_dir() -> Path:
    """Kullanıcıya ait veriler (veritabanı ile aynı yer: `~/.codementor`)."""
    return Path.home() / ".codementor"


def user_config_file() -> Path | None:
    """Exe'nin yanına konan `codementor.toml` paketteki varsayılanı geçersiz kılar."""
    if not is_frozen():
        return None
    candidate = Path(sys.executable).resolve().parent / DEFAULT_CONFIG_FILE
    return candidate if candidate.is_file() else None


def prepare_environment() -> Path:
    """Çalışma dizinini kaynak köküne alır; pencereli exe'de çıktıyı log dosyasına yönlendirir."""
    root = resource_root()
    override = user_config_file()
    if override is not None and CONFIG_FILE_ENV not in os.environ:
        os.environ[CONFIG_FILE_ENV] = str(override)
    os.chdir(root)
    if sys.stdout is None or sys.stderr is None:  # --windowed: konsol yok
        stream = _log_stream()
        sys.stdout = sys.stdout or stream
        sys.stderr = sys.stderr or stream
    return root


def _log_stream() -> TextIO:
    path = user_dir() / LOG_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    return path.open("a", encoding="utf-8", buffering=1)


def load_prefs(directory: Path | None = None) -> DesktopPrefs:
    """Tercihleri okur; dosya yoksa ya da bozuksa varsayılanlar."""
    path = (directory or user_dir()) / PREFS_FILE
    try:
        return DesktopPrefs.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValidationError):
        return DesktopPrefs()


def save_prefs(prefs: DesktopPrefs, directory: Path | None = None) -> None:
    """Tercihleri yazar; yazılamazsa sessizce geçer (uygulama yine çalışır)."""
    path = (directory or user_dir()) / PREFS_FILE
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(prefs.model_dump_json(indent=2), encoding="utf-8")
    except OSError:
        pass


def remember_file(prefs: DesktopPrefs, path: str) -> DesktopPrefs:
    """Son açılan dosyalar listesinin başına ekler (tekrarsız, en fazla `MAX_RECENT_FILES`)."""
    recent = [path, *(p for p in prefs.recent_files if p != path)][:MAX_RECENT_FILES]
    return prefs.model_copy(update={"recent_files": recent})


def save_source(analysis_id: str, code: str, directory: Path | None = None) -> None:
    """Geçmişten açılabilsin diye analiz edilen kodu saklar (rapor kodu içermez)."""
    folder = (directory or user_dir()) / SOURCES_DIR
    try:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{analysis_id}.txt").write_text(code, encoding="utf-8")
    except OSError:
        pass


def load_source(analysis_id: str, directory: Path | None = None) -> str | None:
    """Saklanan kod; yoksa None. Kimlik dosya adına girdiği için yalnızca ULID karakterleri."""
    if not analysis_id.isalnum():
        return None
    path = (directory or user_dir()) / SOURCES_DIR / f"{analysis_id}.txt"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None
