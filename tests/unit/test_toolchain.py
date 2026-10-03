"""Araç keşfi testleri: sahte `PATH` dizinindeki sahte çalıştırılabilirlerle."""

from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

import pytest

from codementor.config import ValidationSettings
from codementor.models.enums import Engine, Language
from codementor.models.validation import Toolchain
from codementor.validation import toolchain as toolchain_module
from codementor.validation.toolchain import (
    clear_toolchain_cache,
    compiler_statuses,
    discover,
    get_toolchain,
)
from codementor.validation.toolchain_install import INSTALL_MARKER
from codementor.validation.zig import ZigLanguage

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


# --- Faz 29: zig ve self-contained Roslyn ------------------------------------------------

_ZIG_FLAGS = ["--target=x86_64-unknown-linux-gnu", "-nostdinc", "-isystem", "/z/lib/include"]


class _Prober:
    """Sahte bayrak sondası: çağrılan zig yollarını kaydeder."""

    def __init__(self, flags: list[str] | None = _ZIG_FLAGS) -> None:
        self.flags = flags
        self.calls: list[tuple[str, str]] = []

    def __call__(self, zig: str, language: ZigLanguage, *, timeout_s: float) -> list[str] | None:
        self.calls.append((zig, language))
        return None if self.flags is None else [*self.flags, f"-D__LANG__={language}"]


def _install_zig(toolchain_dir: Path, *, complete: bool = True) -> Path:
    root = toolchain_dir / "zig"
    _fake_bin(root, "zig")
    if complete:
        (root / INSTALL_MARKER).write_text('{"version": "0.16.0"}', encoding="utf-8")
    return root / f"zig{_EXE}"


def test_path_compilers_preferred_over_downloaded_zig(tmp_path: Path, dll: Path) -> None:
    _install_zig(tmp_path / "tc")
    prober = _Prober()
    chain = discover(
        str(_fake_bin(tmp_path / "bin", "gcc", "g++")),
        dll,
        toolchain_dir=tmp_path / "tc",
        prober=prober,
    )
    assert chain.c is not None
    assert chain.c.name == "gcc"
    assert chain.c.origin == "system"
    assert chain.unreal is not None
    assert chain.unreal.name == "g++"
    assert prober.calls == []  # gerek yokken zig sondası çalışmaz


def test_downloaded_zig_fills_missing_targets(tmp_path: Path, dll: Path) -> None:
    zig = _install_zig(tmp_path / "tc")
    chain = discover(
        str(_fake_bin(tmp_path / "bin")), dll, toolchain_dir=tmp_path / "tc", prober=_Prober()
    )
    assert chain.c is not None
    assert chain.cpp is not None
    assert chain.unreal is not None
    assert (chain.c.name, chain.c.kind, chain.c.origin) == ("zig", "clang", "downloaded")
    assert chain.c.command[:2] == [str(zig.resolve()), "clang"]
    assert "-D__LANG__=c" in chain.c.command
    assert "-D__LANG__=c++" in chain.cpp.command
    assert chain.unreal.command == chain.cpp.command


def test_zig_tool_uses_clang_passthrough(tmp_path: Path, dll: Path) -> None:
    """`zig cc` stdin'i diske yazar; yalnız `zig clang` + sondadan gelen bayraklar kullanılır."""
    _install_zig(tmp_path / "tc")
    chain = discover(
        str(_fake_bin(tmp_path / "bin")), dll, toolchain_dir=tmp_path / "tc", prober=_Prober()
    )
    assert chain.cpp is not None
    assert chain.cpp.command[1] == "clang"
    assert "cc" not in chain.cpp.command
    assert "c++" not in chain.cpp.command
    assert chain.cpp.command[2:4] == ["--target=x86_64-unknown-linux-gnu", "-nostdinc"]


def test_path_zig_before_downloaded_when_path_first(tmp_path: Path, dll: Path) -> None:
    _install_zig(tmp_path / "tc")
    bin_dir = _fake_bin(tmp_path / "bin", "zig")
    chain = discover(str(bin_dir), dll, toolchain_dir=tmp_path / "tc", prober=_Prober())
    assert chain.c is not None
    assert chain.c.origin == "system"
    assert Path(chain.c.command[0]).parent == bin_dir


def test_bundled_first_priority(tmp_path: Path, dll: Path) -> None:
    _install_zig(tmp_path / "tc")
    exe = _fake_bin(tmp_path / "sc", "RoslynCheck") / f"RoslynCheck{_EXE}"
    chain = discover(
        str(_fake_bin(tmp_path / "bin", "gcc", "g++", "clang++", "zig", "dotnet")),
        dll,
        roslyn_exe=exe,
        toolchain_dir=tmp_path / "tc",
        priority="bundled_first",
        prober=_Prober(),
    )
    assert chain.c is not None
    assert chain.c.origin == "downloaded"
    assert chain.unreal is not None
    assert chain.unreal.origin == "downloaded"
    assert chain.csharp is not None
    assert chain.csharp.origin == "bundled"


def test_incomplete_zig_install_ignored(tmp_path: Path, dll: Path) -> None:
    _install_zig(tmp_path / "tc", complete=False)  # yarım kurulum: işaret dosyası yok
    prober = _Prober()
    chain = discover(
        str(_fake_bin(tmp_path / "bin")), dll, toolchain_dir=tmp_path / "tc", prober=prober
    )
    assert chain.c is None
    assert prober.calls == []


def test_zig_probe_failure_leaves_targets_missing(tmp_path: Path, dll: Path) -> None:
    _install_zig(tmp_path / "tc")
    chain = discover(
        str(_fake_bin(tmp_path / "bin")), dll, toolchain_dir=tmp_path / "tc", prober=_Prober(None)
    )
    assert chain.summary() == {"c": None, "cpp": None, "unreal": None, "csharp": None}


def test_self_contained_roslyn_without_dotnet(tmp_path: Path, dll: Path) -> None:
    exe = _fake_bin(tmp_path / "sc", "RoslynCheck") / f"RoslynCheck{_EXE}"
    chain = discover(str(_fake_bin(tmp_path / "bin")), tmp_path / "yok.dll", roslyn_exe=exe)
    assert chain.csharp is not None
    assert (chain.csharp.kind, chain.csharp.origin) == ("roslyn", "bundled")
    assert chain.csharp.command == [str(exe.resolve())]
    # path_first: dotnet + dll varsa o kullanılır
    with_dotnet = discover(str(_fake_bin(tmp_path / "bin2", "dotnet")), dll, roslyn_exe=exe)
    assert with_dotnet.csharp is not None
    assert with_dotnet.csharp.origin == "system"


def test_compiler_statuses_report_origin(tmp_path: Path, dll: Path) -> None:
    _install_zig(tmp_path / "tc")
    chain = discover(
        str(_fake_bin(tmp_path / "bin", "gcc")),
        dll,
        toolchain_dir=tmp_path / "tc",
        prober=_Prober(),
    )
    statuses = {s.target: (s.tool, s.origin) for s in compiler_statuses(chain)}
    assert statuses == {
        "c": ("gcc", "system"),
        "cpp": ("zig", "downloaded"),
        "unreal": ("zig", "downloaded"),
        "csharp": (None, None),
    }


def test_get_toolchain_uses_settings_toolchain_dir(
    tmp_path: Path, dll: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(_fake_bin(tmp_path / "bin")))
    _install_zig(tmp_path / "tc")
    monkeypatch.setattr(toolchain_module, "probe_flags", _Prober())
    settings = ValidationSettings(roslyn_check_dll=dll, toolchain_dir=tmp_path / "tc")
    clear_toolchain_cache()
    try:
        chain = get_toolchain(settings)
        assert chain.c is not None
        assert chain.c.origin == "downloaded"
    finally:
        clear_toolchain_cache()


def test_discovery_never_raises_on_permission_errors(
    tmp_path: Path, dll: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Erişilemeyen dll/exe ya da patlayan sonda keşfi (ve /health/ready'yi) düşürmez."""
    original = Path.is_file

    def is_file(self: Path) -> bool:
        if self.name.startswith("RoslynCheck"):
            raise PermissionError("erişim reddedildi")
        return original(self)

    monkeypatch.setattr(Path, "is_file", is_file)
    chain = discover(str(_fake_bin(tmp_path / "bin", "gcc", "dotnet")), dll, roslyn_exe=dll)
    assert chain.c is not None
    assert chain.csharp is None

    def exploding(_zig: str, _language: ZigLanguage, *, timeout_s: float) -> list[str] | None:
        raise RuntimeError("beklenmeyen")

    _install_zig(tmp_path / "tc")
    monkeypatch.setattr(Path, "is_file", original)
    chain = discover(
        str(_fake_bin(tmp_path / "empty")), dll, toolchain_dir=tmp_path / "tc", prober=exploding
    )
    assert chain == Toolchain()
