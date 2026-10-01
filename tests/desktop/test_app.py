"""Pencere duman testi: gerçek Tk penceresi + FakeProvider. Ekran yoksa (Linux CI) atlanır."""

from __future__ import annotations

import gc
import os
import time
import tkinter as tk
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from codementor.api.state import ApiState
from codementor.desktop import connections_controller as controller_module
from codementor.desktop import runtime
from codementor.desktop.app import App
from codementor.desktop.connections import KeyStore, Probe
from codementor.models.enums import Engine, Language
from codementor.models.provider import ProviderStatus
from tests.integration.conftest import LINKED_LIST

TK_ATTEMPTS = 3


@pytest.fixture
def app(core: ApiState, prefs_dir: Path, store: KeyStore) -> Iterator[App]:
    window = None
    error: tk.TclError | None = None
    # Windows'ta art arda kurulan Tk köklerinde Tcl `init.tcl`'i ara sıra okuyamıyor
    # ("No error"); önceki kökün artıkları toplanıp yeniden denenir. Ekran yoksa atlanır.
    for _ in range(TK_ATTEMPTS):
        gc.collect()
        try:
            window = App(core, prefs_dir=prefs_dir, check_on_start=False, key_store=store)
            break
        except tk.TclError as exc:
            error = exc
            time.sleep(0.2)
    if window is None:
        pytest.skip(f"Tk penceresi açılamadı: {error}")
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


def test_model_choice_overrides_config_and_persists(app: App, prefs_dir: Path) -> None:
    app.connections.check = lambda _name: None  # type: ignore[method-assign]
    app.connections.set_model("ollama", "qwen2.5-coder:14b")
    assert app.settings.providers.ollama.model == "qwen2.5-coder:14b"
    assert app.core.settings is app.settings
    assert app.base_settings.providers.ollama.model != "qwen2.5-coder:14b"
    assert runtime.load_prefs(prefs_dir).providers["ollama"].model == "qwen2.5-coder:14b"
    assert app.settings_view.cards["ollama"].model.get() == "qwen2.5-coder:14b"

    app.connections.set_base_url("ollama", "ftp://yanlis")
    assert app.settings.providers.ollama.base_url != "ftp://yanlis"


def test_default_provider_switch(app: App, prefs_dir: Path) -> None:
    app.connections.check = lambda _name: None  # type: ignore[method-assign]
    app.connections.make_default("claude_cli")
    assert app.provider_name() == "claude_cli"
    assert runtime.load_prefs(prefs_dir).provider == "claude_cli"
    assert "claude_cli" in app.analyze_view.provider_badge.cget("text")
    app.connections.make_default(app.base_default())
    assert runtime.load_prefs(prefs_dir).provider is None


def test_api_key_saved_to_vault_and_process_env(app: App, store: KeyStore) -> None:
    app.connections.check = lambda _name: None  # type: ignore[method-assign]
    app.connections.save_key("openai", "sk-test-1234567890")
    assert store.get("openai") == "sk-test-1234567890"
    assert os.environ["OPENAI_API_KEY"] == "sk-test-1234567890"
    assert "kasasında" in app.settings_view.cards["openai"].key_label.cget("text")

    app.connections.delete_key("openai")
    assert store.get("openai") is None
    assert "OPENAI_API_KEY" not in os.environ


def test_probe_results_update_cards_and_sidebar(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_probe(name: str, _settings: object) -> Probe:
        ready = name == "ollama"
        models = ["qwen2.5-coder:1.5b", "qwen2.5-coder:14b"] if ready else []
        return Probe(ProviderStatus(name=name, model="m", ready=ready, detail="d"), models)

    monkeypatch.setattr(controller_module, "probe", fake_probe)
    app.connections.make_default("ollama")
    app.check_environment()
    pump(app, lambda: len(app.connections.probes) == 6)
    card = app.settings_view.cards["ollama"]
    assert card.status_pill.cget("text").strip() == "hazır"
    assert "qwen2.5-coder:14b" in card.model.cget("values")
    assert app.settings_view.cards["openai"].status_pill.cget("text").strip() == "hazır değil"
    assert app.sidebar.status_text.cget("text") == "ollama"
