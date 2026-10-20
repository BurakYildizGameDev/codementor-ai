"""Big-O ayrıştırıcı testleri (mimari §5.6 dilbilgisi).

Bölüm 2/2.
"""

from __future__ import annotations

import contextlib
import time

import pytest
from hypothesis import given
from hypothesis import strategies as st

from codementor.models.bigo import (
    BigO,
    BigOParseError,
    collapse_variables,
    parse_bigo,
)
from tests.unit.bigo_support import (
    univariate_texts,
    univariates,
)


def test_eq_with_other_types_is_false() -> None:
    assert parse_bigo("n") != "n"


# ------------------------------------------------- Θ/Ω sarmalayıcı, max, log log (Faz H3)


@pytest.mark.parametrize("text", ["Θ(n^2)", "Ω(n^2)", "θ(n^2)", "ω(n²)", "Θ(N²)"])
def test_theta_and_omega_wrappers_inner_expression(text: str) -> None:
    """`Θ/Ω` (ve küçük harfli biçimleri) içindeki ifadeye indirgenir; gösterim O'ya döner."""
    value = parse_bigo(text)
    assert value.canonical == "n^2"
    assert value.display == "O(n²)"


@pytest.mark.parametrize("text", ["Θ(n log n)", "Ω(n log n)"])
def test_theta_omega_are_stripped_like_o(text: str) -> None:
    assert parse_bigo(text) == parse_bigo("n log n")


@pytest.mark.parametrize("text", ["n * Θ(m)", "Θ(n) + m", "n^Θ(2)"])
def test_wrapper_only_at_expression_start(text: str) -> None:
    """Sarmalayıcı yalnızca ifadenin tamamını sarabilir; ortada geçerse reddedilir."""
    with pytest.raises(BigOParseError):
        parse_bigo(text)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("max(n, m)", "m + n"),
        ("max(V, E)", "e + v"),
        ("max(n, n)", "n"),
        ("max(n, m, k)", "k + m + n"),
        ("max(n^2, n log n)", "n^2"),
        ("2*max(n, m)", "m + n"),
    ],
)
def test_max_is_normalized_to_sum(text: str, expected: str) -> None:
    """Big-O'da `max(a, b) = Θ(a + b)`: çok değişkenli toplam gibi temsil edilir."""
    assert parse_bigo(text).canonical == expected


@pytest.mark.parametrize("text", ["max(n)", "max()", "max n", "max(n, m", "max(n m)"])
def test_max_requires_two_arguments_and_parentheses(text: str) -> None:
    with pytest.raises(BigOParseError):
        parse_bigo(text)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("log log n", "log log n"),
        ("log(log n)", "log log n"),
        ("log(log^2 n)", "log log n"),  # log((log n)^2) = 2·log log n = Θ(log log n)
        ("log log n log n", "log n log log n"),
        ("n log log n", "n log log n"),
        ("(log log n)^2", "(log log n)^2"),
        ("log log n + n", "n"),
        ("log^2 n", "log^2 n"),
    ],
)
def test_log_log_n(text: str, expected: str) -> None:
    assert parse_bigo(text).canonical == expected


def test_log_log_ordering_and_roundtrip() -> None:
    """`1 < log log n < log n < n`; kanonik biçim ve gösterim geri ayrıştırılabilir."""
    constant = parse_bigo("1")
    log_log = parse_bigo("log log n")
    log = parse_bigo("log n")
    linear = parse_bigo("n")
    assert constant < log_log < log < linear
    assert log_log.display == "O(log log n)"
    assert parse_bigo(log_log.canonical) == log_log
    assert parse_bigo(parse_bigo("(log log n)^2").display) == parse_bigo("(log log n)^2")


def test_log_log_log_is_rejected() -> None:
    with pytest.raises(BigOParseError, match="log log log"):
        parse_bigo("log log log n")


def test_variable_exponent_of_variable_base_is_rejected() -> None:
    """`n^k` modellenmiyor (sembolik üs); hata mesajı sayısal tabanı önerir."""
    with pytest.raises(BigOParseError, match="değişken üs"):
        parse_bigo("n^k")


def test_wrapper_and_max_survive_collapse_variables() -> None:
    """`collapse_variables` tüm değişkenleri `n` yapar; `log` belirteçleri korunur."""
    assert collapse_variables(parse_bigo("max(n, m)")).canonical == "n"
    assert collapse_variables(parse_bigo("n log log n")).canonical == "n log log n"


def test_hostile_overlong_input_fails_fast() -> None:
    """40 KB kötü niyetli girdi (uzunluk sınırı) hızlı reddedilir (Faz H3 süre testi)."""
    hostile = "(" * 20_000 + "n" + ")" * 20_000
    start = time.perf_counter()
    with pytest.raises(BigOParseError, match="uzun"):
        parse_bigo(hostile)
    assert time.perf_counter() - start < 0.1


@pytest.mark.parametrize("text", ["Θ(" * 20 + "n" + ")" * 20, "max(" * 20 + "n" + ")" * 20])
def test_hostile_nesting_within_limit_fails_fast(text: str) -> None:
    """Sınır içindeki aşırı iç içe girdi özyineleme hatası yerine hızlı hata verir."""
    start = time.perf_counter()
    with pytest.raises(BigOParseError):
        parse_bigo(text)
    assert time.perf_counter() - start < 0.1


# ---------------------------------------------------------------- hatalar


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "O(",
        "O()",
        "O(n))",
        "n^",
        "n^n",
        "foo(n)",
        "n - 1",
        "n/m",
        "e^n",
        "0.5^n",
        "log(V+E)",
        "(n+m)^0.5",
        "n^-1",
        "?",
        "n $",
        "2^(n^2)",
        "(2n)!",
        "n^1.5!",
    ],
)
def test_invalid_raises_parse_error(text: str) -> None:
    with pytest.raises(BigOParseError):
        parse_bigo(text)


def test_parse_error_message_is_turkish_and_quotes_input() -> None:
    with pytest.raises(BigOParseError, match="ayrıştırılamadı") as exc_info:
        parse_bigo("n $")
    assert "n $" in str(exc_info.value)


def test_non_string_rejected() -> None:
    with pytest.raises(TypeError):
        parse_bigo(42)  # type: ignore[arg-type]


@given(univariates, univariates, univariates)
def test_order_transitive(a: BigO, b: BigO, c: BigO) -> None:
    if a < b and b < c:
        assert a < c
    if a <= b and b <= c:
        assert a <= c


@given(univariates, univariates)
def test_order_trichotomy(a: BigO, b: BigO) -> None:
    assert [a < b, a == b, a > b].count(True) == 1
    assert (a <= b) == (a < b or a == b)
    assert (a < b) == (b > a)


@given(univariates)
def test_canonical_roundtrip(b: BigO) -> None:
    assert parse_bigo(b.canonical) == b


@given(univariates)
def test_display_roundtrip(b: BigO) -> None:
    assert parse_bigo(b.display) == b


@given(univariate_texts())
def test_wrapper_and_coefficient_invariance(text: str) -> None:
    base = parse_bigo(text)
    assert parse_bigo(f"O({text})") == base
    assert parse_bigo(f"5*({text})") == base
    assert parse_bigo(f"({text}) + 1") == base


@given(univariates, univariates)
def test_sum_is_max(a: BigO, b: BigO) -> None:
    total = parse_bigo(f"({a.canonical}) + ({b.canonical})")
    assert total == max(a, b)


@given(univariates, univariates, univariates)
def test_product_monotonic(a: BigO, b: BigO, c: BigO) -> None:
    if a <= b:
        ac = parse_bigo(f"({a.canonical})*({c.canonical})")
        bc = parse_bigo(f"({b.canonical})*({c.canonical})")
        assert ac <= bc


@given(st.text(max_size=20))
def test_parse_never_crashes_unexpectedly(text: str) -> None:
    with contextlib.suppress(BigOParseError):
        parse_bigo(text)


@pytest.mark.parametrize("text", ["O(size)", "abs(n)", "O(len)"])
def test_unknown_words_rejected(text: str) -> None:
    with pytest.raises(BigOParseError, match="tanımsız"):
        parse_bigo(text)


def test_overlong_input_rejected() -> None:
    with pytest.raises(BigOParseError, match="uzun"):
        parse_bigo("(" * 150 + "n" + ")" * 150)


@pytest.mark.parametrize("text", ["n^1000", "(2^n)^5000", "(n+m)^500"])
def test_huge_exponents_rejected(text: str) -> None:
    with pytest.raises(BigOParseError, match="üs"):
        parse_bigo(text)


# ------------------------------------------------------------------ parse_cost (amortize `*`)


@pytest.mark.parametrize(
    ("text", "canonical", "amortized"),
    [("1*", "1", True), ("n log n", "n log n", False), (" n* ", "n", True), ("O(1)*", "1", True)],
)
def test_parse_cost(text: str, canonical: str, amortized: bool) -> None:
    from codementor.models.bigo import parse_cost

    value, flag = parse_cost(text)
    assert value.canonical == canonical
    assert flag is amortized


def test_parse_cost_rejects_garbage() -> None:
    from codementor.models.bigo import BigOParseError, parse_cost

    with pytest.raises(BigOParseError):
        parse_cost("**")


@pytest.mark.parametrize(
    ("text", "expected"),
    [("n*m", "n^2"), ("n + m", "n"), ("m log m", "n log n"), ("1", "1"), ("k^3", "n^3")],
)
def test_collapse_variables(text: str, expected: str) -> None:
    """Faz 39: tüm değişkenler `n`'ye indirgenir; `log` korunur."""
    assert collapse_variables(parse_bigo(text)) == parse_bigo(expected)
