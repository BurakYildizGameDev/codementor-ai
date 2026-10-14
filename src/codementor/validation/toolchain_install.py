"""İndirilebilir derleyici kurulumu (Faz 29, ADR-0018).

Derleyicisi olmayan kullanıcı için zig, `toolchain_dir/zig` altına indirilir. Kurallar (§12):

- Adres ve sha256 yalnızca yapılandırmadan gelir; yalnızca https (her yönlendirme adımında).
- Aynı anda tek kurulum: `toolchain_dir/.install.lock` üzerinde işletim sistemi kilidi (süreç
  ölünce bırakılır). Artık temizliği yalnızca kilit alındıktan sonra yapılır.
- İndirme benzersiz bir `downloads/*.part` dosyasına yapılır; sha256 akış sırasında hesaplanır
  ve açmadan önce diskteki dosyadan yeniden doğrulanır; boyut tavanlıdır. Hata, iptal ya da
  uyuşmazlıkta `.part` silinir.
- Arşiv güvenle açılır (`validation.archive`). Açılan zig C ve C++ için sondalanır; tamamlanma
  işareti staging'e yazılır, son iptal denetiminden sonra staging atomik olarak yerine taşınır.
  İşaretsiz dizin kurulu sayılmaz (yarım kurulum).
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import shutil
import stat
import sys
import threading
import time
import uuid
from collections.abc import Callable, Iterator
from pathlib import Path

import httpx

from codementor.config import DownloadSource, ValidationSettings
from codementor.log import get_logger
from codementor.models.validation import DownloadProgress
from codementor.validation.archive import InstallCancelledError as InstallCancelledError
from codementor.validation.archive import Progress, check_cancel, emit, safe_extract
from codementor.validation.archive import ToolchainInstallError as ToolchainInstallError
from codementor.validation.zig import probe_flags, zig_executable

INSTALL_MARKER = ".codementor-install.json"
ARCHIVE_PREFIX = "ziglang/"
LOCK_FILE = ".install.lock"
_MB = 1024 * 1024
_CHUNK = 64 * 1024
_PROGRESS_STEP = 512 * 1024  # bu kadar baytta bir ilerleme olayı
# Windows'ta virüs tarayıcısı/indeksleyici yeni açılan `zig.exe`'yi kısa süre açık tutar; o
# sırada dizin taşıma WinError 5/32 (PermissionError) verir (Faz 58). Geçici kilit kısa
# aralıklarla yeniden denenir (en fazla ~3 sn); kalıcı hata yine Türkçe mesajla döner.
_RETRY_RENAME = os.name == "nt"
_RENAME_DELAYS_S = (0.05, 0.1, 0.2, 0.4, 0.8, 1.6)

Verify = Callable[[Path], bool]

log = get_logger("codementor.toolchain")

_SYSTEMS = {"windows": "windows", "linux": "linux", "darwin": "macos"}
_MACHINES = {"amd64": "x86_64", "x86_64": "x86_64", "arm64": "aarch64", "aarch64": "aarch64"}


def platform_key(system: str | None = None, machine: str | None = None) -> str:
    """`ZigSettings.sources` anahtarı: `windows-x86_64`, `linux-aarch64`, `macos-aarch64` …"""
    raw_system = (system or platform.system()).lower()
    raw_machine = (machine or platform.machine()).lower()
    return f"{_SYSTEMS.get(raw_system, raw_system)}-{_MACHINES.get(raw_machine, raw_machine)}"


def zig_root(toolchain_dir: Path) -> Path:
    """İndirilen zig'in kök dizini."""
    return toolchain_dir / "zig"


def installed_zig(root: Path) -> Path | None:
    """Tamamlanmış kurulumdaki zig çalıştırılabiliri; yoksa ya da yarımsa `None`."""
    try:
        if not (root / INSTALL_MARKER).is_file():
            return None
        exe = zig_executable(root)
        return exe if exe.is_file() else None
    except OSError:
        return None


def installed_marker(root: Path) -> dict[str, object] | None:
    """Kurulum işaretçisinin içeriği (`version`, `sha256`, `platform`); yoksa/bozuksa `None`."""
    try:
        data: object = json.loads((root / INSTALL_MARKER).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def needs_update(settings: ValidationSettings, *, platform: str | None = None) -> bool:
    """Kurulu zig, yapılandırmadaki sürüm/kaynaktan farklı mı (Faz F, F9).

    Kurulum yoksa, işaretçi okunamıyorsa ya da bu platform için kaynak tanımlı değilse
    `False`: o durumda güncelleme değil, kurulum eksikliği söz konusudur.
    """
    root = zig_root(settings.toolchain_dir)
    if installed_zig(root) is None:
        return False
    marker = installed_marker(root)
    source = settings.zig.sources.get(platform or platform_key())
    if marker is None or source is None:
        return False
    return marker.get("version") != settings.zig.version or marker.get("sha256") != source.sha256


def _https_only(request: httpx.Request) -> None:
    if request.url.scheme != "https":
        raise ToolchainInstallError("İndirme https olmayan bir adrese yönlendirildi; durduruldu.")


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(_CHUNK * 16):
            digest.update(chunk)
    return digest.hexdigest()


@contextlib.contextmanager
def _install_lock(root: Path) -> Iterator[None]:
    """Aynı `toolchain_dir`'e eşzamanlı kurulumu engeller (süreçler arası, çökmede bırakılır)."""
    handle = (root / LOCK_FILE).open("a+b")
    try:
        try:
            if sys.platform == "win32":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise ToolchainInstallError(
                "Başka bir derleyici kurulumu sürüyor; bitmesini bekleyip yeniden dene."
            ) from exc
        try:
            yield
        finally:
            if sys.platform == "win32":
                import msvcrt

                with contextlib.suppress(OSError):
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    finally:
        handle.close()


def _download(
    source: DownloadSource,
    target: Path,
    *,
    max_bytes: int,
    timeout_s: float,
    progress: Progress | None,
    cancel: threading.Event | None,
) -> None:
    """`source`'u `target`'a indirir ve sha256'yı doğrular; başarısızlıkta `target` silinir."""
    limit_text = f"{max_bytes // _MB} MB"
    digest = hashlib.sha256()
    try:
        with (
            httpx.Client(
                follow_redirects=True,
                timeout=timeout_s,
                event_hooks={"request": [_https_only]},  # her yönlendirme adımı denetlenir
            ) as client,
            client.stream("GET", source.url) as response,
        ):
            if response.status_code != 200:
                raise ToolchainInstallError(
                    f"İndirme başarısız oldu (HTTP {response.status_code})."
                )
            length = response.headers.get("content-length")
            total = int(length) if length and length.isdigit() else None
            if total is not None and total > max_bytes:
                raise ToolchainInstallError(
                    f"İndirilecek dosya izin verilen boyuttan büyük (sınır {limit_text})."
                )
            done = reported = 0
            emit(progress, DownloadProgress(stage="download", done=0, total=total))
            with target.open("wb") as handle:
                for chunk in response.iter_bytes(_CHUNK):
                    check_cancel(cancel)
                    done += len(chunk)
                    if done > max_bytes:
                        raise ToolchainInstallError(
                            f"İndirilen dosya izin verilen boyutu aştı (sınır {limit_text})."
                        )
                    digest.update(chunk)
                    handle.write(chunk)
                    if done - reported >= _PROGRESS_STEP:
                        reported = done
                        emit(progress, DownloadProgress(stage="download", done=done, total=total))
            check_cancel(cancel)
            emit(progress, DownloadProgress(stage="download", done=done, total=total))
    except httpx.HTTPError as exc:
        target.unlink(missing_ok=True)
        raise ToolchainInstallError(
            f"İndirme yarıda kaldı ({type(exc).__name__}). İnternet bağlantını denetleyip "
            "yeniden dene."
        ) from exc
    except BaseException:
        target.unlink(missing_ok=True)
        raise
    if digest.hexdigest() != source.sha256:
        target.unlink(missing_ok=True)
        raise ToolchainInstallError(
            "İndirilen dosya doğrulanamadı (sha256 uyuşmuyor); dosya silindi."
        )


def _make_executable(path: Path) -> None:
    if os.name != "nt":
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _rename(source: Path, target: Path) -> None:
    """`source.rename(target)`; Windows'taki geçici dosya kilidinde kısa beklemelerle yineler."""
    for delay in _RENAME_DELAYS_S if _RETRY_RENAME else ():
        try:
            source.rename(target)
            return
        except PermissionError:
            time.sleep(delay)
    source.rename(target)


def _replace(staging: Path, final: Path) -> None:
    """Staging'i `final`'ın yerine taşır; eski kurulum en son silinir."""
    old: Path | None = None
    if final.exists():
        old = final.with_name(f".zig-old-{uuid.uuid4().hex[:8]}")
        try:
            _rename(final, old)
        except OSError as exc:
            raise ToolchainInstallError(
                "Kurulu derleyici şu an kullanımda; uygulamayı yeniden başlatıp tekrar dene."
            ) from exc
    try:
        _rename(staging, final)
    except OSError as exc:
        if old is not None:
            with contextlib.suppress(OSError):
                _rename(old, final)
        raise ToolchainInstallError("Derleyici kurulum dizinine taşınamadı.") from exc
    if old is not None:
        shutil.rmtree(old, ignore_errors=True)


def _clean_leftovers(toolchain_dir: Path) -> None:
    """Önceki çökmüş kurulumların artıkları (kilit altında çağrılır).

    İki taşıma arasında çökülmüşse tek geçerli kurulum `.zig-old-*` olarak kalmıştır: silinmez,
    yerine geri taşınır.
    """
    final = zig_root(toolchain_dir)
    olds = sorted(toolchain_dir.glob(".zig-old-*"), key=lambda p: p.stat().st_mtime)
    if not final.exists():
        for old in reversed(olds):
            if installed_zig(old) is not None:
                # Geri taşınamasa da silinmez: tek geçerli kurulum odur (Faz 58 denetimi)
                olds.remove(old)
                with contextlib.suppress(OSError):
                    _rename(old, final)
                break
    for path in [*toolchain_dir.glob(".zig-staging-*"), *olds]:
        shutil.rmtree(path, ignore_errors=True)
    for part in (toolchain_dir / "downloads").glob("*.part"):
        with contextlib.suppress(OSError):
            part.unlink()


def install_zig(
    settings: ValidationSettings,
    *,
    progress: Progress | None = None,
    cancel: threading.Event | None = None,
    platform: str | None = None,
    verify: Verify | None = None,
) -> Path:
    """Zig'i indirir, doğrular ve `toolchain_dir/zig`'e kurar; kurulan çalıştırılabiliri döndürür.

    Hata durumunda Türkçe `ToolchainInstallError`; iptalde `InstallCancelledError`. Önceki
    kurulum, yenisi tamamen hazır olana kadar yerinde kalır.
    """
    zig = settings.zig
    key = platform or platform_key()
    source = zig.sources.get(key)
    if source is None:
        raise ToolchainInstallError(
            f"Bu platform ({key}) için indirilebilir derleyici tanımlı değil. "
            "gcc/clang kurabilir ya da yapılandırmaya kaynak ekleyebilirsin."
        )
    root = settings.toolchain_dir
    try:
        (root / "downloads").mkdir(parents=True, exist_ok=True)
        with _install_lock(root):
            return _install_locked(settings, source, key, progress, cancel, verify)
    except OSError as exc:
        raise ToolchainInstallError(
            f"Derleyici kurulamadı (dosya hatası: {exc.strerror or exc})."
        ) from exc


def _probe_both(exe: Path, timeout_s: float) -> bool:
    """Keşif C ve C++ bayraklarının ikisini de ister; kurulum da ikisini sondalar."""
    return all(
        probe_flags(str(exe), language, timeout_s=timeout_s) is not None
        for language in ("c", "c++")
    )


def _install_locked(
    settings: ValidationSettings,
    source: DownloadSource,
    key: str,
    progress: Progress | None,
    cancel: threading.Event | None,
    verify: Verify | None,
) -> Path:
    zig = settings.zig
    root = settings.toolchain_dir
    _clean_leftovers(root)
    unique = uuid.uuid4().hex[:8]
    archive = root / "downloads" / f"zig-{source.sha256[:16]}-{unique}.part"
    staging = root / f".zig-staging-{unique}"
    check = verify or (lambda exe: _probe_both(exe, zig.probe_timeout_s))
    try:
        _download(
            source,
            archive,
            max_bytes=zig.max_download_mb * _MB,
            timeout_s=zig.download_timeout_s,
            progress=progress,
            cancel=cancel,
        )
        if _file_sha256(archive) != source.sha256:  # akışta doğrulanan dosya değişmemiş olmalı
            raise ToolchainInstallError("İndirilen dosya diskte değişmiş; kurulum durduruldu.")
        safe_extract(
            archive,
            staging,
            prefix=ARCHIVE_PREFIX,
            max_bytes=zig.max_extract_mb * _MB,
            max_files=zig.max_files,
            progress=progress,
            cancel=cancel,
        )
        archive.unlink(missing_ok=True)
        exe = zig_executable(staging)
        if not exe.is_file():
            raise ToolchainInstallError("Arşivde zig çalıştırılabiliri bulunamadı.")
        _make_executable(exe)
        check_cancel(cancel)
        emit(progress, DownloadProgress(stage="check", done=0, total=1))
        if not check(exe):
            raise ToolchainInstallError(
                "Derleyici indirildi ama bu bilgisayarda çalıştırılamadı; kurulum geri alındı."
            )
        marker = {"version": zig.version, "sha256": source.sha256, "platform": key}
        (staging / INSTALL_MARKER).write_text(json.dumps(marker), encoding="utf-8")
        check_cancel(cancel)  # son nokta: bundan sonra kurulum tamamlanır
        final = zig_root(root)
        _replace(staging, final)
        emit(progress, DownloadProgress(stage="check", done=1, total=1))
    except OSError as exc:
        raise ToolchainInstallError(
            f"Derleyici kurulamadı (dosya hatası: {exc.strerror or exc})."
        ) from exc
    finally:
        archive.unlink(missing_ok=True)
        shutil.rmtree(staging, ignore_errors=True)
    log.info("toolchain_installed", tool="zig", version=zig.version, platform=key)
    return zig_executable(final)
