"""Jinja2 şablon ortamı, sınırlayıcı koruması ve `prompt_version` (mimari §5.4.4)."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

TEMPLATE_SUFFIXES = (".j2", ".yaml", ".yml")

# `<user_code>` / `</user_code>` kullanıcı verisinde geçerse sınırlayıcıyı kırmasın diye açılı
# ayraç `&lt;` yapılır (mimari §12). Eşleşme bir "iskelet" üzerinde aranır: görünmez karakterler
# atılır, NFKC (tam genişlikli biçimler) ve benzer görünen harfler (Kiril e, c ...) katlanır.
# Metnin geri kalanı değişmez; kanıtın birebir alıntı olması bozulmasın.
_DELIMITER = re.compile(r"<\s*/?\s*user_code")
# Kod noktalarıyla yazıldı: kaynakta görünmez ya da benzer görünen karakter olmasın.
_INVISIBLE = frozenset(
    map(chr, (0x00AD, 0x180E, 0xFEFF, *range(0x200B, 0x2010), *range(0x2060, 0x2065)))
)
_CONFUSABLES = str.maketrans(
    {
        **dict.fromkeys(map(chr, (0x2039, 0x3008, 0x27E8, 0x1438)), "<"),  # açılı tırnak/ayraçlar
        **dict.fromkeys(map(chr, (0x2044, 0x2215, 0x29F8)), "/"),  # kesir, bölme, büyük eğik çizgi
        **dict.fromkeys(map(chr, (0x057D, 0x03C5)), "u"),  # Ermeni seh, Yunan upsilon
        chr(0x0455): "s",  # Kiril dze
        chr(0x0435): "e",  # Kiril ie
        chr(0x0433): "r",  # Kiril ghe
        **dict.fromkeys(map(chr, (0x0441, 0x03F2)), "c"),  # Kiril es, Yunan hilal sigma
        **dict.fromkeys(map(chr, (0x043E, 0x03BF)), "o"),  # Kiril o, Yunan omikron
        chr(0x0501): "d",  # Kiril komi de
        chr(0x2017): "_",  # çift alt çizgi
    }
)


def _skeleton(text: str) -> tuple[str, list[int]]:
    """Karşılaştırma için katlanmış metin ve her iskelet karakterinin özgün konumu."""
    chars: list[str] = []
    positions: list[int] = []
    for i, ch in enumerate(text):
        if ch in _INVISIBLE:
            continue
        folded = unicodedata.normalize("NFKC", ch.translate(_CONFUSABLES)).lower()
        chars.append(folded if len(folded) == 1 else ch)
        positions.append(i)
    return "".join(chars), positions


def guard_delimiters(text: str) -> str:
    """Kullanıcı kaynaklı metindeki `<user_code>` benzeri dizileri etkisizleştirir."""
    skeleton, positions = _skeleton(text)
    starts = [positions[m.start()] for m in _DELIMITER.finditer(skeleton)]
    if not starts:
        return text
    parts: list[str] = []
    previous = 0
    for start in starts:
        parts.append(text[previous:start])
        parts.append("&lt;")
        previous = start + 1
    parts.append(text[previous:])
    return "".join(parts)


def _require_dir(directory: Path) -> Path:
    if not directory.is_dir():
        raise FileNotFoundError(f"Prompt şablon dizini bulunamadı: {directory}")
    return directory.resolve()


@lru_cache(maxsize=8)
def _environment(directory: Path) -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(directory), encoding="utf-8"),
        undefined=StrictUndefined,
        autoescape=False,  # çıktı HTML değil; kullanıcı verisi yalnızca değişken olarak girer
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=False,
    )
    env.filters["guard"] = guard_delimiters
    return env


def render(directory: Path, name: str, **context: Any) -> str:
    """`directory/name` şablonunu işler; tanımsız değişken hata verir."""
    return _environment(_require_dir(directory)).get_template(name).render(**context).strip()


def prompt_version(directory: Path) -> str:
    """`"v1+" + sha256(şablonlar + few-shot'lar)[:8]`; satır sonu farkı sürümü değiştirmez."""
    root = _require_dir(directory)
    digest = hashlib.sha256()
    files = sorted(
        p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in TEMPLATE_SUFFIXES
    )
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n") + b"\0")
    return f"{root.name}+{digest.hexdigest()[:8]}"
