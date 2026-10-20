"""Test ağ koruması (Faz 50, AGENTS.md kural 4): loopback dışına soket bağlantısı engellenir.

`@pytest.mark.live` testleri muaftır. Unix soketleri ve loopback (`127.0.0.0/8`, `::1`,
`localhost`) serbesttir; alt süreçler etkilenmez (kendi süreçleridir).

Tam tarama #8 (KALAN_ISLER iş 17): Windows'un varsayılan Proactor döngüsü `sock_connect`'i
`socket.connect` yerine `_overlapped.ConnectEx` ile yapar (`IocpProactor.connect`); respx'siz bir
`httpx.AsyncClient` bu yoldan ağa çıkabiliyordu. O yol ve DNS çözümlemesi (`socket.getaddrinfo`)
de korunur.
"""

from __future__ import annotations

import ipaddress
import socket
import sys
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


def is_local_host(host: Any) -> bool:
    """DNS'e gitmeyen ad mı: boş (pasif bağlama), loopback adı ya da IP literali.

    IP literali çözümleme yapmaz; loopback dışı IP'ye bağlanma `connect` korumasında düşer.
    """
    if host is None:
        return True
    if isinstance(host, bytes):
        host = host.decode("ascii", "replace")
    if not isinstance(host, str):
        return False
    if not host or host.lower() in _LOOPBACK_NAMES:
        return True
    try:
        ipaddress.ip_address(host.split("%", 1)[0])
    except ValueError:
        return False
    return True


def _guard_getaddrinfo(original: Any) -> Any:
    def guarded(host: Any, *args: Any, **kwargs: Any) -> Any:
        if not is_local_host(host):
            raise NetworkBlockedError(f"test DNS çözümlemeye çalıştı: {host!r}")
        return original(host, *args, **kwargs)

    return guarded


def _guard_proactor_connect(original: Any) -> Any:
    def guarded(self: Any, conn: socket.socket, address: Any) -> Any:
        if conn.family in (socket.AF_INET, socket.AF_INET6) and not is_loopback(address):
            raise NetworkBlockedError(f"test ağa çıkmaya çalıştı: {address!r}")
        return original(self, conn, address)

    return guarded


def guarded_patches() -> list[tuple[Any, str, Any]]:
    """`(hedef, ad, korumalı)` yamaları: socket yöntemleri, DNS ve Windows Proactor bağlantısı."""
    patches: list[tuple[Any, str, Any]] = [
        (socket.socket, name, method) for name, method in guarded_methods().items()
    ]
    patches.append((socket, "getaddrinfo", _guard_getaddrinfo(socket.getaddrinfo)))
    if sys.platform == "win32":
        from asyncio import windows_events

        proactor = windows_events.IocpProactor
        patches.append((proactor, "connect", _guard_proactor_connect(proactor.connect)))
    return patches
