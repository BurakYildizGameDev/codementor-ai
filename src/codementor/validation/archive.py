"""İndirilen derleyici arşivini güvenle açma ve kurulum hataları (Faz 29, ADR-0018).

Yalnızca `prefix` altındaki üyeler, önek atılarak hedef dizine açılır. Reddedilenler: mutlak yol,
sürücü harfi, `..`, `\\`, `:` (NTFS akışı), sembolik bağlantı, Windows'un sessizce değiştirdiği
adlar (sonda nokta/boşluk), ayrılmış aygıt adları (`CON`, `NUL.h`, `COM1` …) ve büyük/küçük
harf duyarsız çakışan adlar. Açılan toplam boyut (bildirilen ve gerçekten yazılan) ve dosya sayısı
tavanlıdır (zip bombası).
"""

from __future__ import annotations

import threading
import zipfile
import zlib
from collections.abc import Callable
from pathlib import Path, PurePosixPath, PureWindowsPath

from codementor.models.validation import DownloadProgress

_MB = 1024 * 1024
_CHUNK = 64 * 1024
_SYMLINK = 0o120000
_RESERVED = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{i}" for i in range(10)}
    | {f"LPT{i}" for i in range(10)}
    | {"COM¹", "COM²", "COM³", "LPT¹", "LPT²", "LPT³"}
)

Progress = Callable[[DownloadProgress], None]


class ToolchainInstallError(Exception):
    """Kullanıcıya gösterilecek Türkçe kurulum hatası."""


class InstallCancelledError(ToolchainInstallError):
    """Kullanıcı kurulumu iptal etti."""

    def __init__(self) -> None:
        super().__init__("İndirme iptal edildi; yarım kalan dosyalar silindi.")


def check_cancel(cancel: threading.Event | None) -> None:
    """İptal istendiyse `InstallCancelledError`."""
    if cancel is not None and cancel.is_set():
        raise InstallCancelledError


def emit(progress: Progress | None, event: DownloadProgress) -> None:
    """İlerleme geri çağrısı varsa olayı iletir."""
    if progress is not None:
        progress(event)


def _unsafe(info: zipfile.ZipInfo, reason: str) -> ToolchainInstallError:
    return ToolchainInstallError(f"Arşiv güvenli değil: '{info.filename}' {reason}.")


def member_path(name: str, info: zipfile.ZipInfo) -> PurePosixPath:
    """Üye adını güvenli göreli yola çevirir; güvensizse `ToolchainInstallError`."""
    if (info.external_attr >> 16) & 0o170000 == _SYMLINK:
        raise _unsafe(info, "sembolik bağlantı içeriyor")
    windows = PureWindowsPath(name)
    posix = PurePosixPath(name)
    if (
        "\\" in name
        or ":" in name
        or "\x00" in name
        or windows.drive
        or windows.is_absolute()
        or posix.is_absolute()
        or ".." in posix.parts
    ):
        raise _unsafe(info, "izin verilmeyen yol")
    for part in posix.parts:
        if part != part.rstrip(". "):
            raise _unsafe(info, "noktayla ya da boşlukla biten ad")
        if part.split(".", 1)[0].upper() in _RESERVED:
            raise _unsafe(info, "ayrılmış aygıt adı")
    return posix


def safe_extract(
    archive: Path,
    dest: Path,
    *,
    prefix: str,
    max_bytes: int,
    max_files: int,
    progress: Progress | None = None,
    cancel: threading.Event | None = None,
) -> None:
    """Arşivin `prefix` altındaki üyelerini önek atılarak `dest`'e açar (bkz. modül notu)."""
    try:
        with zipfile.ZipFile(archive) as zf:
            members = [m for m in zf.infolist() if m.filename.startswith(prefix)]
            files = [m for m in members if not m.is_dir()]
            if not files:
                raise ToolchainInstallError("Arşivde beklenen derleyici dosyaları yok.")
            if len(files) > max_files:
                raise ToolchainInstallError(
                    f"Arşivde çok fazla dosya var (sınır {max_files}); açılmadı."
                )
            too_big = ToolchainInstallError(
                f"Arşivin açılmış hâli çok büyük (sınır {max_bytes // _MB} MB); açılmadı."
            )
            if sum(m.file_size for m in files) > max_bytes:
                raise too_big
            dest.mkdir(parents=True, exist_ok=True)
            root = dest.resolve()
            seen: set[str] = set()
            written = 0
            for index, info in enumerate(members):
                check_cancel(cancel)
                relative = info.filename[len(prefix) :]
                if not relative.strip("/"):
                    continue
                path = member_path(relative, info)
                folded = path.as_posix().rstrip("/").casefold()
                if not info.is_dir():
                    if folded in seen:  # Windows'ta aynı dosyaya düşer; sonuncu kazanırdı
                        raise _unsafe(info, "başka bir üyeyle aynı ada sahip")
                    seen.add(folded)
                target = dest.joinpath(*path.parts)
                if not target.resolve().is_relative_to(root):
                    raise _unsafe(info, "hedef dizinin dışına çıkıyor")
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(info) as source, target.open("wb") as sink:
                    while chunk := source.read(_CHUNK):
                        written += len(chunk)
                        if written > max_bytes:  # bildirilen boyut yalan olabilir
                            raise too_big
                        sink.write(chunk)
                if index % 500 == 0:
                    emit(
                        progress, DownloadProgress(stage="extract", done=index, total=len(members))
                    )
    except (
        zipfile.BadZipFile,
        zipfile.LargeZipFile,
        EOFError,
        zlib.error,
        NotImplementedError,  # desteklenmeyen sıkıştırma
        RuntimeError,  # şifreli üye
    ) as exc:
        raise ToolchainInstallError(
            "İndirilen arşiv açılamadı (bozuk ya da desteklenmeyen dosya)."
        ) from exc
