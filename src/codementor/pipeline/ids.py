"""Bağımlılıksız ULID (analysis_id): 48 bit milisaniye + 80 bit rastgele, Crockford base32."""

from __future__ import annotations

import secrets
import time

_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def new_ulid(timestamp_ms: int | None = None) -> str:
    """26 karakterlik ULID; zaman önekli olduğu için sözlük sırası ≈ oluşturma sırası."""
    ms = int(time.time() * 1000) if timestamp_ms is None else timestamp_ms
    value = (ms & ((1 << 48) - 1)) << 80 | secrets.randbits(80)
    chars = []
    for _ in range(26):
        chars.append(_ALPHABET[value & 31])
        value >>= 5
    return "".join(reversed(chars))
