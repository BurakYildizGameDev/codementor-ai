"""Zorluk → mentorluk ayarı tablosu (mimari §5.4.3)."""

from __future__ import annotations

from itertools import pairwise

import pytest

from codementor.models.enums import Difficulty
from codementor.prompts.mentoring import mentoring_profile

# (zorluk, deneme) → (ipucu seviyesi, en az soru, en çok soru, kavram adı)
TABLE = [
    (Difficulty.VERY_EASY, 1, 2, 2, 3, True),
    (Difficulty.EASY, 1, 2, 2, 3, True),
    (Difficulty.MEDIUM, 1, 1, 2, 2, False),
    (Difficulty.MEDIUM, 2, 2, 2, 2, True),
    (Difficulty.HARD, 1, 1, 1, 2, False),
    (Difficulty.HARD, 2, 2, 1, 2, False),
    (Difficulty.HARD, 3, 3, 1, 2, True),
]


@pytest.mark.parametrize(("difficulty", "attempt", "level", "lo", "hi", "concept"), TABLE)
def test_table(
    difficulty: Difficulty, attempt: int, level: int, lo: int, hi: int, concept: bool
) -> None:
    profile = mentoring_profile(difficulty, attempt)
    assert profile.hint_level == level
    assert (profile.min_questions, profile.max_questions) == (lo, hi)
    assert profile.name_concept is concept


@pytest.mark.parametrize("difficulty", list(Difficulty))
def test_level_increases_per_attempt_and_caps_at_three(difficulty: Difficulty) -> None:
    levels = [mentoring_profile(difficulty, attempt).hint_level for attempt in range(1, 8)]
    assert levels == sorted(levels)
    assert levels[-1] == 3
    assert all(b - a <= 1 for a, b in pairwise(levels))


def test_free_mode_defaults_to_medium() -> None:
    assert mentoring_profile(None, 1) == mentoring_profile(Difficulty.MEDIUM, 1)


def test_attempt_must_be_positive() -> None:
    with pytest.raises(ValueError, match="en az 1"):
        mentoring_profile(Difficulty.EASY, 0)
