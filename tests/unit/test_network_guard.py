"""Ağ koruması (Faz 50): loopback dışına bağlanan test düşer, loopback serbest."""

from __future__ import annotations

import asyncio
import socket

import pytest

from tests.network_guard import NetworkBlockedError, is_local_host, is_loopback


def test_async_connect_blocked() -> None:
    """Tam tarama #8: Windows Proactor `ConnectEx` yolu da düşer (eskiden zaman aşımına giderdi)."""

    async def attempt() -> None:
        await asyncio.wait_for(asyncio.open_connection("203.0.113.1", 443), timeout=2)

    with pytest.raises(NetworkBlockedError, match="ağa çıkmaya"):
        asyncio.run(attempt())


def test_async_loopback_allowed() -> None:
    async def round_trip() -> bytes:
        async def echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            writer.write(await reader.read(4))
            await writer.drain()
            writer.close()

        server = await asyncio.start_server(echo, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        async with server:
            reader, writer = await asyncio.open_connection("127.0.0.1", port)
            writer.write(b"ping")
            await writer.drain()
            data = await reader.read(4)
            writer.close()
            await writer.wait_closed()
            return data

    assert asyncio.run(round_trip()) == b"ping"


def test_dns_lookup_blocked() -> None:
    with pytest.raises(NetworkBlockedError, match="DNS"):
        socket.getaddrinfo("example.com", 443)


def test_local_lookups_allowed() -> None:
    assert socket.getaddrinfo("127.0.0.1", 80)
    assert socket.getaddrinfo("localhost", 80)


@pytest.mark.parametrize(
    ("host", "expected"),
    [
        (None, True),
        ("", True),
        ("localhost", True),
        ("10.0.0.1", True),  # IP literali çözümleme yapmaz; bağlanma connect korumasında düşer
        ("::1", True),
        (b"127.0.0.1", True),
        ("example.com", False),
        ("api.anthropic.com", False),
    ],
)
def test_is_local_host(host: object, expected: bool) -> None:
    assert is_local_host(host) is expected


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
