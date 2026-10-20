"""Kaynak kökü ve göreli yol çözümü (ADR-0016, ADR-0027).

`data/`, `prompts/` ve varsayılan `codementor.toml` kaynak kökündedir:
- exe (PyInstaller): `sys._MEIPASS`
- kurulu wheel: paket içindeki `codementor/_resources/` (`importlib.resources`)
- kaynaktan/düzenlenebilir kurulum: depo kökü

Yapılandırmadaki göreli yollar kaynağına göre çözülür: varsayılan → kaynak kökü,
`codementor.toml` → dosyanın dizini (orada yoksa kaynak kökü), ortam değişkeni/CLI bayrağı →
çalışma dizini.
"""

from __future__ import annotations

import os
import sys
import time
from importlib.resources import files
from pathlib import Path

RESOURCES_DIR = "_resources"

# Windows'ta tarayıcı/indeksleyici yeni yazılan dosyayı kısa süre açık tutunca `os.replace`
# WinError 5/32 (PermissionError) verir (Faz 58'deki toolchain kilidiyle aynı). Küçük dosyalar
# için toplam ~0,8 sn yeniden denenir (masaüstünde arayüz iş parçacığından da çağrılır).
_RETRY_REPLACE = os.name == "nt"
_REPLACE_DELAYS_S = (0.02, 0.05, 0.1, 0.2, 0.4)


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


def resolve_config_relative(path: Path, base: Path) -> Path:
    """`codementor.toml`'daki göreli yolu toml'un dizinine (`base`) göre çözer (ADR-0016).

    O dizinde yoksa ama kaynak kökünde varsa kaynak köküne düşer (ADR-0027): exe'nin yanına
    kopyalanan varsayılan toml'daki `data/...` yolları paket verisini göstermeye devam eder.
    """
    resolved = resolve_relative(path, base)
    if path.is_absolute() or resolved.exists():
        return resolved
    bundled = resource_path(str(path))
    return bundled if bundled.exists() else resolved


def replace_file(source: Path, target: Path) -> None:
    """`os.replace(source, target)`; Windows'taki geçici dosya kilidinde kısa beklemelerle yineler.

    Kalıcı hata (son deneme) çağırana iletilir.
    """
    for delay in _REPLACE_DELAYS_S if _RETRY_REPLACE else ():
        try:
            os.replace(source, target)
            return
        except PermissionError:
            time.sleep(delay)
    os.replace(source, target)
