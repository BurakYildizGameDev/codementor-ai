"""Tier 1 araç keşfi (mimari §5.2.2, ADR-0009, ADR-0018).

Araçlar mutlak yolla çağrılır (alt süreç ortamındaki `PATH`'e güvenilmez). Tercih sırası:

- C: gcc → clang · C++: g++ → clang++ · Unreal C++: clang++ → g++ (mimari clang++ önerir)
- Bunlar yoksa zig (Faz 29): önce `PATH`'teki, sonra `toolchain_dir`'e indirilmiş olan.
  Zig `zig clang <bayraklar>` ile çağrılır (bkz. `validation.zig`); sonda yalnız gerekince.
- C# / Unity: `dotnet` + derlenmiş `tools/roslyn-check` → yoksa self-contained `RoslynCheck`
  (pakete gömülü, dotnet gerekmez).

`toolchain_priority = "bundled_first"` sırayı çevirir: indirilen/gömülü araç önce denenir.
Sonuç önbelleklenir; kurulumdan sonra `clear_toolchain_cache()`. `/health/ready` ve masaüstü
`compiler_statuses()` kullanır.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path
from typing import Literal, Protocol

from codementor.config import ValidationSettings
from codementor.log import get_logger
from codementor.models.api import CompilerStatus
from codementor.models.validation import CompilerTool, DiagnosticTool, Toolchain, ToolOrigin
from codementor.validation.runner import find_on_path
from codementor.validation.toolchain_install import installed_zig, zig_root
from codementor.validation.zig import ZigLanguage, probe_flags

Priority = Literal["path_first", "bundled_first"]
log = get_logger("codementor.toolchain")

_KIND: dict[str, DiagnosticTool] = {
    "gcc": "gcc",
    "g++": "gcc",
    "clang": "clang",
    "clang++": "clang",
}


class Prober(Protocol):
    """`probe_flags` imzası; testlerde sahtesi verilir."""

    def __call__(
        self, zig: str, language: ZigLanguage, *, timeout_s: float
    ) -> list[str] | None: ...


def _which(name: str, path: str) -> str | None:
    # shutil.which değil: Windows'ta çalışma dizinine de bakar (Faz A2, Y1)
    found = find_on_path(name, path)
    return str(found) if found else None


def _existing(path: Path | None) -> str | None:
    """Dosya varsa mutlak yolu; erişim hatası (izin, bozuk yol) yok sayılır."""
    try:
        return str(path.resolve()) if path is not None and path.is_file() else None
    except (OSError, ValueError):
        return None


def _first(names: tuple[str, ...], path: str) -> CompilerTool | None:
    for name in names:
        exe = _which(name, path)
        if exe:
            return CompilerTool(name=name, kind=_KIND[name], command=[exe])
    return None


class _Zig:
    """Zig adaylarını gerektiğinde (ilk istekte) sondalar; ilk çalışan aday kullanılır."""

    def __init__(
        self, candidates: list[tuple[str, ToolOrigin]], prober: Prober, timeout_s: float
    ) -> None:
        self._candidates = candidates
        self._prober = prober
        self._timeout_s = timeout_s
        self._tools: tuple[CompilerTool, CompilerTool] | None = None
        self._probed = False

    def tools(self) -> tuple[CompilerTool, CompilerTool] | None:
        if not self._probed:
            self._probed = True
            for exe, origin in self._candidates:
                c = self._prober(exe, "c", timeout_s=self._timeout_s)
                cpp = self._prober(exe, "c++", timeout_s=self._timeout_s) if c else None
                if c and cpp:
                    self._tools = (
                        CompilerTool(
                            name="zig", kind="clang", command=[exe, "clang", *c], origin=origin
                        ),
                        CompilerTool(
                            name="zig", kind="clang", command=[exe, "clang", *cpp], origin=origin
                        ),
                    )
                    break
        return self._tools

    def c(self) -> CompilerTool | None:
        tools = self.tools()
        return tools[0] if tools else None

    def cpp(self) -> CompilerTool | None:
        tools = self.tools()
        return tools[1] if tools else None


def _choose(
    system: CompilerTool | None, fallback: Callable[[], CompilerTool | None], priority: Priority
) -> CompilerTool | None:
    """`path_first`: sistem aracı varsa yedeğe (zig sondası) hiç bakılmaz."""
    if priority == "path_first" and system is not None:
        return system
    return fallback() or system


def discover(
    path: str,
    roslyn_dll: Path,
    *,
    roslyn_exe: Path | None = None,
    toolchain_dir: Path | None = None,
    priority: Priority = "path_first",
    probe_timeout_s: float = 30,
    prober: Prober = probe_flags,
) -> Toolchain:
    """Verilen `PATH` ve kurulum dizinlerinde araçları arar; hiçbir zaman istisna fırlatmaz.

    `toolchain_dir`: indirilen araçların dizini (zig `toolchain_dir/zig`); yarım kurulum yok
    sayılır.
    """
    try:
        return _discover(
            path,
            roslyn_dll,
            roslyn_exe=roslyn_exe,
            toolchain_dir=toolchain_dir,
            priority=priority,
            probe_timeout_s=probe_timeout_s,
            prober=prober,
        )
    except Exception as exc:  # son güvenlik ağı: keşif analizi ve /health/ready'yi düşürmez
        log.warning("toolchain_discovery_failed", error=type(exc).__name__)
        return Toolchain()


def _discover(
    path: str,
    roslyn_dll: Path,
    *,
    roslyn_exe: Path | None = None,
    toolchain_dir: Path | None = None,
    priority: Priority = "path_first",
    probe_timeout_s: float = 30,
    prober: Prober = probe_flags,
) -> Toolchain:

    path_zig = _which("zig", path)
    downloaded = installed_zig(zig_root(toolchain_dir)) if toolchain_dir is not None else None
    downloaded_exe = _existing(downloaded)
    candidates: list[tuple[str, ToolOrigin]] = []
    if path_zig:
        candidates.append((path_zig, "system"))
    if downloaded_exe is not None:
        entry: tuple[str, ToolOrigin] = (downloaded_exe, "downloaded")
        candidates.insert(0 if priority == "bundled_first" else len(candidates), entry)
    zig = _Zig(candidates, prober, probe_timeout_s)
    dotnet_tool = None
    dotnet, dll = _which("dotnet", path), _existing(roslyn_dll)
    if dotnet and dll:
        dotnet_tool = CompilerTool(name="roslyn-check", kind="roslyn", command=[dotnet, dll])
    bundled_tool = None
    if bundled := _existing(roslyn_exe):
        bundled_tool = CompilerTool(
            name="roslyn-check", kind="roslyn", command=[bundled], origin="bundled"
        )
    return Toolchain(
        c=_choose(_first(("gcc", "clang"), path), zig.c, priority),
        cpp=_choose(_first(("g++", "clang++"), path), zig.cpp, priority),
        unreal=_choose(_first(("clang++", "g++"), path), zig.cpp, priority),
        csharp=_choose(dotnet_tool, lambda: bundled_tool, priority),
    )


def compiler_statuses(toolchain: Toolchain) -> list[CompilerStatus]:
    """`/health/ready` ve masaüstü için hedef → araç adı ve kökeni."""
    return [
        CompilerStatus(
            target=target, tool=tool.name if tool else None, origin=tool.origin if tool else None
        )
        for target, tool in (
            ("c", toolchain.c),
            ("cpp", toolchain.cpp),
            ("unreal", toolchain.unreal),
            ("csharp", toolchain.csharp),
        )
    ]


@lru_cache(maxsize=4)
def _cached(
    path: str,
    roslyn_dll: str,
    roslyn_exe: str,
    toolchain_dir: str,
    priority: Priority,
    probe_timeout_s: float,
) -> Toolchain:
    return discover(
        path,
        Path(roslyn_dll),
        roslyn_exe=Path(roslyn_exe),
        toolchain_dir=Path(toolchain_dir),
        priority=priority,
        probe_timeout_s=probe_timeout_s,
        prober=probe_flags,
    )


def get_toolchain(settings: ValidationSettings) -> Toolchain:
    """Süreç ortamındaki `PATH` için önbellekli keşif."""
    return _cached(
        os.environ.get("PATH", ""),
        str(settings.roslyn_check_dll),
        str(settings.roslyn_check_exe),
        str(settings.toolchain_dir),
        settings.toolchain_priority,
        settings.zig.probe_timeout_s,
    )


def clear_toolchain_cache() -> None:
    """Önbelleği temizler (araç kurulduktan sonra veya testlerde)."""
    _cached.cache_clear()
