"""Windows konsolu (cp1254/cp1252) Türkçe ve sembollerde çökmemeli (Faz 27)."""

from __future__ import annotations

import io

from rich.console import Console

from codementor.cli.encoding import ensure_utf8


def _stream(encoding: str) -> io.TextIOWrapper:
    return io.TextIOWrapper(io.BytesIO(), encoding=encoding, newline="")


def test_cp1254_stream_switched_to_utf8_and_rich_prints() -> None:
    stream = _stream("cp1254")
    ensure_utf8(stream)
    assert stream.encoding.lower().replace("-", "") == "utf8"
    Console(file=stream, force_terminal=False, width=80).print("✗ taslak → ş ğ ı İ")
    stream.flush()
    data = stream.buffer.getvalue()  # type: ignore[attr-defined]
    assert "✗ taslak → ş ğ ı İ".encode() in data


def test_utf8_stream_untouched() -> None:
    stream = _stream("utf-8")
    ensure_utf8(stream)
    assert stream.encoding == "utf-8"


def test_streams_without_reconfigure_are_ignored() -> None:
    ensure_utf8(io.StringIO())  # pytest yakalama akışları gibi: hata vermez
    ensure_utf8(None)
