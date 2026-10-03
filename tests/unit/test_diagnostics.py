"""Derleyici tanı ayrıştırıcısı testleri (derleyicisiz, kaydedilmiş örnek çıktılarla).

Tanı metinleri derleyici sürümüne göre değişir; testler mesaj metnine değil
satır/kolon/önem düzeyine bakar.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.validation.diagnostics import (
    MAX_DIAGNOSTICS,
    MAX_MESSAGE_CHARS,
    is_missing_header,
    parse_compiler_output,
    parse_roslyn_output,
)

SAMPLES = Path(__file__).resolve().parents[1] / "fixtures" / "tier1"


def _sample(name: str) -> str:
    return (SAMPLES / name).read_text(encoding="utf-8")


def _shape(text: str, tool: str) -> list[tuple[int, int | None, str]]:
    diags, _ = parse_compiler_output(text, tool)  # type: ignore[arg-type]
    assert all(d.tool == tool for d in diags)
    return [(d.line, d.column, d.severity) for d in diags]


def test_parse_gcc_sample() -> None:
    assert _shape(_sample("gcc_c_type_error.txt"), "gcc") == [
        (3, 13, "error"),
        (4, 9, "warning"),
        (7, 6, "error"),
        (6, 6, "note"),
    ]


def test_parse_clang_sample() -> None:
    assert _shape(_sample("clang_cpp_type_error.txt"), "clang") == [
        (5, 9, "error"),
        (6, 9, "warning"),
        (9, 12, "error"),
    ]


@pytest.mark.parametrize(
    ("name", "tool"), [("gcc_missing_header.txt", "gcc"), ("clang_missing_header.txt", "clang")]
)
def test_missing_header_detected(name: str, tool: str) -> None:
    diags, _ = parse_compiler_output(_sample(name), tool)  # type: ignore[arg-type]
    (diag,) = diags
    assert (diag.line, diag.severity) == (1, "error")
    assert is_missing_header(diag.message)


def test_type_errors_are_not_missing_headers() -> None:
    diags, _ = parse_compiler_output(_sample("gcc_c_type_error.txt"), "gcc")
    assert not any(is_missing_header(d.message) for d in diags)


def test_ignores_other_files_and_windows_paths() -> None:
    """Stub başlığı, sistem başlıkları ve `In file included from` satırları atlanır."""
    assert _shape(_sample("clang_unreal_stub.txt"), "clang") == [
        (24, 5, "error"),
        (18, 7, "error"),
    ]


def test_line_without_column() -> None:
    assert _shape("<stdin>:4: warning: no newline at end of file\n", "gcc") == [
        (4, None, "warning")
    ]


def test_message_is_trimmed_and_crlf_tolerated() -> None:
    diags, _ = parse_compiler_output("<stdin>:2:1: error:   bad thing  \r\n", "gcc")
    assert diags[0].message == "bad thing"


def test_caps_at_max() -> None:
    text = "".join(f"<stdin>:{i}:1: error: e{i}\n" for i in range(1, 50))
    diags, truncated = parse_compiler_output(text, "gcc")
    assert len(diags) == MAX_DIAGNOSTICS
    assert truncated


def test_garbage_yields_nothing() -> None:
    assert parse_compiler_output("Segmentation fault\n\x00\x01", "clang") == ([], False)


def test_parse_roslyn_json() -> None:
    diags, truncated = parse_roslyn_output(_sample("roslyn_errors.json"))
    assert not truncated
    assert [(d.tool, d.line, d.column, d.severity) for d in diags] == [
        ("roslyn", 5, 22, "error"),
        ("roslyn", 9, 1, "error"),
        ("roslyn", 2, 2, "warning"),
    ]
    assert diags[0].message.startswith("CS1002")


def test_parse_roslyn_clean() -> None:
    assert parse_roslyn_output(_sample("roslyn_clean.json")) == ([], False)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "not json",
        '{"line": 1}',
        '[{"line": "x", "column": 1, "severity": "error", "id": "A", "message": "m"}]',
        '[{"line": 1, "column": 1, "severity": "fatal", "id": "A", "message": "m"}]',
        '[{"line": 0, "column": 1, "severity": "error", "id": "A", "message": "m"}]',
    ],
)
def test_invalid_roslyn_output(text: str) -> None:
    with pytest.raises(ValueError, match="Roslyn"):
        parse_roslyn_output(text)


def test_linear_on_long_whitespace_message() -> None:
    """Denetim O1: `.*?` + `[ \t]*$` uzun boşlukta karesel geri izliyordu."""
    import time

    line = "<stdin>:1:1: error: a" + " " * 60_000 + "x\n"
    start = time.perf_counter()
    diags, _ = parse_compiler_output(line * 16, "gcc")
    assert time.perf_counter() - start < 0.5
    assert diags[0].message.startswith("a ")


def test_long_message_is_capped() -> None:
    diags, _ = parse_compiler_output("<stdin>:1:1: error: " + "a" * 5000 + "\n", "gcc")
    assert len(diags[0].message) <= MAX_MESSAGE_CHARS + 1
    assert diags[0].message.endswith("…")


def test_parse_zig_clang_crlf_output() -> None:
    """`zig clang` (Faz 29) clang biçimini Windows'ta CRLF ile basar; `\r` mesaja sızmaz."""
    raw = (SAMPLES / "zig_clang_cpp_crlf.txt").read_bytes().decode("utf-8")
    assert "\r\n" in raw  # .gitattributes: -text
    diags, capped = parse_compiler_output(raw, "clang")
    assert [(d.line, d.column, d.severity) for d in diags] == [(5, 19, "error")]
    assert diags[0].message == "expected ';' after expression"
    assert not capped
