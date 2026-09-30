"""§5.6 Satır aralığı ve kanıt eşleşmesi."""

from __future__ import annotations

import time

import pytest

from codementor.verify.lines import check_line_range, match_evidence, normalize_evidence

LINES = [
    "using System.Collections.Generic;",  # 1
    "",  # 2
    "class A {",  # 3
    "    void Update() {",  # 4
    "        var x = new List<int>();",  # 5
    "        for (int i = 0; i <= n; i++)",  # 6
    "            total += a[i];",  # 7
    "    }",  # 8
    "}",  # 9
]


@pytest.mark.parametrize(
    ("start", "end", "ok"),
    [
        (1, None, True),
        (9, None, True),
        (3, 5, True),
        (0, None, False),
        (10, None, False),
        (5, 3, False),
        (8, 12, False),
    ],
)
def test_line_range(start: int, end: int | None, ok: bool) -> None:
    assert check_line_range(start, end, len(LINES)) is ok


def test_exact_match_not_shifted() -> None:
    m = match_evidence("i <= n", 6, None, LINES)
    assert m.found
    assert m.line_start == 6
    assert not m.shifted


@pytest.mark.parametrize("reported", [4, 5, 7, 8])
def test_shift_within_two_lines_corrected(reported: int) -> None:
    m = match_evidence("i <= n", reported, None, LINES)
    assert m.found
    assert m.line_start == 6
    assert m.shifted is (reported != 6)


@pytest.mark.parametrize("reported", [3, 9])
def test_shift_of_three_lines_not_found(reported: int) -> None:
    assert not match_evidence("i <= n", reported, None, LINES).found


def test_missing_evidence_not_found() -> None:
    assert not match_evidence("HashSet<int> seen", 5, None, LINES).found


@pytest.mark.parametrize(
    "evidence",
    [
        "var x=new List<int>()",  # plan tuzağı: boşluk + noktalı virgül
        "var x = new List<int>();",
        "var   x =\tnew List<int>( );",
        "Line 5: var x = new List<int>();",
        "satır 5 - var x = new List<int>()",
        " 5 | var x = new List<int>();",
        "`var x = new List<int>();`",
        "var x = new List&lt;int>();",  # Faz 8 kaçışı
        "var x = ... List<int>()",  # üç nokta: parçalar sırayla
    ],
)
def test_whitespace_semicolon_and_prefix_insensitive(evidence: str) -> None:
    m = match_evidence(evidence, 5, None, LINES)
    assert m.found, evidence
    assert m.line_start == 5


def test_pipe_expression_kept_when_prefix_strip_fails() -> None:
    lines = ["int flags = 0 | FLAG_A;"]
    assert match_evidence("0 | FLAG_A", 1, None, lines).found


def test_multiline_evidence_sets_line_end() -> None:
    m = match_evidence("for (int i = 0; i <= n; i++)\n    total += a[i];", 6, None, LINES)
    assert m.found
    assert (m.line_start, m.line_end) == (6, 7)


def test_reported_range_is_searched() -> None:
    m = match_evidence("total += a[i];", 4, 5, LINES)  # aralık 4-5, ±2 → 7 dahil
    assert m.found
    assert m.line_start == 7


def test_closest_occurrence_wins() -> None:
    lines = ["x++;", "y();", "x++;", "z();", "x++;"]
    assert match_evidence("x++", 4, None, lines).line_start in {3, 5}
    assert match_evidence("x++", 1, None, lines).line_start == 1


@pytest.mark.parametrize("evidence", ["", "   ", ";", "...", "``"])
def test_trivial_evidence_rejected(evidence: str) -> None:
    assert not match_evidence(evidence, 5, None, LINES).found


def test_normalize_evidence() -> None:
    assert normalize_evidence("Line 12: foo();") == "foo();"
    assert normalize_evidence('"bar"') == "bar"
    assert normalize_evidence("a &lt; b") == "a < b"


def test_long_single_line_is_fast() -> None:
    """§12: 40 KB'lık tek satırda çok sayıda eşleşme karesel olmamalı."""
    lines = ["a" * 40_000]
    start = time.perf_counter()
    m = match_evidence("aa", 1, None, lines)
    assert m.found
    assert time.perf_counter() - start < 0.5
