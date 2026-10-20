"""İndirilen Zig araç zinciri için libc başlıklarını budama (Faz J, J2 spec).

Zig varsayılan olarak tüm işletim sistemleri ve mimariler için libc ve musl/glibc
başlıklarını barındırır (~382 MB). Yerel derleme (Tier 1) için yalnızca yerel platformun
ve mimarinin başlıkları gereklidir; diğerleri (mips, riscv, s390x, wasi, darwin vb.)
güvenle budanabilir (hedef: <150 MB).
"""

from __future__ import annotations

import contextlib
import os
import shutil
from pathlib import Path

from codementor.log import get_logger
from codementor.models.validation import PruneReport
from codementor.validation.toolchain_install import platform_key

log = get_logger("codementor.toolchain.prune")

# Yabancı mimariler (mevcut mimari x86_64 iken budanabilecekler)
FOREIGN_ARCHS = frozenset(
    {
        "aarch64",
        "arm",
        "arm64",
        "i386",
        "mips",
        "mips64",
        "powerpc",
        "powerpc64",
        "riscv64",
        "s390x",
        "sparc",
    }
)


def _is_unrelated_target(name: str, target_os: str, target_arch: str) -> bool:
    """Klasör adının geçerli işletim sistemi veya mimariyle ilgisiz olup olmadığını belirler."""
    lower = name.lower()

    # İşletim sistemi uyuşmazlığı
    if target_os == "linux" and any(
        os_tag in lower for os_tag in ("windows", "mingw", "darwin", "apple", "wasi", "haiku")
    ):
        return True
    if target_os == "windows":
        if any(os_tag in lower for os_tag in ("darwin", "apple", "wasi", "haiku")):
            return True
        if "linux" in lower and "x86_64" not in lower:
            return True
    elif target_os == "macos" and any(
        os_tag in lower for os_tag in ("windows", "mingw", "haiku", "wasi")
    ):
        return True

    # Mimari uyuşmazlığı
    for foreign in FOREIGN_ARCHS:
        if foreign == target_arch:
            continue
        if lower.startswith(f"{foreign}-") or lower.startswith(f"{foreign}_") or lower == foreign:
            return True

    return False


def prune_zig_directory(
    zig_root: Path,
    platform: str | None = None,
    *,
    dry_run: bool = False,
) -> PruneReport:
    """Belirtilen Zig kurulum dizinindeki gereksiz libc hedeflerini temizler."""
    key = platform or platform_key()
    parts = key.split("-")
    target_os = parts[0] if len(parts) > 0 else "linux"
    target_arch = parts[1] if len(parts) > 1 else "x86_64"

    libc_dir = zig_root / "lib" / "libc"
    removed_dirs: list[str] = []
    failed_dirs: list[str] = []
    removed_files = 0
    reclaimed_bytes = 0

    if not libc_dir.is_dir():
        return PruneReport(
            removed_dirs=[],
            removed_files_count=0,
            reclaimed_bytes=0,
            dry_run=dry_run,
        )

    # include ve musl/arch dizinlerini tara
    candidates: list[Path] = []
    include_dir = libc_dir / "include"
    if include_dir.is_dir():
        for entry in include_dir.iterdir():
            if entry.is_dir() and _is_unrelated_target(entry.name, target_os, target_arch):
                candidates.append(entry)

    musl_arch = libc_dir / "musl" / "arch"
    if musl_arch.is_dir():
        for entry in musl_arch.iterdir():
            if entry.is_dir() and _is_unrelated_target(entry.name, target_os, target_arch):
                candidates.append(entry)

    darwin_dir = libc_dir / "darwin"
    if target_os != "macos" and darwin_dir.is_dir():
        candidates.append(darwin_dir)

    wasi_dir = libc_dir / "wasi"
    if wasi_dir.is_dir():
        candidates.append(wasi_dir)

    for cand in candidates:
        rel = str(cand.relative_to(zig_root)).replace("\\", "/")
        f_count = 0
        b_count = 0
        for root, _, files in os.walk(cand):
            f_count += len(files)
            for f in files:
                with contextlib.suppress(OSError):
                    b_count += (Path(root) / f).stat().st_size

        if not dry_run:
            shutil.rmtree(cand, ignore_errors=True)
            if cand.exists():  # kilitli dosya ya da izin: silinmeyeni "kaldırıldı" sayma
                failed_dirs.append(rel)
                continue

        removed_dirs.append(rel)
        removed_files += f_count
        reclaimed_bytes += b_count

    log.info(
        "zig_pruned",
        platform=key,
        dirs_removed=len(removed_dirs),
        dirs_failed=len(failed_dirs),
        files_removed=removed_files,
        bytes_reclaimed=reclaimed_bytes,
        dry_run=dry_run,
    )

    return PruneReport(
        removed_dirs=removed_dirs,
        removed_files_count=removed_files,
        reclaimed_bytes=reclaimed_bytes,
        dry_run=dry_run,
        failed_dirs=failed_dirs,
    )
