"""`test_toolchain_install.py` için ortak düzenek: sabitler, yardımcılar, fixture'lar."""

from __future__ import annotations

import hashlib
import io
import json
import os
import zipfile
from collections.abc import Iterator
from pathlib import Path

import httpx
import pytest

from codementor.config import DownloadSource, ValidationSettings, ZigSettings
from codementor.validation import toolchain_install
from codementor.validation.archive import safe_extract
from codementor.validation.toolchain_install import (
    INSTALL_MARKER,
    install_zig,
)

URL = "https://example.test/ziglang.whl"


PLATFORM = "linux-x86_64"


EXE = "zig.exe" if os.name == "nt" else "zig"


def _wheel(
    *, marker: bytes = b"v1", padding: int = 0, extra: dict[str, bytes] | None = None
) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        archive.writestr(f"ziglang/{EXE}", marker)
        archive.writestr("ziglang/lib/include/stdio.h", b"int printf(const char*, ...);\n")
        archive.writestr("ziglang/lib/big.bin", os.urandom(padding))
        archive.writestr("ziglang-0.16.0.dist-info/METADATA", b"Name: ziglang\n")
        for name, data in (extra or {}).items():
            archive.writestr(name, data)
    return buffer.getvalue()


def _settings(tmp_path: Path, payload: bytes, **zig: object) -> ValidationSettings:
    source = DownloadSource(url=URL, sha256=hashlib.sha256(payload).hexdigest())
    return ValidationSettings(
        toolchain_dir=tmp_path / "tc",
        zig=ZigSettings(version="0.16.0", sources={PLATFORM: source}, **zig),  # type: ignore[arg-type]
    )


def _install(settings: ValidationSettings, **kwargs: object) -> Path:
    return install_zig(settings, platform=PLATFORM, verify=lambda _exe: True, **kwargs)  # type: ignore[arg-type]


def _fake_install(settings: ValidationSettings, *, version: str, sha256: str) -> Path:
    """Elle kurulmuş gibi dizin + işaretçi (ağ yok)."""
    root = settings.toolchain_dir / "zig"
    root.mkdir(parents=True, exist_ok=True)
    exe = root / EXE
    exe.write_bytes(b"v1")
    marker = {"version": version, "sha256": sha256, "platform": PLATFORM}
    (root / INSTALL_MARKER).write_text(json.dumps(marker), encoding="utf-8")
    return exe


def _leftovers(settings: ValidationSettings) -> list[str]:
    root = settings.toolchain_dir
    return sorted(
        p.name for p in root.rglob("*") if p.name.endswith(".part") or p.name.startswith(".zig-")
    )


class _BrokenStream(httpx.SyncByteStream):
    """Bir parça gönderip bağlantıyı koparan akış (yarım indirme)."""

    def __init__(self, first: bytes) -> None:
        self.first = first

    def __iter__(self) -> Iterator[bytes]:
        yield self.first
        raise httpx.ReadError("bağlantı koptu")


# --- Arşiv güvenliği ---------------------------------------------------------------------


def _zip(tmp_path: Path, entries: list[zipfile.ZipInfo | tuple[str, bytes]]) -> Path:
    path = tmp_path / "a.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for entry in entries:
            if isinstance(entry, zipfile.ZipInfo):
                archive.writestr(entry, b"/etc/passwd")
            else:
                archive.writestr(*entry)
    return path


def _extract(archive: Path, dest: Path, **limits: int) -> None:
    safe_extract(
        archive,
        dest,
        prefix="ziglang/",
        max_bytes=limits.get("max_bytes", 10_000_000),
        max_files=limits.get("max_files", 100),
    )


# ------------------------------------------- Faz 58: Windows'ta geçici dizin kilidi


def _flaky_staging_rename(monkeypatch: pytest.MonkeyPatch, failures: int) -> list[int]:
    """Staging taşımasını `failures` kez WinError 5 benzeri hatayla düşürür (tarayıcı kilidi)."""
    real = Path.rename
    left = [failures]

    def rename(self: Path, target: str | os.PathLike[str]) -> Path:
        if self.name.startswith(".zig-staging-") and left[0]:
            left[0] -= 1
            raise PermissionError(13, "Erişim engellendi")
        return real(self, target)

    monkeypatch.setattr(Path, "rename", rename)
    monkeypatch.setattr(toolchain_install, "_RETRY_RENAME", True)
    monkeypatch.setattr(toolchain_install, "_RENAME_DELAYS_S", (0.0,) * 4)
    return left
