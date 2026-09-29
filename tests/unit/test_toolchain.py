"""Araç keşfi testleri: sahte `PATH` dizinindeki sahte çalıştırılabilirlerle."""

from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

import pytest

from codementor.config import ValidationSettings
from codementor.models.enums import Engine, Language
from codementor.validation.toolchain import clear_toolchain_cache, discover, get_toolchain

_EXE = ".exe" if sys.platform == "win32" else ""


def _fake_bin(directory: Path, *names: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    for name in names:
        exe = directory / f"{name}{_EXE}"
        exe.write_bytes(b"")
        exe.chmod(exe.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return directory


@pytest.fixture
def dll(tmp_path: Path) -> Path:
    path = tmp_path / "roslyn" / "RoslynCheck.dll"
    path.parent.mkdir()
    path.write_bytes(b"MZ")
    return path


def test_empty_path_finds_nothing(tmp_path: Path, dll: Path) -> None:
    chain = discover(str(_fake_bin(tmp_path / "bin")), dll)
    assert chain.summary() == {"c": None, "cpp": None, "unreal": None, "csharp": None}
    for language, engine in [
        (Language.C, Engine.NONE),
        (Language.CPP, Engine.NONE),
        (Language.CPP, Engine.UNREAL),
        (Language.CSHARP, Engine.UNITY),
    ]:
        assert chain.for_code(language, engine) is None


def test_fake_path_finds_gcc(tmp_path: Path, dll: Path) -> None:
    bin_dir = _fake_bin(tmp_path / "bin", "gcc", "g++")
    chain = discover(str(bin_dir), dll)
    assert chain.c is not None
    assert chain.cpp is not None
    assert chain.unreal is not None
    assert (chain.c.name, chain.c.kind) == ("gcc", "gcc")
    assert (chain.cpp.name, chain.cpp.kind) == ("g++", "gcc")
    assert Path(chain.c.command[0]).is_absolute()
    assert Path(chain.c.command[0]).parent == bin_dir
    assert chain.unreal.name == "g++"


def test_prefers_gcc_over_clang_for_plain_code(tmp_path: Path, dll: Path) -> None:
    first = _fake_bin(tmp_path / "a", "clang", "clang++")
    second = _fake_bin(tmp_path / "b", "gcc", "g++")
    chain = discover(os.pathsep.join([str(first), str(second)]), dll)
    assert chain.c is not None
    assert chain.c.name == "gcc"
    assert chain.cpp is not None
    assert chain.cpp.name == "g++"


def test_unreal_prefers_clang(tmp_path: Path, dll: Path) -> None:
    chain = discover(str(_fake_bin(tmp_path / "bin", "g++", "clang++")), dll)
    assert chain.unreal is not None
    assert (chain.unreal.name, chain.unreal.kind) == ("clang++", "clang")


def test_clang_only(tmp_path: Path, dll: Path) -> None:
    chain = discover(str(_fake_bin(tmp_path / "bin", "clang", "clang++")), dll)
    assert chain.c is not None
    assert chain.c.kind == "clang"
    assert chain.cpp is not None
    assert chain.cpp.name == "clang++"


def test_roslyn_needs_dotnet_and_dll(tmp_path: Path, dll: Path) -> None:
    with_dotnet = str(_fake_bin(tmp_path / "bin", "dotnet"))
    chain = discover(with_dotnet, dll)
    assert chain.csharp is not None
    assert chain.csharp.kind == "roslyn"
    assert chain.csharp.command[1:] == [str(dll.resolve())]
    assert chain.for_code(Language.CSHARP, Engine.UNITY) == chain.csharp

    assert discover(with_dotnet, tmp_path / "yok.dll").csharp is None
    assert discover(str(_fake_bin(tmp_path / "empty")), dll).csharp is None


def test_get_toolchain_is_cached(
    tmp_path: Path, dll: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(_fake_bin(tmp_path / "bin", "gcc")))
    settings = ValidationSettings(roslyn_check_dll=dll)
    clear_toolchain_cache()
    try:
        first = get_toolchain(settings)
        assert first.c is not None
        _fake_bin(tmp_path / "bin", "g++")
        assert get_toolchain(settings) is first  # önbellekten
        clear_toolchain_cache()
        assert get_toolchain(settings).cpp is not None
    finally:
        clear_toolchain_cache()


def test_discovery_never_raises_on_bad_path(dll: Path) -> None:
    chain = discover(os.pathsep.join(["", "\x00bad", "/nonexistent/dir"]), dll)
    assert chain.c is None
