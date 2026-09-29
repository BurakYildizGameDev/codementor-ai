"""K0 normalizasyon testleri (mimari §5.1)."""

from __future__ import annotations

import hashlib
import re

import pytest
from hypothesis import given
from hypothesis import strategies as st

from codementor.config import LimitsSettings
from codementor.ingest.errors import (
    CodeTooLargeError,
    EmptyCodeError,
    IngestError,
    InvalidEncodingError,
)
from codementor.ingest.normalize import escape_invisible_breaks, normalize
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint, NormalizedCode

HINT = LanguageHint(language=Language.C, engine=Engine.NONE)
PREFIX = re.compile(r"^ *\d+ \|( |$)")


def _n(raw: str | bytes, **limits: int) -> NormalizedCode:
    return normalize(raw, HINT, limits=LimitsSettings(**limits) if limits else None)


# ---------------------------------------------------------------- metin dönüşümü


def test_crlf_and_lone_cr_become_lf() -> None:
    code = _n("int a;\r\nint b;\rint c;\n")
    assert code.text == "int a;\nint b;\nint c;\n"
    assert code.lines == ["int a;", "int b;", "int c;"]


def test_bom_removed_from_str_and_bytes() -> None:
    assert _n("﻿int x;").text == "int x;"
    assert _n(b"\xef\xbb\xbfint x;").text == "int x;"


def test_bytes_decoded_as_utf8() -> None:
    assert _n('char *s = "ğüş";'.encode()).lines == ['char *s = "ğüş";']


def test_invalid_utf8_rejected() -> None:
    with pytest.raises(InvalidEncodingError, match="UTF-8") as exc:
        _n(b"int x = 1; \xff\xfe")
    assert exc.value.status_code == 422


def test_lone_surrogate_rejected_as_encoding_error() -> None:
    """JSON'dan gelen `"\\ud800"` geçerli bir Python str'dir; 500 değil 422 dönmeli."""
    with pytest.raises(InvalidEncodingError, match="Unicode") as exc:
        _n("int x; /* " + chr(0xD800) + " */")
    assert exc.value.status_code == 422


def test_numbered_view_escapes_invisible_line_breaks() -> None:
    """Sahte satır numarası enjeksiyonu: U+2028 LLM'e satır sonu gibi görünmemeli."""
    fake = "int a;" + chr(0x2028) + " 2 | int sahte;"
    code = _n(fake + "\nint b;")
    assert code.lines[0] == fake  # metnin kendisi değişmez
    first, second = code.numbered_view.split("\n")
    assert chr(0x2028) not in code.numbered_view
    assert first == "1 | int a;\\u2028 2 | int sahte;"
    assert second == "2 | int b;"


def test_raw_shortcut_reports_characters_for_str() -> None:
    with pytest.raises(CodeTooLargeError, match="karakter"):
        _n("x" * 1_000, max_bytes=100)


def test_nul_byte_rejected() -> None:
    with pytest.raises(InvalidEncodingError, match="ikili"):
        _n("int x;\x00")


@pytest.mark.parametrize("raw", ["", "   ", "\n\n\t\n", b"", "﻿"])
def test_empty_code_rejected(raw: str | bytes) -> None:
    with pytest.raises(EmptyCodeError, match="boş"):
        _n(raw)


def test_tabs_and_trailing_spaces_preserved() -> None:
    code = _n("int main(void) {\n\treturn 0;  \n}")
    assert code.lines[1] == "\treturn 0;  "


def test_trailing_newline_does_not_add_line() -> None:
    assert len(_n("a;\nb;\n").lines) == 2
    assert len(_n("a;\nb;").lines) == 2
    assert len(_n("a;\nb;\n\n").lines) == 3


def test_unicode_line_separators_are_not_newlines() -> None:
    """tree-sitter yalnızca \\n sayar; satır numaraları onunla uyumlu olmalı."""
    separators = chr(0x2028) + chr(0x85) + chr(0x0C)
    code = _n(f"int a; /* {separators} */\nint b;")
    assert len(code.lines) == 2


# ---------------------------------------------------------------- sınırlar


def test_line_limit_boundary() -> None:
    assert len(_n("a;\nb;\nc;\n", max_lines=3).lines) == 3
    with pytest.raises(CodeTooLargeError, match=r"4 satır.*en fazla 3") as exc:
        _n("a;\nb;\nc;\nd;", max_lines=3)
    assert exc.value.status_code == 413


def test_byte_limit_counts_utf8_bytes() -> None:
    assert _n("ğğğğğ", max_bytes=10).text == "ğğğğğ"  # 10 bayt
    with pytest.raises(CodeTooLargeError, match=r"12 bayt.*en fazla 10"):
        _n("ğğğğğğ", max_bytes=10)


def test_byte_limit_applies_after_crlf_normalization() -> None:
    assert _n("a;\r\nb;", max_bytes=5).text == "a;\nb;"


def test_huge_raw_input_rejected_before_decoding() -> None:
    with pytest.raises(CodeTooLargeError):
        _n(b"x" * 1_000_000, max_bytes=100)


def test_errors_share_base_class() -> None:
    for cls in (CodeTooLargeError, EmptyCodeError, InvalidEncodingError):
        assert issubclass(cls, IngestError)
        assert issubclass(cls, ValueError)


def test_default_limits_from_config() -> None:
    with pytest.raises(CodeTooLargeError, match="600"):
        normalize("x;\n" * 601, HINT)


# ---------------------------------------------------------------- numaralı görünüm


def test_numbered_view_single_digit() -> None:
    code = _n("a;\nb;")
    assert code.numbered_view == "1 | a;\n2 | b;"


def test_numbered_view_right_aligned() -> None:
    code = _n("\n".join(f"s{i};" for i in range(1, 11)))
    view = code.numbered_view.split("\n")
    assert view[0] == " 1 | s1;"
    assert view[9] == "10 | s10;"
    assert len({line.index("|") for line in view}) == 1


def test_numbered_view_three_digits_and_empty_lines() -> None:
    code = _n("x;\n" + "\n" * 98 + "y;")
    view = code.numbered_view.split("\n")
    assert len(view) == len(code.lines) == 100
    assert view[0] == "  1 | x;"
    assert view[1] == "  2 |"
    assert view[99] == "100 | y;"


@given(
    st.lists(
        st.text(
            alphabet=st.characters(blacklist_characters="\r\n\x00", blacklist_categories=["Cs"]),
            max_size=30,
        ),
        min_size=1,
        max_size=40,
    ).filter(lambda lines: "\n".join(lines).removeprefix("﻿").strip() != "")
)
def test_numbered_view_roundtrip(lines: list[str]) -> None:
    text = "\n".join(lines).removeprefix("﻿")
    code = normalize(text, HINT, limits=LimitsSettings(max_lines=100, max_bytes=100_000))
    view = code.numbered_view.split("\n")
    assert len(view) == len(code.lines)
    expected = [escape_invisible_breaks(line) for line in code.lines]
    assert [PREFIX.sub("", line, count=1) for line in view] == expected
    assert [int(line.split("|")[0]) for line in view] == list(range(1, len(view) + 1))


# ---------------------------------------------------------------- özet ve dil


def test_sha256_matches_text_and_ignores_line_endings() -> None:
    a, b = _n("int a;\r\nint b;\r\n"), _n("int a;\nint b;\n")
    assert a.sha256 == b.sha256 == hashlib.sha256(b"int a;\nint b;\n").hexdigest()


def test_hint_sets_language_and_engine() -> None:
    code = normalize("x = 1;", LanguageHint(language=Language.CSHARP, engine=Engine.UNITY))
    assert (code.language, code.engine) == (Language.CSHARP, Engine.UNITY)


def test_detection_used_without_hint() -> None:
    code = normalize("using UnityEngine;\npublic class A : MonoBehaviour {}")
    assert (code.language, code.engine) == (Language.CSHARP, Engine.UNITY)
