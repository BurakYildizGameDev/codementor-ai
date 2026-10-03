"""§5.6 Güven skoru formülü."""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from codementor.models.llm_output import Certainty
from codementor.models.verification import AgreementState
from codementor.verify.confidence import (
    AGREEMENT_SCORES,
    LLM_EXACT_CONFIDENCE,
    LLM_SHIFTED_CONFIDENCE,
    analysis_confidence,
    evidence_ratio,
    finding_confidence,
)

STATES: list[AgreementState] = ["agrees", "justified_conflict", "no_hint", "unjustified_conflict"]


@pytest.mark.parametrize(
    ("schema", "state", "evidence", "expected"),
    [
        (True, "agrees", 1.0, 1.0),
        (True, "justified_conflict", 1.0, 0.85),
        (True, "no_hint", 1.0, 0.88),
        (False, "agrees", 1.0, 0.6),
        (True, "agrees", 0.5, 0.85),
        (False, "unjustified_conflict", 0.0, 0.0),
    ],
)
def test_formula_table(
    schema: bool, state: AgreementState, evidence: float, expected: float
) -> None:
    assert analysis_confidence(schema, state, evidence) == pytest.approx(expected)


@given(st.booleans(), st.sampled_from(STATES), st.floats(allow_nan=False, allow_infinity=False))
def test_always_in_unit_interval_and_matches_formula(
    schema: bool, state: AgreementState, evidence: float
) -> None:
    score = analysis_confidence(schema, state, evidence)
    assert 0.0 <= score <= 1.0
    clamped = max(0.0, min(1.0, evidence))
    formula = 0.4 * schema + 0.3 * AGREEMENT_SCORES[state] + 0.3 * clamped
    assert score == pytest.approx(formula, abs=1e-4)


@given(st.integers(min_value=0, max_value=50), st.integers(min_value=0, max_value=50))
def test_evidence_ratio_bounds(matched: int, total: int) -> None:
    ratio = evidence_ratio(min(matched, total), total)
    assert 0.0 <= ratio <= 1.0
    if total == 0:
        assert ratio == 1.0  # doğrulanmamış iddia yok


def test_monotonic_in_each_component() -> None:
    assert analysis_confidence(True, "agrees", 1) > analysis_confidence(False, "agrees", 1)
    assert analysis_confidence(True, "agrees", 1) > analysis_confidence(True, "no_hint", 1)
    assert analysis_confidence(True, "no_hint", 1) > analysis_confidence(
        True, "justified_conflict", 1
    )
    assert analysis_confidence(True, "agrees", 1) > analysis_confidence(True, "agrees", 0.5)


@pytest.mark.parametrize(
    ("certainty", "shifted", "expected"),
    [
        ("high", False, 0.85),
        ("medium", False, 0.7),
        ("low", False, 0.5),
        ("high", True, 0.75),
        ("low", True, 0.4),
    ],
)
def test_certainty_maps_confidence(certainty: Certainty, shifted: bool, expected: float) -> None:
    """Faz 35: rapordaki bulgu güveni modelin kendi beyanından gelir."""
    assert finding_confidence(certainty, shifted=shifted) == pytest.approx(expected)


def test_shifted_lowers_certainty_confidence() -> None:
    for certainty in ("high", "medium", "low"):
        assert finding_confidence(certainty, shifted=True) < finding_confidence(
            certainty, shifted=False
        )


def test_missing_certainty_keeps_legacy() -> None:
    assert finding_confidence(None, shifted=False) == LLM_EXACT_CONFIDENCE
    assert finding_confidence(None, shifted=True) == LLM_SHIFTED_CONFIDENCE
