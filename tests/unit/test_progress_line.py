"""Faz 33: CLI ilerleme satırında aşama adı, canlı süre ve token."""

from __future__ import annotations

from codementor.report.progress import STAGE_LABELS, ProgressLine

from codementor.models.pipeline import ALL_STAGES, StageEvent


def _event(stage: str, status: str, tokens: int = 0) -> StageEvent:
    return StageEvent.model_validate(
        {"analysis_id": "A", "stage": stage, "status": status, "tokens": tokens}
    )


def test_every_stage_has_turkish_label() -> None:
    assert set(STAGE_LABELS) == set(ALL_STAGES)


def test_line_shows_stage_elapsed_and_tokens() -> None:
    line = ProgressLine(started=100.0)
    assert line.text(now=100.0) == "Analiz başlıyor… · 0,0 sn"
    line.on_event(_event("llm_a", "started"))
    assert line.text(now=102.5) == "LLM analiz · 2,5 sn"
    line.on_event(_event("llm_a", "completed", tokens=4512))
    line.on_event(_event("prompt_b", "started"))
    line.on_event(_event("llm_b", "started"))
    assert line.text(now=110.25) == "LLM mentorluk · 10,2 sn · 4512 token"


def test_skipped_stage_does_not_change_label() -> None:
    line = ProgressLine(started=0.0)
    line.on_event(_event("tier0", "started"))
    line.on_event(_event("tier1", "skipped"))
    assert line.text(now=1.0).startswith("Sözdizimi")
