"""Ağ koruması (Faz 50): loopback dışına bağlanan test düşer, loopback serbest."""

from __future__ import annotations

import socket

import pytest

from tests.network_guard import NetworkBlockedError, is_loopback


def test_non_loopback_connect_blocked() -> None:
    """Kabul: loopback dışına bağlanan test düşer (203.0.113.0/24 belge adresi)."""
    with (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock,
        pytest.raises(NetworkBlockedError, match="ağa çıkmaya"),
    ):
        sock.connect(("203.0.113.1", 443))


def test_create_connection_blocked() -> None:
    with pytest.raises(NetworkBlockedError):
        socket.create_connection(("203.0.113.1", 80), timeout=1)


def test_loopback_allowed() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]
        with socket.create_connection(("127.0.0.1", port), timeout=2):
            pass


@pytest.mark.parametrize(
    ("address", "expected"),
    [
        (("127.0.0.1", 1), True),
        (("127.5.0.1", 1), True),
        (("::1", 1, 0, 0), True),
        (("localhost", 1), True),
        (("10.0.0.1", 1), False),
        (("example.com", 443), False),
        (("::ffff:203.0.113.1", 1, 0, 0), False),
    ],
)
def test_is_loopback(address: tuple[object, ...], expected: bool) -> None:
    assert is_loopback(address) is expected
