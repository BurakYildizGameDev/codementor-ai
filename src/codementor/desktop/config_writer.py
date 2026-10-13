"""Masaüstü tercihlerini `codementor.toml`'a yazar (Faz 24): CLI ve API aynı modeli kullansın.

Yalnız `[providers]` altındaki `default` ve sağlayıcı başına `model`, `base_url`,
`allow_tool_agent` yazılır; API anahtarı hiçbir zaman (kasada kalır, ADR-0014). `tomlkit`
dosyanın yorumlarını ve sırasını korur.

Faz C (Y7, O7): kullanıcının yazdığı biçim korunur: satır içi tablo (`providers = { … }`) ve
nokta anahtarı (`providers.fallback = …`) yerinde güncellenir, değiştirilmeyen anahtarlar
kaybolmaz. BOM'lu dosya okunur, BOM'suz yazılır. Yazım atomiktir (geçici dosya + `os.replace`):
yarıda kesilirse eski dosya bozulmaz.
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any

import tomlkit
from tomlkit import TOMLDocument
from tomlkit.items import InlineTable, Table

from codementor.models.desktop import DesktopPrefs

_BOM = "\ufeff"  # kaynakta görünmez karakter olmasın diye kaçışla


def _table(parent: MutableMapping[str, Any], key: str) -> MutableMapping[str, Any]:
    """`parent[key]` tablosu; yoksa ebeveynin biçiminde (satır içi ya da normal) oluşturulur."""
    existing = parent.get(key)
    if isinstance(existing, MutableMapping):
        return existing
    # Başlıklı tablo yalnız başlıklı bir tablonun ya da belgenin altına; satır içi tablo ya da
    # nokta anahtarlı (`providers.x = …`) üst düzeyin altına başlık eklemek sonraki satırları
    # yanlış tabloya kaydırır: orada satır içi tablo yazılır.
    headed = isinstance(parent, (Table, TOMLDocument)) and not isinstance(parent, InlineTable)
    table: MutableMapping[str, Any] = tomlkit.table() if headed else tomlkit.inline_table()
    parent[key] = table
    return parent[key]  # type: ignore[no-any-return]


def _write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=f".{path.name}-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        os.replace(temp, path)
    except BaseException:
        Path(temp).unlink(missing_ok=True)
        raise


def write_provider_prefs(path: Path, prefs: DesktopPrefs) -> Path:
    """Tercihleri `path`'e işler (dosya yoksa oluşturur); yazılan yolu döndürür."""
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    document = tomlkit.parse(text.removeprefix(_BOM))
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
    _write_atomic(path, tomlkit.dumps(document))
    return path
