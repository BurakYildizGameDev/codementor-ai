"""Big-O ayrıştırıcı testleri (mimari §5.6 dilbilgisi).

Bölüm 1/2.
"""

from __future__ import annotations

import pytest

from codementor.models.bigo import (
    BigOComparisonError,
    BigOParseError,
    parse_bigo,
)
from tests.unit.bigo_support import (
    CHAIN,
)

# ---------------------------------------------------------------- kanonik biçim


@pytest.mark.parametrize("text", ["O(N^2)", "O(n²)", "O(n*n)", "o(n^2)", "n^2"])
def test_quadratic_variants_same_canonical(text: str) -> None:
    assert parse_bigo(text).canonical == "n^2"


@pytest.mark.parametrize(
    "text",
    [
        "n log n",
        "nlogn",
        "N*log(N)",
        "O(n log n)",
        "O(nlogn)",
        "n*log n",
        "n lg n",
        "O(n log2 n)",
        "O(n log_2 n)",
        "O(n log₂ n)",
        "n·log(n)",
        "log(n) * n",
        "O(N LOG N)",
    ],
)
def test_nlogn_variants(text: str) -> None:
    assert parse_bigo(text).canonical == "n log n"


@pytest.mark.parametrize(
    "text", ["log n", "log(n)", "O(log n)", "O(log(n))", "lg n", "ln n", "logn", "log(n^2)"]
)
def test_log_forms_equal(text: str) -> None:
    assert parse_bigo(text).canonical == "log n"


@pytest.mark.parametrize("text", ["O(1)", "1", "O(5)", "O(100)", "3"])
def test_constant_forms(text: str) -> None:
    b = parse_bigo(text)
    assert b.canonical == "1"
    assert b.is_constant
    assert b.variables == frozenset()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("O(3n^2 + n)", "n^2"),
        ("O(2n)", "n"),
        ("n/2", "n"),
        ("n + 1", "n"),
        ("n^2 + n log n + 7", "n^2"),
        ("O(n + log n)", "n"),
        ("(n+1)^2", "n^2"),
        ("2^n + n^100", "2^n"),
        ("n! + 3^n", "n!"),
    ],
)
def test_drops_coefficients_and_lower_terms(text: str, expected: str) -> None:
    assert parse_bigo(text).canonical == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("n^3", "n^3"),
        ("n*n*n", "n^3"),
        ("n³", "n^3"),
        ("n^2 * n", "n^3"),
        ("(n^2)^2", "n^4"),
        ("n^1.5", "n^1.5"),
        ("sqrt(n)", "n^0.5"),
        ("sqrt n", "n^0.5"),
        ("n sqrt(n)", "n^1.5"),
        ("log^2 n", "log^2 n"),
        ("log² n", "log^2 n"),
        ("(log n)^2", "log^2 n"),
        ("log(n)^2", "log^2 n"),
        ("log n * log n", "log^2 n"),
        ("n^2 log n", "n^2 log n"),
        ("2^n", "2^n"),
        ("2ⁿ", "2^n"),
        ("O(2^N)", "2^n"),
        ("(2^n)^2", "4^n"),
        ("2^n * 3^n", "6^n"),
        ("n^2 2^n", "n^2 2^n"),
        ("n * 2^n", "n 2^n"),
        ("n!", "n!"),
        ("O(N!)", "n!"),
        ("log(n!)", "n log n"),
        ("log(2^n)", "n"),
        ("O(n^{2})", "n^2"),
        ("O(n^(2))", "n^2"),
        ("n × n", "n^2"),
        ("  O( n ^ 2 )  ", "n^2"),
    ],
)
def test_single_variable_canonical(text: str, expected: str) -> None:
    assert parse_bigo(text).canonical == expected


# ---------------------------------------------------------------- display


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("n^2", "O(n²)"),
        ("n^3", "O(n³)"),
        ("n^10", "O(n¹⁰)"),
        ("n", "O(n)"),
        ("1", "O(1)"),
        ("nlogn", "O(n log n)"),
        ("log^2 n", "O(log² n)"),
        ("n^2 log n", "O(n² log n)"),
        ("2^n", "O(2^n)"),
        ("n!", "O(n!)"),
        ("n^1.5", "O(n^1.5)"),
        ("V+E", "O(e + v)"),
    ],
)
def test_display_uses_superscript(text: str, expected: str) -> None:
    assert parse_bigo(text).display == expected


def test_str_is_canonical() -> None:
    assert str(parse_bigo("O(N²)")) == "n^2"


# ---------------------------------------------------------------- çok değişkenli


@pytest.mark.parametrize(
    ("text", "expected", "variables"),
    [
        ("O(V+E)", "e + v", {"e", "v"}),
        ("O(E+V)", "e + v", {"e", "v"}),
        ("O(n*m)", "m*n", {"m", "n"}),
        ("O(nm)", "m*n", {"m", "n"}),
        ("O(m n)", "m*n", {"m", "n"}),
        ("O(n*m + n)", "m*n", {"m", "n"}),
        ("O(n^2 + m)", "m + n^2", {"m", "n"}),
        ("O((V+E) log V)", "e*log v + v log v", {"e", "v"}),
        ("O(n log m)", "log m*n", {"m", "n"}),
        ("O(n*m + 1)", "m*n", {"m", "n"}),
    ],
)
def test_multivariable_parse(text: str, expected: str, variables: set[str]) -> None:
    b = parse_bigo(text)
    assert b.canonical == expected
    assert b.variables == frozenset(variables)
    assert not b.is_univariate


@pytest.mark.parametrize(("a", "b"), [("V+E", "n"), ("n*m", "n^2"), ("n", "m"), ("V+E", "V+E")])
def test_multivariable_comparison_raises(a: str, b: str) -> None:
    x, y = parse_bigo(a), parse_bigo(b)
    with pytest.raises(BigOComparisonError, match="karşılaştırılamaz"):
        _ = x < y
    with pytest.raises(BigOComparisonError):
        _ = x >= y


def test_comparison_error_is_value_error() -> None:
    assert issubclass(BigOComparisonError, ValueError)
    assert issubclass(BigOParseError, ValueError)


def test_constant_comparable_with_multivariable() -> None:
    assert parse_bigo("1") < parse_bigo("V+E")
    assert parse_bigo("n*m") > parse_bigo("O(1)")


@pytest.mark.parametrize(
    ("a", "b", "same"),
    [
        ("O(V+E)", "O(E+V)", True),
        ("O(n*m)", "O(m*n)", True),
        ("O(nm)", "n*m", True),
        ("O(n*m)", "O(n+m)", False),
        ("n^2", "O(n*n)", True),
        ("n^2", "n^3", False),
        ("n", "m", False),
        ("n log n", "N*log(N)", True),
    ],
)
def test_same_class(a: str, b: str, same: bool) -> None:
    assert parse_bigo(a).same_class(parse_bigo(b)) is same


def test_ordering_chain() -> None:
    parsed = [parse_bigo(t) for t in CHAIN]
    for i, a in enumerate(parsed):
        for j, b in enumerate(parsed):
            assert (a < b) is (i < j), (CHAIN[i], CHAIN[j])
            assert (a <= b) is (i <= j)
            assert (a > b) is (i > j)
            assert (a >= b) is (i >= j)
    assert sorted(reversed(parsed)) == parsed


@pytest.mark.parametrize(
    ("small", "big"),
    [
        ("log n", "log^2 n"),
        ("log^5 n", "n^0.5"),
        ("n log^3 n", "n^1.5"),
        ("n^2 log n", "n^3"),
        ("n^100", "2^n"),
        ("2^n", "n 2^n"),
        ("n^2 2^n", "3^n"),
        ("100^n", "n!"),
        ("n!", "n n!"),
    ],
)
def test_ordering_edge_cases(small: str, big: str) -> None:
    assert parse_bigo(small) < parse_bigo(big)
    assert parse_bigo(big) > parse_bigo(small)


def test_equality_and_hash() -> None:
    a, b = parse_bigo("O(N²)"), parse_bigo("n*n")
    assert a == b
    assert hash(a) == hash(b)
    assert len({a, b, parse_bigo("n")}) == 2
