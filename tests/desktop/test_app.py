"""Pencere duman testi: gerçek Tk penceresi + FakeProvider. Ekran yoksa (Linux CI) atlanır."""

from __future__ import annotations

import time
import tkinter as tk
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from codementor.api.state import ApiState
from codementor.desktop import runtime
from codementor.desktop.app import App
from codementor.models.enums import Engine, Language
from tests.integration.conftest import LINKED_LIST


@pytest.fixture
def app(core: ApiState, prefs_dir: Path) -> Iterator[App]:
    try:
        window = App(core, prefs_dir=prefs_dir, check_on_start=False)
    except tk.TclError as exc:  # ekran yok
        pytest.skip(f"Tk penceresi açılamadı: {exc}")
    window.withdraw()
    yield window
    if window.winfo_exists():
        window._closing = True
        window.destroy()


def pump(app: App, until: Callable[[], bool], timeout: float = 30) -> None:
    deadline = time.monotonic() + timeout
    while not until():
        assert time.monotonic() < deadline, "zaman aşımı"
        app.update()
        time.sleep(0.02)


def analyze(app: App) -> None:
    app.analyze()
    assert app.analyze_view.busy
    pump(app, lambda: not app.analyze_view.busy)


def test_full_mentoring_flow(app: App, prefs_dir: Path) -> None:
    view = app.analyze_view
    view.editor.set(LINKED_LIST, Language.C)
    analyze(app)

    report = view.report
    assert report is not None
    assert report.socratic is not None
    assert view.findings.winfo_ismapped() or view.findings.grid_info()
    assert all(g.status in ("done", "skipped") for g in app.tracker.groups())
    marked = view.editor.text.tag_ranges("line_high")
    assert marked, "yüksek önemli bulgu satırı boyanmalı"
    assert runtime.load_source(report.analysis_id, prefs_dir) == LINKED_LIST

    first_level = report.socratic.hint_level
    analyze(app)  # "Bir ipucu daha"
    assert view.report is not None
    assert view.report.socratic is not None
    assert view.report.socratic.hint_level == first_level + 1

    old_session = app.prefs.session_id
    app.restart()
    assert app.prefs.session_id != old_session
    assert view.report is None
    assert runtime.load_prefs(prefs_dir).session_id == app.prefs.session_id


def test_empty_code_shows_error_without_running(app: App) -> None:
    app.analyze_view.editor.set("   \n")
    app.analyze()
    assert not app.bridge.is_running("analyze")
    assert app.analyze_view.summary.winfo_children()


def test_history_reopens_report_with_code(app: App) -> None:
    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    report = app.analyze_view.report
    assert report is not None
    app.analyze_view.editor.set("int baska;\n")
    app.navigate("history")
    assert app.history_view.list.winfo_children()

    app.open_history(report.analysis_id)
    assert app.current_view == "analyze"
    assert app.analyze_view.editor.get() == LINKED_LIST
    assert app.analyze_view.report == report


def test_question_bank_starts_task(app: App) -> None:
    question = next(
        q for q in app.core.questions().filter(Language.CPP) if q.engine is Engine.UNREAL
    )
    app.navigate("questions")
    app.start_question(question)
    view = app.analyze_view
    assert app.current_view == "analyze"
    assert (view.language, view.engine) == (Language.CPP, Engine.UNREAL)
    assert view.question == question
    assert view.task.winfo_manager() == "grid"


def test_language_switch_limits_engines(app: App) -> None:
    view = app.analyze_view
    view.select(Language.CSHARP, Engine.UNITY, None)
    view._on_language("C")
    assert view.engine is Engine.NONE
    assert view.language is Language.C


def test_open_file_detects_language_and_size_limit(app: App, tmp_path: Path) -> None:
    source = tmp_path / "Oyuncu.cs"
    source.write_text("public class Oyuncu {}\n", encoding="utf-8")
    app.load_file(str(source))
    assert app.analyze_view.language is Language.CSHARP
    assert app.analyze_view.editor.get() == "public class Oyuncu {}\n"
    assert app.prefs.recent_files[0] == str(source)

    big = tmp_path / "buyuk.c"
    big.write_text("x" * (app.settings.limits.max_bytes + 1), encoding="utf-8")
    app.load_file(str(big))
    assert app.analyze_view.editor.get() == "public class Oyuncu {}\n"


def test_provider_choice_is_persisted(app: App, prefs_dir: Path) -> None:
    app.check_environment = lambda: None  # type: ignore[method-assign]
    app.choose_provider("claude_cli")
    assert app.provider_name() == "claude_cli"
    assert runtime.load_prefs(prefs_dir).provider == "claude_cli"
    app.choose_provider(None)
    assert app.provider_name() == app.settings.providers.default
