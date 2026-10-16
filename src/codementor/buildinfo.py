"""Derleme ve sürüm bilgisi okuma yardımcıları (Faz 60)."""

from __future__ import annotations

import functools
import json
from pathlib import Path

from codementor import __version__
from codementor.log import get_logger
from codementor.models.build import BuildInfo
from codementor.paths import resource_path

log = get_logger("codementor.buildinfo")  # maskeleme zinciri her zaman kurulu (Faz G5)


@functools.lru_cache(maxsize=1)
def build_info() -> BuildInfo:
    """Çalışan uygulamanın sürüm ve derleme bilgisini döndürür."""
    path: Path = resource_path("data/build_info.json")
    if not path.is_file():
        return BuildInfo(
            version=__version__,
            commit=None,
            built_at=None,
            source="kaynak",
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return BuildInfo.model_validate(data)
    except Exception as exc:  # bozuk JSON ya da şema dışı alan: exe yine açılmalı
        log.warning("build_info_unreadable", error=type(exc).__name__)
        return BuildInfo(
            version=__version__,
            commit=None,
            built_at=None,
            source="kaynak",
        )


def describe(info: BuildInfo) -> str:
    """BuildInfo nesnesini tek satırlık okunabilir metne dönüştürür."""
    if info.source == "kaynak":
        return f"{info.version} · kaynaktan"
    parts = [info.version]
    if info.commit:
        parts.append(info.commit)
    if info.built_at:
        parts.append(info.built_at.strftime("%d.%m.%Y"))
    if len(parts) == 1:
        parts.append("exe")
    return " · ".join(parts)


def format_cli_version(info: BuildInfo) -> str:
    """CLI --version çıktısını biçimlendirir."""
    if info.source == "kaynak":
        return f"codementor {info.version} (kaynaktan)"
    parts = []
    if info.commit:
        parts.append(info.commit)
    if info.built_at:
        parts.append(info.built_at.strftime("%Y-%m-%d"))
    parts.append("exe")
    return f"codementor {info.version} ({', '.join(parts)})"
