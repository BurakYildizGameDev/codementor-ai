"""Masaüstü çalışma ortamı: kaynak kökü, kullanıcı dizini, tercihler ve kaynak kod arşivi.

Yapılandırma yolları çalışma dizininden bağımsız çözülür (`codementor.paths`, ADR-0016).
Exe'de `data/` ve `prompts/` PyInstaller'ın açtığı `sys._MEIPASS` altındadır; kaynaktan
çalışırken depo köküdür. Çalışma dizini yine bu köke alınır (zararsız; dosya diyaloğu için).
"""

from __future__ import annotations

import contextlib
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, TextIO

from pydantic import ValidationError

from codementor import paths
from codementor.config import CONFIG_FILE_ENV, DEFAULT_CONFIG_FILE, config_file
from codementor.models.desktop import MAX_RECENT_FILES, DesktopPrefs

if TYPE_CHECKING:
    from codementor.desktop.app import App

PREFS_FILE = "desktop.json"
LOG_FILE = "desktop.log"
SOURCES_DIR = "desktop-sources"
LOG_MAX_BYTES = 5 * 1024 * 1024  # Faz 49: açılışta aşılmışsa `desktop.log.1` olur (tek yedek)


def is_frozen() -> bool:
    """PyInstaller paketinin içinden mi çalışıyoruz."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def resource_root() -> Path:
    """`data/`, `prompts/` ve varsayılan `codementor.toml`'un bulunduğu kök."""
    return paths.resource_root()


def user_dir() -> Path:
    """Kullanıcıya ait veriler (veritabanı ile aynı yer: `~/.codementor`)."""
    return Path.home() / ".codementor"


def is_installed_package() -> bool:
    """Wheel'den kurulu mu (kaynak kökü paketteki `_resources`): oraya yazılmaz (Faz C, O9)."""
    return not is_frozen() and resource_root().name == paths.RESOURCES_DIR


def _user_config_target() -> Path | None:
    """Paket verisi salt okunur/geçici olduğunda kullanıcının toml'u: exe'de exe'nin yanı, kurulu
    wheel'de `~/.codementor/codementor.toml`; depodan çalışırken None (depo kökündeki dosya)."""
    if is_frozen():
        return Path(sys.executable).resolve().parent / DEFAULT_CONFIG_FILE
    if is_installed_package():
        return user_dir() / DEFAULT_CONFIG_FILE
    return None


def user_config_file() -> Path | None:
    """Kullanıcının toml'u varsa (exe yanı ya da kurulu wheel'de `~/.codementor`) o dosya;
    paketteki varsayılanı geçersiz kılar."""
    target = _user_config_target()
    return target if target is not None and target.is_file() else None


def writable_config_file() -> Path:
    """Tercihlerin yazılacağı `codementor.toml` (Faz 24; Faz C, Y8/O9).

    Öncelik: `CODEMENTOR_CONFIG_FILE` → exe yanı / `~/.codementor` (yoksa paketteki varsayılan
    oraya kopyalanır, varsayılan ayarlar kaybolmasın) → depodan çalışırken etkin dosya. Seçilen
    yol `CODEMENTOR_CONFIG_FILE`'a yazılır: yeniden yükleme ve gösterilen konum aynı dosyadır.
    """
    if env := os.environ.get(CONFIG_FILE_ENV):
        return Path(env).absolute()
    target = _user_config_target()
    if target is None:
        target = config_file().absolute()
    else:
        bundled = resource_root() / DEFAULT_CONFIG_FILE
        if not target.is_file() and bundled.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(bundled, target)
    os.environ[CONFIG_FILE_ENV] = str(target)
    return target


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
    try:
        if path.stat().st_size > LOG_MAX_BYTES:
            os.replace(path, path.with_name(LOG_FILE + ".1"))
    except OSError:
        pass  # dosya yok ya da kilitli: eklemeye devam
    return path.open("a", encoding="utf-8", buffering=1)


def load_prefs(directory: Path | None = None) -> DesktopPrefs:
    """Tercihleri okur; dosya yoksa ya da bozuksa varsayılanlar."""
    path = (directory or user_dir()) / PREFS_FILE
    try:
        return DesktopPrefs.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValidationError):
        return DesktopPrefs()


def save_prefs(prefs: DesktopPrefs, directory: Path | None = None) -> None:
    """Tercihleri atomik yazar (geçici dosya + `os.replace`; yarıda kesilen yazım eski dosyayı
    bozmaz, Faz 49); yazılamazsa sessizce geçer (uygulama yine çalışır)."""
    path = (directory or user_dir()) / PREFS_FILE
    temp = path.with_name(f"{PREFS_FILE}.{os.getpid()}.tmp")  # iki örnek aynı dosyaya yazmasın
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp.write_text(prefs.model_dump_json(indent=2), encoding="utf-8")
        os.replace(temp, path)
    except OSError:
        with contextlib.suppress(OSError):
            temp.unlink(missing_ok=True)


def confirm_close(app: App) -> bool:
    """Kapanış onayları: kaydedilmemiş değişiklik ve süren iş (analiz/indirme) — Faz F (F5/F7)."""
    if app.files.is_dirty and not app.confirm(
        "Kaydedilmemiş değişiklik", "Değişiklikler kaybolacak. Devam edilsin mi?", parent=app
    ):
        return False
    busy = app.analyze_view.busy or app.connections.download_cancellation is not None
    if not busy:
        return True
    return app.confirm("Çıkış", "Analiz (ya da indirme) sürüyor. Çıkılsın mı?", parent=app)


def remember_file(prefs: DesktopPrefs, path: str) -> DesktopPrefs:
    """Son açılan dosyalar listesinin başına ekler (tekrarsız, en fazla `MAX_RECENT_FILES`)."""
    recent = [path, *(p for p in prefs.recent_files if p != path)][:MAX_RECENT_FILES]
    return prefs.model_copy(update={"recent_files": recent})


def forget_file(prefs: DesktopPrefs, path: str) -> DesktopPrefs:
    """Son dosyalar listesinden çıkarır (dosya silinmiş ya da taşınmış)."""
    return prefs.model_copy(update={"recent_files": [p for p in prefs.recent_files if p != path]})


def save_source(
    analysis_id: str, code: str, directory: Path | None = None, *, keep: int | None = None
) -> None:
    """Geçmişten açılabilsin diye analiz edilen kodu saklar (rapor kodu içermez); `keep`
    verilirse en yeni o kadar dosya kalır (Faz 49)."""
    folder = (directory or user_dir()) / SOURCES_DIR
    try:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{analysis_id}.txt").write_text(code, encoding="utf-8")
    except OSError:
        return
    prune_sources(keep, directory)


def prune_sources(keep: int | None, directory: Path | None = None) -> None:
    """Saklanan kodlardan en yeni `keep` tanesi kalır (analiz kayıt sınırıyla aynı, Faz 49)."""
    if keep is None:
        return
    folder = (directory or user_dir()) / SOURCES_DIR
    try:
        files = list(folder.glob("*.txt"))
    except OSError:
        return
    if len(files) <= keep:  # çoğu kayıtta stat taraması yok (Tk ana iş parçacığı)
        return
    dated: list[tuple[float, Path]] = []
    for path in files:
        with contextlib.suppress(OSError):  # başka örnek arada silmiş olabilir
            dated.append((path.stat().st_mtime, path))
    dated.sort(reverse=True)
    for _mtime, path in dated[keep:]:
        with contextlib.suppress(OSError):
            path.unlink(missing_ok=True)


def load_source(analysis_id: str, directory: Path | None = None) -> str | None:
    """Saklanan kod; yoksa None. Kimlik dosya adına girdiği için yalnızca ULID karakterleri."""
    if not analysis_id.isalnum():
        return None
    path = (directory or user_dir()) / SOURCES_DIR / f"{analysis_id}.txt"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def delete_source(analysis_id: str, directory: Path | None = None) -> bool:
    """Saklanan kodu siler (Faz 62). Kimlik yalnızca alfasayısal karakterler içerebilir."""
    if not analysis_id.isalnum():
        return False
    path = (directory or user_dir()) / SOURCES_DIR / f"{analysis_id}.txt"
    try:
        if path.is_file():
            path.unlink()
            return True
        return False
    except OSError:
        return False


def clear_sources(directory: Path | None = None) -> int:
    """Tüm saklanan kodları siler (Faz 62); silinen dosya sayısını döner."""
    folder = (directory or user_dir()) / SOURCES_DIR
    try:
        files = list(folder.glob("*.txt"))
    except OSError:
        return 0
    count = 0
    for path in files:
        with contextlib.suppress(OSError):
            path.unlink(missing_ok=True)
            count += 1
    return count


def backup_corrupted_db(db_path: Path | str) -> Path:
    """Bozuk SQLite dosyasını (varsa -wal ve -shm ile birlikte) `bozuk-YYYYAAGG-SSDDss` son
    ekiyle yeniden adlandırır.
    """
    p = Path(db_path)
    if str(p) == ":memory:" or not p.exists():
        return p
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = p.with_name(f"{p.name}.bozuk-{stamp}")
    p.rename(target)
    for ext in ("-wal", "-shm"):
        extra = p.with_name(p.name + ext)
        if extra.exists():
            with contextlib.suppress(OSError):
                extra.rename(target.with_name(target.name + ext))
    return target
