"""Masaüstü tercihlerini `codementor.toml`'a yazar (Faz 24): CLI ve API aynı modeli kullansın.

Yalnız `[providers]` altındaki `default` ve sağlayıcı başına `model`, `base_url`,
`allow_tool_agent` yazılır; API anahtarı hiçbir zaman (kasada kalır, ADR-0014). `tomlkit`
dosyanın yorumlarını ve sırasını korur.
"""

from __future__ import annotations

from pathlib import Path

import tomlkit
from tomlkit.items import Table

from codementor.models.desktop import DesktopPrefs


def _table(parent: Table | tomlkit.TOMLDocument, key: str) -> Table:
    existing = parent.get(key)
    if isinstance(existing, Table):
        return existing
    table = tomlkit.table()
    parent[key] = table
    return table


def write_provider_prefs(path: Path, prefs: DesktopPrefs) -> Path:
    """Tercihleri `path`'e işler (dosya yoksa oluşturur); yazılan yolu döndürür."""
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    document = tomlkit.parse(text)
    providers = _table(document, "providers")
    if prefs.provider:
        providers["default"] = prefs.provider
    for name, override in prefs.providers.items():
        values = override.as_settings()
        if not values:
            continue
        section = _table(providers, name)
        for key, value in values.items():
            section[key] = value
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(tomlkit.dumps(document), encoding="utf-8")
    return path
