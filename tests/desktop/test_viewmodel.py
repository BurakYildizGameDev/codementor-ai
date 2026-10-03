"""Görünüm modeli: aşama grupları, satır işaretleri, etiketler."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from hypothesis import given
from hypothesis import strategies as st

from codementor.desktop.viewmodel import (
    CATEGORY_LABELS,
    SAMPLES,
    STAGE_GROUPS,
    StageTracker,
    engines_for,
    format_ms,
    language_for_path,
    line_marks,
    report_headline,
    split_findings,
)
from codementor.models.enums import AuditCategory, Engine, Language, Severity
from codementor.models.findings import Diagnostic, Finding
from codementor.models.pipeline import ALL_STAGES, Stage, StageEvent, StageStatus

REPO = Path(__file__).resolve().parents[2]


def event(stage: Stage, status: StageStatus, ms: int = 0) -> StageEvent:
    return StageEvent(analysis_id="A", stage=stage, status=status, duration_ms=ms)


def finding(line: int, end: int | None = None, severity: Severity = Severity.HIGH) -> Finding:
    return Finding(
        id="F-001",
        rule_id=None,
        category=AuditCategory.MEMORY_SAFETY,
        severity=severity,
        line_start=line,
        line_end=end,
        evidence="x",
        description="açıklama",
        source="static",
        confidence=1.0,
    )


def diagnostic(line: int, severity: str = "error") -> Diagnostic:
    return Diagnostic(tool="gcc", severity=severity, line=line, column=None, message="m")  # type: ignore[arg-type]


def statuses(tracker: StageTracker) -> dict[str, str]:
    return {g.key: g.status for g in tracker.groups()}


def test_groups_cover_every_stage_exactly_once() -> None:
    covered = [s for g in STAGE_GROUPS for s in g.stages]
    assert sorted(covered) == sorted(ALL_STAGES)


def test_tracker_starts_pending_and_marks_running_group() -> None:
    tracker = StageTracker()
    assert set(statuses(tracker).values()) == {"pending"}
    tracker.apply(event("cache", "started"))
    assert statuses(tracker)["prepare"] == "running"


def test_partially_seen_group_stays_running_until_finish() -> None:
    tracker = StageTracker()
    tracker.apply(event("cache", "completed", 3))
    assert statuses(tracker)["prepare"] == "running"  # ingest henüz gelmedi
    tracker.apply(event("ingest", "completed", 4))
    view = next(g for g in tracker.groups() if g.key == "prepare")
    assert (view.status, view.duration_ms) == ("done", 7)


def test_finish_marks_unseen_groups_skipped_and_failure_wins() -> None:
    tracker = StageTracker()
    for stage in ("cache", "ingest", "tier0"):
        tracker.apply(event(stage, "completed"))
    tracker.apply(event("tier1", "skipped"))
    tracker.apply(event("facts", "failed"))
    tracker.finish()
    result = statuses(tracker)
    assert result["prepare"] == "done"
    assert result["compile"] == "done"
    assert result["static"] == "failed"
    assert result["analysis"] == "skipped"
    assert tracker.completed_ratio() == 1.0


def test_all_skipped_group_is_skipped() -> None:
    tracker = StageTracker()
    tracker.apply(event("report", "skipped"))
    assert statuses(tracker)["report"] == "skipped"


def test_reset_clears_state() -> None:
    tracker = StageTracker()
    tracker.apply(event("cache", "completed", 10))
    tracker.finish()
    tracker.reset()
    assert tracker.total_ms() == 0
    assert set(statuses(tracker).values()) == {"pending"}


def test_line_marks_merge_messages_and_keep_highest_severity() -> None:
    marks = line_marks(
        [finding(2, severity=Severity.LOW), finding(2, severity=Severity.HIGH)],
        [diagnostic(2, "warning"), diagnostic(3, "note")],
        line_count=5,
    )
    assert [m.line for m in marks] == [2]  # not seviyesindeki tanı işaretlenmez
    assert marks[0].level is Severity.HIGH
    assert len(marks[0].messages) == 3
    assert marks[0].messages[0].startswith("Bellek güvenliği")


def test_line_marks_expand_ranges_and_clip_to_file() -> None:
    marks = line_marks([finding(3, 9), finding(0), finding(42)], [diagnostic(99)], line_count=5)
    assert [m.line for m in marks] == [3, 4, 5]


@given(
    st.lists(st.tuples(st.integers(-5, 60), st.none() | st.integers(-5, 60)), max_size=12),
    st.integers(1, 50),
)
def test_line_marks_stay_inside_file(spans: list[tuple[int, int | None]], count: int) -> None:
    marks = line_marks([finding(s, e) for s, e in spans], [], line_count=count)
    lines = [m.line for m in marks]
    assert lines == sorted(set(lines))
    assert all(1 <= line <= count for line in lines)


def test_category_labels_match_mentor_templates() -> None:
    data = yaml.safe_load((REPO / "data" / "mentor_templates.yaml").read_text(encoding="utf-8"))
    expected = {AuditCategory(k): v["label"] for k, v in data["categories"].items()}
    assert expected == CATEGORY_LABELS


def test_engine_language_compatibility() -> None:
    assert engines_for(Language.C) == [Engine.NONE]
    for language in (Language.PYTHON, Language.HTML, Language.CSS):
        assert engines_for(language) == [Engine.NONE]
    assert Engine.UNREAL in engines_for(Language.CPP)
    assert Engine.UNITY in engines_for(Language.CSHARP)
    assert Engine.UNITY not in engines_for(Language.CPP)


def test_language_for_path() -> None:
    assert language_for_path("a/b/Main.CS") is Language.CSHARP
    assert language_for_path("x.hpp") is Language.CPP
    assert language_for_path("x.h") is Language.C
    assert language_for_path("app.py") is Language.PYTHON
    assert language_for_path("index.HTM") is Language.HTML
    assert language_for_path("style.css") is Language.CSS
    assert language_for_path("notes.txt") is None


def test_format_ms() -> None:
    assert format_ms(850) == "850 ms"
    assert format_ms(4200) == "4.2 sn"
    assert format_ms(65_000) == "1 dk 05 sn"


def test_samples_exist_for_every_language() -> None:
    assert set(SAMPLES) == set(Language)


# ---------------------------------------------------------------- Faz 36: hatalar ve öneriler


def suggestion(line: int) -> Finding:
    return finding(line, severity=Severity.LOW).model_copy(update={"kind": "suggestion"})


def test_split_findings_orders_issues_and_separates_suggestions() -> None:
    low, high = finding(1, severity=Severity.LOW), finding(9, severity=Severity.HIGH)
    issues, suggestions = split_findings([low, suggestion(3), high])
    assert issues == [high, low]  # önem sırası
    assert [f.line_start for f in suggestions] == [3]


def test_line_marks_skip_suggestions() -> None:
    """Editörde yalnız hatalar boyanır; öneri satırı işaretlenmez."""
    assert line_marks([suggestion(2)], [], line_count=5) == []


def test_report_headline_counts_errors_and_suggestions() -> None:
    from types import SimpleNamespace

    def report(findings: list[Finding]) -> Any:
        return SimpleNamespace(
            findings=findings,
            compilation=SimpleNamespace(status=SimpleNamespace(value="passed")),
            meta=SimpleNamespace(cache_hit=False),
        )

    assert report_headline(report([finding(1), suggestion(2)])).startswith(
        "1 hata · 1 öneri · 1 yüksek önem"
    )
    assert report_headline(report([suggestion(2)])).startswith("Hata yok · 1 öneri")
    assert report_headline(report([])).startswith("Hata yok ·")
