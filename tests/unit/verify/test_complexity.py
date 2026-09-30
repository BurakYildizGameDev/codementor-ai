"""§5.6 Big-O normalizasyonu, karmaşıklık çatışması, `is_optimal`."""

from __future__ import annotations

from typing import Literal

import pytest

from codementor.models.bigo import parse_bigo
from codementor.models.facts import ComplexityHint
from codementor.models.llm_output import LLMComplexity
from codementor.models.questions import ExpectedComplexity
from codementor.verify.complexity import (
    check_complexity,
    is_optimal,
    normalize_complexity,
    resolve_conflict,
)

Agreement = Literal["agrees", "conflicts", "no_hint"]
HINT_N2 = ComplexityHint(value="n^2", confidence="high", basis=["iç içe döngü"])


@pytest.mark.parametrize(
    ("text", "canonical"),
    [
        ("O(N²)", "n^2"),
        ("O(n^2)", "n^2"),
        ("O(n*n)", "n^2"),
        ("n^2", "n^2"),
        ("O(n^2) per frame", "n^2"),
        ("O(n) amortized", "n"),
        ("O(n^2) (kare başına)", "n^2"),
        ("Θ(n log n)", "n log n"),
        ("Ω(n)", "n"),
        ("O(n + m)", "m + n"),
        ("n log n, en kötü durumda", "n log n"),
        ("O(1)", "1"),
        ("constant", "1"),
        ("doğrusal", "n"),
    ],
)
def test_normalize(text: str, canonical: str) -> None:
    result = normalize_complexity(text)
    assert result is not None, text
    assert result.canonical == canonical


@pytest.mark.parametrize("text", ["", "hızlı", "karesel civarı, duruma göre", "O(", "O(n"])
def test_unparsable_returns_none(text: str) -> None:
    assert normalize_complexity(text) is None


def test_conflict_states() -> None:
    n, n2 = parse_bigo("n"), parse_bigo("n^2")
    assert resolve_conflict(n2, None, "agrees") == "no_hint"
    assert resolve_conflict(n2, HINT_N2, "agrees") == "agrees"
    assert resolve_conflict(n2, HINT_N2, "conflicts") == "agrees"  # aynı sınıf: çatışma yok
    assert resolve_conflict(n, HINT_N2, "conflicts") == "justified_conflict"
    assert resolve_conflict(n, HINT_N2, "agrees") == "unjustified_conflict"
    assert resolve_conflict(n, HINT_N2, "no_hint") == "unjustified_conflict"


def _complexity(time: str, agreement: Agreement = "agrees", space: str = "O(n)") -> LLMComplexity:
    return LLMComplexity(
        reasoning_steps=["adım"],
        time_complexity=time,
        space_complexity=space,
        optimal_time_target="O(n)",
        agreement=agreement,
    )


def test_unjustified_conflict_requests_repair() -> None:
    check = check_complexity(_complexity("O(n)"), HINT_N2, None)
    assert check.state == "unjustified_conflict"
    assert check.needs_repair
    assert "O(n^2)" in check.errors[0]
    assert "conflicts" in check.errors[0]


def test_justified_conflict_accepted() -> None:
    check = check_complexity(_complexity("O(n)", "conflicts"), HINT_N2, None)
    assert check.state == "justified_conflict"
    assert not check.needs_repair
    assert check.time == "n"


def test_unparsable_requests_repair() -> None:
    check = check_complexity(_complexity("hızlı", space="bilmiyorum"), HINT_N2, None)
    assert check.needs_repair
    assert check.time is None
    assert len(check.errors) == 2
    assert check.errors[0].startswith("complexity.time_complexity:")


def test_unparsable_optimal_target_is_dropped_not_repaired() -> None:
    c = _complexity("O(n^2)").model_copy(update={"optimal_time_target": "bilinmiyor"})
    check = check_complexity(c, HINT_N2, None)
    assert not check.needs_repair
    assert check.optimal_target is None


EXPECTED = ExpectedComplexity(time={"push": "1*", "search": "n"}, space="n")


@pytest.mark.parametrize(
    ("time", "expected", "optimal"),
    [
        ("n", EXPECTED, True),
        ("log n", EXPECTED, True),
        ("n^2", EXPECTED, False),
        ("n", None, None),
        ("1", ExpectedComplexity(time={"push": "1*"}, space="1"), True),
        ("n", ExpectedComplexity(time={"push": "1*"}, space="1"), False),
        ("e + v", ExpectedComplexity(time={"bfs": "V + E"}, space="v"), True),
        ("n*m", ExpectedComplexity(time={"bfs": "V + E"}, space="v"), None),
    ],
)
def test_is_optimal(time: str, expected: ExpectedComplexity | None, optimal: bool | None) -> None:
    assert is_optimal(parse_bigo(time), expected) is optimal
