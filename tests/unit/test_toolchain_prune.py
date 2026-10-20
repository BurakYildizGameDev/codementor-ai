"""Zig libc başlık budama testleri (Faz J, J2)."""

from __future__ import annotations

from pathlib import Path

from codementor.validation.toolchain_prune import _is_unrelated_target, prune_zig_directory
from tools import prune_zig


def test_is_unrelated_target_linux() -> None:
    # Linux x86_64
    assert _is_unrelated_target("any-windows-any", "linux", "x86_64")
    assert _is_unrelated_target("x86_64-windows-gnu", "linux", "x86_64")
    assert _is_unrelated_target("riscv64-linux-gnu", "linux", "x86_64")
    assert _is_unrelated_target("mips", "linux", "x86_64")
    assert _is_unrelated_target("darwin", "linux", "x86_64")

    # Kept for Linux x86_64
    assert not _is_unrelated_target("x86_64-linux-gnu", "linux", "x86_64")
    assert not _is_unrelated_target("x86_64-linux-musl", "linux", "x86_64")
    assert not _is_unrelated_target("generic-glibc", "linux", "x86_64")


def test_is_unrelated_target_windows() -> None:
    # Windows x86_64
    assert _is_unrelated_target("darwin", "windows", "x86_64")
    assert _is_unrelated_target("wasi", "windows", "x86_64")
    assert _is_unrelated_target("arm-linux-gnu", "windows", "x86_64")

    # Kept for Windows x86_64
    assert not _is_unrelated_target("any-windows-any", "windows", "x86_64")
    assert not _is_unrelated_target("x86_64-windows-gnu", "windows", "x86_64")


def test_prune_zig_directory_dry_run(tmp_path: Path) -> None:
    libc_inc = tmp_path / "lib" / "libc" / "include"
    libc_inc.mkdir(parents=True)

    # create kept directory
    kept = libc_inc / "x86_64-linux-gnu"
    kept.mkdir()
    (kept / "stdio.h").write_text("// stdio", encoding="utf-8")

    # create prunable directory
    prunable = libc_inc / "mips-linux-gnu"
    prunable.mkdir()
    (prunable / "stdio.h").write_text("// mips stdio", encoding="utf-8")

    report = prune_zig_directory(tmp_path, platform="linux-x86_64", dry_run=True)
    assert report.dry_run is True
    assert len(report.removed_dirs) == 1
    assert report.removed_files_count == 1
    assert prunable.exists()  # dry run should not delete


def test_prune_zig_directory_execution(tmp_path: Path) -> None:
    libc = tmp_path / "lib" / "libc"
    include = libc / "include"
    include.mkdir(parents=True)
    darwin = libc / "darwin"
    darwin.mkdir(parents=True)
    (darwin / "header.h").write_text("// macos", encoding="utf-8")

    musl_arch = libc / "musl" / "arch"
    musl_arch.mkdir(parents=True)
    mips_arch = musl_arch / "mips"
    mips_arch.mkdir()
    (mips_arch / "syscall.h").write_text("// syscall", encoding="utf-8")

    x86_arch = musl_arch / "x86_64"
    x86_arch.mkdir()
    (x86_arch / "syscall.h").write_text("// syscall", encoding="utf-8")

    report = prune_zig_directory(tmp_path, platform="linux-x86_64", dry_run=False)
    assert report.dry_run is False
    assert len(report.removed_dirs) == 2  # darwin and mips arch
    assert not darwin.exists()
    assert not mips_arch.exists()
    assert x86_arch.exists()


def test_tools_prune_zig_cli(tmp_path: Path) -> None:
    libc = tmp_path / "lib" / "libc" / "include"
    libc.mkdir(parents=True)
    (libc / "wasi").mkdir()
    (libc / "wasi" / "wasi.h").write_text("// wasi", encoding="utf-8")

    rc = prune_zig.main([str(tmp_path), "--dry-run", "--platform=linux-x86_64"])
    assert rc == 0
