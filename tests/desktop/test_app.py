"""Pencere duman testi: gerçek Tk penceresi + FakeProvider. Ekran yoksa (Linux CI) atlanır."""

from __future__ import annotations

import gc
import os
import sys
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
from codementor.desktop.views import analyze_view as analyze_view_module
from codementor.models.enums import Engine, Language
from codementor.models.provider import ProviderStatus
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from tests.desktop.conftest import StallingProvider
from tests.integration.conftest import LINKED_LIST

TK_ATTEMPTS = 3
HTML_PAGE = '<html>\n<img src="a.png">\n</html>\n'
PY_LINE = "print('merhaba')\n"


@pytest.fixture
def app(core: ApiState, prefs_dir: Path, store: KeyStore) -> Iterator[App]:
    yield from _open(core, prefs_dir, store)


@pytest.fixture
def stalled_app(stalled_core: ApiState, prefs_dir: Path, store: KeyStore) -> Iterator[App]:
    yield from _open(stalled_core, prefs_dir, store)


def _open(core: ApiState, prefs_dir: Path, store: KeyStore) -> Iterator[App]:
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
    app.files.load(str(source))
    assert app.analyze_view.language is Language.CSHARP
    assert app.analyze_view.editor.get() == "public class Oyuncu {}\n"
    assert app.prefs.recent_files[0] == str(source)

    big = tmp_path / "buyuk.c"
    big.write_text("x" * (app.settings.limits.max_bytes + 1), encoding="utf-8")
    app.files.load(str(big))
    assert app.analyze_view.editor.get() == "public class Oyuncu {}\n"


def test_html_report_hides_complexity_card(app: App, core: ApiState) -> None:
    replies = [
        FakeReply(data={"additional_findings": []}),
        FakeReply(data={"key_flaw_concept": "Alternatif metin", "guiding_questions": ["Kim?"]}),
    ]
    core.provider_factory = lambda _n: FakeProvider(
        script=list(replies), retry=RetryPolicy(max_retries=0)
    )
    view = app.analyze_view
    view.select(Language.HTML, Engine.NONE, None)
    assert view.language_picker.get() == "HTML"
    view.editor.set(HTML_PAGE, Language.HTML)
    analyze(app)
    assert view.report is not None
    assert view.report.complexity is None
    assert not view.complexity.winfo_ismapped()
    assert {f.rule_id for f in view.report.findings} >= {"HTML-ACC-001", "HTML-ACC-002"}


def test_open_python_file(app: App, tmp_path: Path) -> None:
    source = tmp_path / "ornek.py"
    source.write_text(PY_LINE, encoding="utf-8")
    app.files.load(str(source))
    assert app.analyze_view.language is Language.PYTHON
    assert app.analyze_view.engine is Engine.NONE


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
    assert app.sidebar.status_text.cget("text") == "claude_cli"
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


@pytest.fixture
def no_stop_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    """Durdur testlerinde çift tıklama korumasını kapatır (koruma ayrıca sınanır)."""
    monkeypatch.setattr(analyze_view_module, "STOP_GUARD_S", 0.0)


@pytest.mark.usefixtures("no_stop_guard")
def test_stop_button_cancels_analysis(stalled_app: App, stalling: StallingProvider) -> None:
    """Faz 19: meşgulken düğme "Durdur" olur; tıklanınca LLM çağrısı iptal edilir."""
    view = stalled_app.analyze_view
    view.editor.set(LINKED_LIST, Language.C)
    stalled_app.analyze()
    assert view.busy
    assert view.run_button.cget("text") == "Durdur"
    assert stalling.started.wait(10)
    view.run_button.invoke()
    assert not view.busy
    assert view.run_button.cget("text") == "Denetle"
    assert "durduruldu" in stalled_app.toast_label.cget("text")
    pump(stalled_app, lambda: not stalled_app.bridge.is_running("analyze"), timeout=10)
    assert stalling.cancelled.is_set()
    assert view.report is None
    stalled_app.update()  # geç mesaj gelse bile ekrana yazılmaz
    assert not view.busy


def test_quick_double_click_does_not_stop(stalled_app: App, stalling: StallingProvider) -> None:
    """Denetim O3: "Denetle"ye çift tıklama analizi başlatıp hemen durdurmamalı."""
    view = stalled_app.analyze_view
    view.editor.set(LINKED_LIST, Language.C)
    view.run_button.invoke()
    view.run_button.invoke()  # ikinci tıklama koruma süresi içinde
    assert view.busy
    assert stalling.started.wait(10)
    stalled_app.stop_analysis()


@pytest.mark.usefixtures("no_stop_guard")
def test_restart_while_previous_closing_shows_toast(
    stalled_app: App, stalling: StallingProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Denetim O2: önceki iş parçacığı kapanırken "Denetle" sessizce yok sayılmaz."""
    view = stalled_app.analyze_view
    view.editor.set(LINKED_LIST, Language.C)
    stalled_app.analyze()
    assert stalling.started.wait(10)
    stalled_app.stop_analysis()
    monkeypatch.setattr(stalled_app.bridge, "is_running", lambda _task: True)
    stalled_app.analyze()
    assert not view.busy
    assert "kapanıyor" in stalled_app.toast_label.cget("text")


@pytest.mark.usefixtures("no_stop_guard")
def test_escape_stops_only_on_analyze_page(stalled_app: App, stalling: StallingProvider) -> None:
    view = stalled_app.analyze_view
    view.editor.set(LINKED_LIST, Language.C)
    stalled_app.analyze()
    assert stalling.started.wait(10)
    stalled_app.navigate("history")
    stalled_app.on_escape()  # başka sayfada Esc (ör. açılır liste kapatma) analizi durdurmaz
    assert view.busy
    stalled_app.navigate("analyze")
    stalled_app.on_escape()
    assert not view.busy
    stalled_app.stop_analysis()  # boşta iken zararsız
    pump(stalled_app, lambda: not stalled_app.bridge.is_running("analyze"), timeout=10)


# --- Faz 24: arama, son dosyalar, sürükle-bırak -----------------------------------------------


def test_ctrl_f_highlights_and_cycles_matches(app: App) -> None:
    editor = app.analyze_view.editor
    editor.set("int x = 1;\nint y = x + x;\n", Language.C)
    bar = editor.find_bar
    editor._open_find(None)
    assert bar.is_open
    bar.entry.insert(0, "x")
    bar.refresh()
    assert len(bar.matches) == 3
    assert bar.count.cget("text") == "1/3"
    assert editor.text.tag_ranges("search")
    bar.next()
    bar.next()
    assert bar.count.cget("text") == "3/3"
    bar.next()
    assert bar.count.cget("text") == "1/3"
    bar.previous()
    assert bar.count.cget("text") == "3/3"
    current = editor.text.tag_ranges("search_current")
    assert [str(i) for i in current] == ["2.12", "2.13"]
    editor.text.insert("end", "x\n")  # metin değişince eşleşmeler yenilenir
    app.update()
    assert len(bar.matches) == 4
    bar.entry.delete(0, "end")
    bar.entry.insert(0, "yok")
    bar.refresh()
    assert bar.count.cget("text") == "Sonuç yok"


def test_escape_closes_find_bar_without_stopping(
    stalled_app: App, stalling: StallingProvider
) -> None:
    view = stalled_app.analyze_view
    view.editor.set(LINKED_LIST, Language.C)
    stalled_app.analyze()
    assert stalling.started.wait(10)
    view.editor._open_find(None)
    assert view.editor.find_bar._close_event() == "break"  # Esc'in uygulamaya ulaşmasını keser
    assert not view.editor.find_bar.is_open
    assert not view.editor.text.tag_ranges("search")
    assert view.busy
    stalled_app.stop_analysis()
    pump(stalled_app, lambda: not stalled_app.bridge.is_running("analyze"), timeout=10)


def test_recent_menu_opens_file_and_drops_missing(app: App, tmp_path: Path) -> None:
    first, second = tmp_path / "bir.c", tmp_path / "iki.py"
    first.write_text("int main(void) { return 0; }\n", encoding="utf-8")
    second.write_text(PY_LINE, encoding="utf-8")
    app.files.load(str(first))
    app.files.load(str(second))
    labels = [label for label, _ in app.analyze_view.recent_items()]
    assert labels[0].startswith("iki.py")
    assert labels[1].startswith("bir.c")

    app.analyze_view.recent_items()[1][1]()  # menüden "bir.c"
    assert app.analyze_view.editor.get() == first.read_text(encoding="utf-8")
    assert app.analyze_view.language is Language.C

    second.unlink()
    app.files.open_recent(str(second))
    assert str(second) not in app.prefs.recent_files
    assert str(second) not in runtime.load_prefs(app.prefs_dir).recent_files
    assert app.analyze_view.language is Language.C  # editör değişmedi


def test_drop_opens_file(app: App, tmp_path: Path) -> None:
    folder = tmp_path / "boşluklu klasör"
    folder.mkdir()
    source = folder / "Oyuncu.cs"
    source.write_text("public class Oyuncu {}\n", encoding="utf-8")
    app.files.on_drop("{" + source.as_posix() + "} " + (tmp_path / "yok.c").as_posix())
    assert app.analyze_view.language is Language.CSHARP
    assert app.analyze_view.editor.get() == "public class Oyuncu {}\n"
    app.files.on_drop(folder.as_posix())  # klasör: açılmaz
    assert app.analyze_view.editor.get() == "public class Oyuncu {}\n"


def test_drag_and_drop_registered_on_windows(app: App) -> None:
    if sys.platform == "win32":  # tkdnd ikilileri tkinterdnd2 paketinde
        assert app.files.drop_enabled


def test_write_toml_button(app: App, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "codementor.toml"
    target.write_text('# yorum\n[providers]\ndefault = "ollama"\n', encoding="utf-8")
    monkeypatch.setattr(runtime, "writable_config_file", lambda: target)
    app.connections.check = lambda _name: None  # type: ignore[method-assign]
    app.connections.make_default("claude_cli")
    app.connections.set_model("ollama", "qwen2.5-coder:14b")
    app.settings_view.write_config_button.invoke()
    text = target.read_text(encoding="utf-8")
    assert text.startswith("# yorum")
    assert 'default = "claude_cli"' in text
    assert 'model = "qwen2.5-coder:14b"' in text
    assert str(target) in app.toast_label.cget("text")

    target.write_text("[bozuk", encoding="utf-8")
    app.write_config()
    assert "yazılamadı" in app.toast_label.cget("text")
