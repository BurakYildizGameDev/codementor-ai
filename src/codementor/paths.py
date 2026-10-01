"""Kaynak kökü ve göreli yol çözümü (ADR-0016).

`data/`, `prompts/` ve varsayılan `codementor.toml` kaynak kökündedir:
- exe (PyInstaller): `sys._MEIPASS`
- kurulu wheel: paket içindeki `codementor/_resources/` (`importlib.resources`)
- kaynaktan/düzenlenebilir kurulum: depo kökü

Yapılandırmadaki göreli yollar kaynağına göre çözülür: varsayılan → kaynak kökü,
`codementor.toml` → dosyanın dizini, ortam değişkeni/CLI bayrağı → çalışma dizini.
"""

from __future__ import annotations

import sys
from importlib.resources import files
from pathlib import Path

RESOURCES_DIR = "_resources"


def _package_resources() -> Path:
    """Wheel'deki paket verisi dizini (düzenlenebilir kurulumda yoktur)."""
    return Path(str(files("codementor") / RESOURCES_DIR))


def resource_root() -> Path:
    """`data/` ve `prompts/` dizinlerinin bulunduğu kök."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        bundle: str = sys._MEIPASS
        return Path(bundle)
    bundled = _package_resources()
    if bundled.is_dir():
        return bundled
    # src/codementor/paths.py → depo kökü
    return Path(__file__).resolve().parents[2]


def resource_path(relative: str) -> Path:
    """Kaynak köküne göre mutlak yol (yapılandırma varsayılanları için)."""
    return resource_root() / relative


def resolve_relative(path: Path, base: Path) -> Path:
    """Göreli `path`'i `base`'e göre çözer; mutlak yol olduğu gibi kalır."""
    return path if path.is_absolute() else base / path
