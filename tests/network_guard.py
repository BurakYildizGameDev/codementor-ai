"""Test ağ koruması (Faz 50, AGENTS.md kural 4): loopback dışına soket bağlantısı engellenir.

`@pytest.mark.live` testleri muaftır. Unix soketleri ve loopback (`127.0.0.0/8`, `::1`,
`localhost`) serbesttir; alt süreçler etkilenmez (kendi süreçleridir).
"""

from __future__ import annotations

import ipaddress
import socket
from typing import Any

_LOOPBACK_NAMES = frozenset({"localhost", "localhost.localdomain"})


class NetworkBlockedError(RuntimeError):
    """Test, loopback dışına bağlanmaya çalıştı."""


def is_loopback(address: Any) -> bool:
    """`connect` adresi loopback mı (ad ya da IP; IPv6 dörtlüsü dahil)."""
    host = address[0] if isinstance(address, tuple) else address
    if not isinstance(host, str):
        return False
    if host.lower() in _LOOPBACK_NAMES:
        return True
    try:
        return ipaddress.ip_address(host.split("%", 1)[0]).is_loopback
    except ValueError:
        return False


def _guard(original: Any) -> Any:
    def guarded(self: socket.socket, address: Any) -> Any:
        if self.family in (socket.AF_INET, socket.AF_INET6) and not is_loopback(address):
            raise NetworkBlockedError(f"test ağa çıkmaya çalıştı: {address!r}")
        return original(self, address)

    return guarded


def guarded_methods() -> dict[str, Any]:
    """`socket.socket` üzerine yamanacak korumalı `connect` / `connect_ex`."""
    return {
        "connect": _guard(socket.socket.connect),
        "connect_ex": _guard(socket.socket.connect_ex),
    }
