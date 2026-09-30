"""Zorluk → mentorluk ayarı (mimari §5.4.3)."""

from __future__ import annotations

from codementor.models.enums import Difficulty
from codementor.models.prompts import MentoringProfile

MAX_HINT_LEVEL = 3

# zorluk → (başlangıç ipucu seviyesi, en az soru, en çok soru, kavram adı hangi denemeden itibaren)
_TABLE: dict[Difficulty, tuple[int, int, int, int]] = {
    Difficulty.VERY_EASY: (2, 2, 3, 1),
    Difficulty.EASY: (2, 2, 3, 1),
    Difficulty.MEDIUM: (1, 2, 2, 2),
    Difficulty.HARD: (1, 1, 2, 3),
}
FREE_MODE_DIFFICULTY = Difficulty.MEDIUM


def mentoring_profile(difficulty: Difficulty | None, attempt: int = 1) -> MentoringProfile:
    """Her yeni gönderim ipucu seviyesini 1 artırır (en fazla 3); soru yoksa orta zorluk."""
    if attempt < 1:
        raise ValueError(f"Deneme sayısı en az 1 olmalı: {attempt}")
    start, low, high, concept_from = _TABLE[difficulty or FREE_MODE_DIFFICULTY]
    return MentoringProfile(
        hint_level=min(MAX_HINT_LEVEL, start + attempt - 1),
        min_questions=low,
        max_questions=high,
        name_concept=attempt >= concept_from,
    )
