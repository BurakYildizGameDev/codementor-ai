"""Masaüstü tercihlerini `codementor.toml`'a yazar (Faz 24): CLI ve API aynı modeli kullansın.

Yalnız `[providers]` altındaki `default` ve sağlayıcı başına `model`, `base_url`,
`allow_tool_agent` yazılır; API anahtarı hiçbir zaman (kasada kalır, ADR-0014). `tomlkit`
dosyanın yorumlarını ve sırasını korur.

Faz C (Y7, O7): kullanıcının yazdığı biçim korunur: satır içi tablo (`providers = { … }`) ve
nokta anahtarı (`providers.fallback = …`) yerinde güncellenir, değiştirilmeyen anahtarlar
kaybolmaz. BOM'lu dosya okunur, BOM'suz yazılır. Yazım atomiktir (geçici dosya + `os.replace`):
yarıda kesilirse eski dosya bozulmaz.

Faz G6 (denetimden ertelenenler): `[providers]` beklenmeyen biçimdeyse (dizi tablosu
`[[providers.x]]` ya da tablo olmayan değer, ör. `providers = "x"`) dosya EZİLMEZ; yazma
`ValueError` ile durur ve eski dosya bayt bayt korunur. Dosyanın satır sonu biçimi (CRLF/LF)
korunur.
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
from codementor.paths import replace_file

_BOM = "\ufeff"  # kaynakta görünmez karakter olmasın diye kaçışla

_UNEXPECTED_SHAPE = "codementor.toml'da [providers] beklenmeyen biçimde; elle düzeltin."


def _newline_of(text: str) -> str:
    """Dosyada kullanılan satır sonunu verir (`"\\r\\n"`, `"\\r"` ya da `"\\n"`); yoksa `"\\n"`."""
    index = text.find("\n")
    if index == -1:
        return "\r" if "\r" in text else "\n"
    return "\r\n" if text[index - 1 : index] == "\r" else "\n"


def _table(parent: MutableMapping[str, Any], key: str) -> MutableMapping[str, Any]:
    """`parent[key]` tablosu; yoksa ebeveynin biçiminde (satır içi ya da normal) oluşturulur."""
    existing = parent.get(key)
    if isinstance(existing, MutableMapping):
        return existing
    if existing is not None:
        # Var olan değer tablo değil: dizi tablosu (`[[providers.x]]`) ya da düz değer
        # (`providers = "x"`). Üzerine yazmak kullanıcının yapılandırmasını sessizce silerdi.
        raise ValueError(_UNEXPECTED_SHAPE)
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
        replace_file(Path(temp), path)
    except BaseException:
        Path(temp).unlink(missing_ok=True)
        raise


def write_provider_prefs(path: Path, prefs: DesktopPrefs) -> Path:
    """Tercihleri `path`'e işler (dosya yoksa oluşturur); yazılan yolu döndürür."""
    # `newline=""` ile okunur: evrensel satır sonu çevirisi CRLF'yi LF yapar ve yazarken
    # kullanıcının dosyası sessizce dönüşürdü. (`Path.read_text` `newline`'ı 3.13'te aldı.)
    if path.is_file():
        with path.open(encoding="utf-8", newline="") as handle:
            original = handle.read()
    else:
        original = ""
    newline = _newline_of(original)
    document = tomlkit.parse(original.removeprefix(_BOM))
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
    written = tomlkit.dumps(document)
    if newline != "\n":
        # tomlkit var olan satır sonlarını korur, ama yeni eklediği satırları LF yazar; dosyanın
        # biçimine çeviriyoruz (önce CRLF'leri LF'e indir, sonra hepsini hedefe yaz).
        written = written.replace("\r\n", "\n").replace("\n", newline)
    _write_atomic(path, written)
    return path
