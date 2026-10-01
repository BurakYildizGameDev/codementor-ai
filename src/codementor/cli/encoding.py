"""Konsol kodlaması (Faz 27): Windows'ta stdout/stderr çoğu zaman cp1254/cp1252'dir.

Rich tabloları `✗`, `→` ve Türkçe karakterler içerir; bu kodlamalar bunları yazamaz ve CLI
`UnicodeEncodeError` ile çöker. Akış UTF-8 değilse yeniden yapılandırılır; yazılamayan
karakter (eski konsol yazı tipi) çökme yerine `?` olur.
"""

from __future__ import annotations

import sys
from typing import TextIO


def ensure_utf8(stream: TextIO | None) -> None:
    """`stream` UTF-8 değilse UTF-8'e alır (`reconfigure` desteklemeyen akışlara dokunmaz)."""
    if stream is None:
        return
    encoding = (getattr(stream, "encoding", None) or "").lower().replace("-", "")
    reconfigure = getattr(stream, "reconfigure", None)
    if encoding == "utf8" or reconfigure is None:
        return
    reconfigure(encoding="utf-8", errors="replace")


def ensure_utf8_console() -> None:
    """CLI girişinde çağrılır: standart çıktı ve hata akışları."""
    ensure_utf8(sys.stdout)
    ensure_utf8(sys.stderr)
