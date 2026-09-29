"""Tier 1 araç keşfi (mimari §5.2.2, ADR-0009).

Araçlar `PATH`'te aranır ve mutlak yolla çağrılır (alt süreç ortamındaki `PATH`'e
güvenilmez). Tercih sırası:

- C: gcc → clang · C++: g++ → clang++ · Unreal C++: clang++ → g++ (mimari clang++ önerir)
- C# / Unity: `dotnet` + derlenmiş `tools/roslyn-check` (`make roslyn-check`)

Sonuç `PATH` ve DLL yolu anahtarıyla önbelleklenir; `/health/ready` `summary()` kullanır.
"""

from __future__ import annotations

import os
import shutil
from functools import lru_cache
from pathlib import Path

from codementor.config import ValidationSettings
from codementor.models.validation import CompilerTool, DiagnosticTool, Toolchain

_KIND: dict[str, DiagnosticTool] = {
    "gcc": "gcc",
    "g++": "gcc",
    "clang": "clang",
    "clang++": "clang",
}


def _which(name: str, path: str) -> str | None:
    try:
        found = shutil.which(name, path=path)
    except (OSError, ValueError):
        return None
    return str(Path(found).resolve()) if found else None


def _first(names: tuple[str, ...], path: str) -> CompilerTool | None:
    for name in names:
        exe = _which(name, path)
        if exe:
            return CompilerTool(name=name, kind=_KIND[name], command=[exe])
    return None


def discover(path: str, roslyn_dll: Path) -> Toolchain:
    """Verilen `PATH` dizgesinde araçları arar; hiçbir zaman istisna fırlatmaz."""
    csharp = None
    dotnet = _which("dotnet", path)
    if dotnet and roslyn_dll.is_file():
        csharp = CompilerTool(
            name="roslyn-check", kind="roslyn", command=[dotnet, str(roslyn_dll.resolve())]
        )
    return Toolchain(
        c=_first(("gcc", "clang"), path),
        cpp=_first(("g++", "clang++"), path),
        unreal=_first(("clang++", "g++"), path),
        csharp=csharp,
    )


@lru_cache(maxsize=4)
def _cached(path: str, roslyn_dll: str) -> Toolchain:
    return discover(path, Path(roslyn_dll))


def get_toolchain(settings: ValidationSettings) -> Toolchain:
    """Süreç ortamındaki `PATH` için önbellekli keşif."""
    return _cached(os.environ.get("PATH", ""), str(settings.roslyn_check_dll))


def clear_toolchain_cache() -> None:
    """Önbelleği temizler (araç kurulduktan sonra veya testlerde)."""
    _cached.cache_clear()
