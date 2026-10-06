"""Pencere duman testi: gerçek Tk penceresi + FakeProvider. Ekran yoksa (Linux CI) atlanır."""

from __future__ import annotations

import gc
import os
import sys
import threading
import time
import tkinter as tk
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from codementor.api.state import ApiState
from codementor.config import CONFIG_FILE_ENV
from codementor.desktop import connections_controller as controller_module
from codementor.desktop import runtime
from codementor.desktop.app import App
from codementor.desktop.connections import PROVIDERS, KeyStore, Probe
from codementor.desktop.views import analyze_view as analyze_view_module
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.provider import ProviderStatus
from codementor.models.request import AnalysisRequest
from codementor.models.validation import DownloadProgress
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.storage.db import AnalysisRow
from codementor.validation.toolchain_install import InstallCancelledError, ToolchainInstallError
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
    # Yok edilen pencerenin Tk nesneleri (font vb.) burada, ana iş parçacığında toplansın: aksi
    # halde sonraki testin iş parçacığında toplanır, Font.__del__ ana döngüsü çalışmayan Tcl'i
    # bekler ve test kilitlenir (Faz 30'da büyüyen veriyle görüldü)
    window = None
    gc.collect()


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


def next_hint(app: App) -> None:
    app.analyze_view.actions.next_hint()
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
    analyze(app)  # Aynı kodla "Denetle": seviye artmaz (Faz 61)
    assert view.report is not None
    assert view.report.socratic is not None
    assert view.report.socratic.hint_level == first_level
    next_hint(app)  # "Bir ipucu daha": seviye artar (Faz 61)
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
    app.connections.save_key("gemini", "sk-test-1234567890")
    assert store.get("gemini") == "sk-test-1234567890"
    assert os.environ["GEMINI_API_KEY"] == "sk-test-1234567890"
    assert "kasasında" in app.settings_view.cards["gemini"].key_label.cget("text")

    app.connections.delete_key("gemini")
    assert store.get("gemini") is None
    assert "GEMINI_API_KEY" not in os.environ


def test_probe_results_update_cards_and_sidebar(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_probe(name: str, _settings: object) -> Probe:
        ready = name == "ollama"
        models = ["qwen2.5-coder:1.5b", "qwen2.5-coder:14b"] if ready else []
        return Probe(ProviderStatus(name=name, model="m", ready=ready, detail="d"), models)

    monkeypatch.setattr(controller_module, "probe", fake_probe)
    app.connections.make_default("ollama")
    app.check_environment()
    pump(app, lambda: len(app.connections.probes) == len(PROVIDERS))
    card = app.settings_view.cards["ollama"]
    assert card.status_pill.cget("text").strip() == "hazır"
    assert "qwen2.5-coder:14b" in card.model.cget("values")
    assert app.settings_view.cards["gemini"].status_pill.cget("text").strip() == "hazır değil"
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


# --- Faz 33: kullanıcı deneyimi -------------------------------------------------------------


def test_find_options_case_and_whole_word(app: App) -> None:
    editor = app.analyze_view.editor
    editor.set("int Count = 0;\nint count = counter;\n", Language.C)
    bar = editor.find_bar
    editor._open_find(None)
    bar.entry.insert(0, "count")
    bar.refresh()
    assert len(bar.matches) == 3
    bar.case_var.set(True)
    bar.refresh()
    assert len(bar.matches) == 2
    bar.word_var.set(True)
    bar.refresh()
    assert len(bar.matches) == 1
    assert bar.count.cget("text") == "1/1"


def test_ctrl_h_replace_current_and_all(app: App) -> None:
    editor = app.analyze_view.editor
    editor.set("x = x + x;\n", Language.C)
    bar = editor.find_bar
    assert editor._open_replace(None) == "break"
    assert bar.is_open
    assert bar.replace_open
    bar.entry.insert(0, "x")
    bar.replace_entry.insert(0, "y")
    bar.refresh()
    bar.replace_current()
    assert editor.get() == "y = x + x;\n"
    assert bar.count.cget("text") == "1/2"  # kalan eşleşmeler yeniden sayıldı
    bar.replace_every()
    assert editor.get() == "y = y + y;\n"
    assert "2" in app.toast_label.cget("text")
    assert bar.count.cget("text") == "Sonuç yok"


def test_folder_drop_offers_source_files(
    app: App, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ("Oyuncu.cs", "Dusman.cs", "notlar.txt"):
        (tmp_path / name).write_text(f"// {name}\n", encoding="utf-8")
    offered: list[list[tuple[str, Any]]] = []
    monkeypatch.setattr(app.analyze_view, "show_file_menu", offered.append)
    app.files.on_drop(tmp_path.as_posix())
    (items,) = offered
    assert [label.split()[0] for label, _ in items] == ["Dusman.cs", "Oyuncu.cs"]
    items[1][1]()  # menüden seç
    assert app.analyze_view.editor.get() == "// Oyuncu.cs\n"


def test_folder_drop_without_sources_notifies(app: App, tmp_path: Path) -> None:
    (tmp_path / "notlar.txt").write_text("x", encoding="utf-8")
    app.files.on_drop(tmp_path.as_posix())
    assert "kaynak dosya yok" in app.toast_label.cget("text")


def test_reload_config_button(app: App, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "codementor.toml"
    target.write_text('[providers.ollama]\nmodel = "toml-model"\n', encoding="utf-8")
    monkeypatch.setenv(CONFIG_FILE_ENV, str(target))
    app.connections.check = lambda _name: None  # type: ignore[method-assign]
    app.settings_view.reload_config_button.invoke()
    assert app.base_settings.providers.ollama.model == "toml-model"
    assert "yeniden yüklendi" in app.toast_label.cget("text")
    target.write_text("[bozuk", encoding="utf-8")
    app.reload_config()
    assert "okunamadı" in app.toast_label.cget("text")
    assert app.base_settings.providers.ollama.model == "toml-model"  # bozuk dosya uygulanmaz


def test_report_headline_shows_usage() -> None:
    from codementor.desktop.viewmodel import report_usage

    assert report_usage(_usage_report(tokens=(1200, 340), cost=0.0123)) == (
        "token 1200/340 · ~$0.0123"
    )
    assert report_usage(_usage_report(tokens=(0, 0), cost=None)) is None


def _usage_report(tokens: tuple[int, int], cost: float | None) -> Any:
    from types import SimpleNamespace

    from codementor.models.report import ReportMeta

    meta = ReportMeta(
        provider="fake",
        model="m",
        prompt_version="v1",
        rules_version="r1",
        schema_version="1.0",
        tokens_in=tokens[0],
        tokens_out=tokens[1],
        stage_latency_ms={},
        early_exit=False,
        cache_hit=False,
        degraded=False,
        repair_attempts=0,
        warnings=[],
        cost_est=cost,
    )
    return SimpleNamespace(meta=meta)


# --- Faz 29: derleyiciyi indir --------------------------------------------------------------


def _toast(app: App) -> str:
    return str(app.toast_label.cget("text"))


def test_compiler_download_progress_and_success(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    proceed = threading.Event()

    def fake_install(
        settings: object, *, progress: Callable[[object], None], cancel: object
    ) -> Path:
        progress(DownloadProgress(stage="download", done=50 * 1024 * 1024, total=100 * 1024 * 1024))
        assert proceed.wait(10)
        return Path("/tc/zig/zig")

    monkeypatch.setattr(controller_module, "install_zig", fake_install)
    view = app.settings_view
    view.download_button.invoke()
    assert view.downloading
    pump(app, lambda: "50 / 100 MB" in str(view.download_text.cget("text")))
    assert view.download_cancel.grid_info()  # sürerken İptal görünür
    proceed.set()
    pump(app, lambda: not view.downloading)
    assert "kuruldu" in str(view.download_text.cget("text"))
    assert "kuruldu" in _toast(app)
    assert not view.download_button.grid_info()


def test_compiler_download_error_shown(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    def failing(settings: object, **_kwargs: object) -> Path:
        raise ToolchainInstallError("İndirilen dosya doğrulanamadı (sha256 uyuşmuyor).")

    monkeypatch.setattr(controller_module, "install_zig", failing)
    view = app.settings_view
    view.download_button.invoke()
    pump(app, lambda: not view.downloading)
    assert "sha256 uyuşmuyor" in str(view.download_text.cget("text"))
    assert view.download_button.grid_info()  # yeniden denenebilir


def test_compiler_download_cancel(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    started = threading.Event()
    stopped = threading.Event()

    release = threading.Event()

    def waiting(settings: object, *, progress: object, cancel: threading.Event) -> Path:
        started.set()
        assert cancel.wait(10), "iptal gelmedi"
        stopped.set()
        assert release.wait(10)  # yarım dosyaların silinmesi sürüyor
        raise InstallCancelledError

    monkeypatch.setattr(controller_module, "install_zig", waiting)
    view = app.settings_view
    view.download_button.invoke()
    assert started.wait(5)
    view.download_cancel.invoke()
    assert stopped.wait(5)  # arka plandaki indirme gerçekten durdu
    # işçi bitmeden "iptal edildi / silindi" denmez; yeniden başlatma da reddedilir (denetim O2)
    assert "İptal ediliyor" in str(view.download_text.cget("text"))
    assert view.downloading
    view.download_button.invoke()
    assert "kapanıyor" in _toast(app)
    release.set()
    app.bridge.join("toolchain", 5)
    pump(app, lambda: not view.downloading)
    assert "iptal edildi" in str(view.download_text.cget("text"))
    assert view.download_button.grid_info()


def test_question_difficulty_filter(app: App) -> None:
    """Faz 30: dil ve zorluk filtreleri birlikte uygulanır; sayı etiketi güncellenir."""
    app.navigate("questions")
    view = app.questions_view
    expected = app.core.questions().filter(Language.C, None, Difficulty.HARD)
    assert len(expected) >= 1
    view.filter.set("C")
    view.difficulty_filter.set("Zor")
    view.refresh()
    assert view.count_label.cget("text") == f"{len(expected)} soru"
    assert len(view.grid_area.winfo_children()) == len(expected)
    view.filter.set("Tümü")
    view.difficulty_filter.set("Tümü")
    view.refresh()
    assert view.count_label.cget("text") == f"{len(app.core.questions())} soru"


def test_question_view_messages(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    """Boş filtre sonucu ile okunamayan banka farklı mesaj verir (denetim D1)."""
    app.navigate("questions")
    view = app.questions_view

    def label_texts() -> list[str]:
        return [str(w.cget("text")) for w in view.grid_area.winfo_children()]

    monkeypatch.setattr(view, "_load", lambda _l, _d: [])
    view.difficulty_filter.set("Zor")
    view.refresh()
    assert label_texts() == ["Bu filtrelerle eşleşen soru yok."]

    monkeypatch.setattr(view, "_load", lambda _l, _d: None)
    view.refresh()
    assert label_texts() == ["Soru bankası boş ya da okunamadı."]


def test_finding_list_groups_suggestions(app: App) -> None:
    """Faz 36: hatalar açık, öneriler "Öneriler (n)" düğmesinin altında katlı."""
    from codementor.models.enums import AuditCategory, FindingSource, Severity
    from codementor.models.findings import Finding

    def make(line: int, kind: str) -> Finding:
        return Finding(
            id=f"F-00{line}",
            rule_id=None,
            category=AuditCategory.DESIGN,
            severity=Severity.LOW,
            line_start=line,
            line_end=None,
            evidence="x",
            description=f"{kind} açıklaması",
            source=FindingSource.LLM,
            confidence=0.7,
            kind=kind,  # type: ignore[arg-type]
        )

    findings = app.analyze_view.findings
    findings.show([make(1, "issue"), make(2, "suggestion")], [])
    app.update()
    assert findings.count.cget("text") == "1"
    toggle = findings.suggestion_toggle
    assert toggle is not None
    assert toggle.cget("text") == "Öneriler (1) ▸"
    assert not findings.suggestion_body.grid_info()
    toggle.invoke()
    app.update()
    assert toggle.cget("text") == "Öneriler (1) ▾"
    assert findings.suggestion_body.grid_info()
    findings.show([make(1, "issue")], [])
    assert findings.suggestion_toggle is None


# --- Faz 60: geçmişte uyumsuz rapor --------------------------------------------------------


def test_open_history_missing_record_shows_not_found_toast(app: App) -> None:
    """Faz 60: Kayıt hiç yoksa 'Bu analiz artık bulunamıyor.' mesajı gösterilir."""
    app.open_history("01JNONEXISTENT9999999999999")
    assert "Bu analiz artık bulunamıyor." in _toast(app)


def test_open_history_incompatible_report_loads_code_and_clears_results(app: App) -> None:
    """Faz 60: Rapor şeması uyumsuzsa kod açılır, sonuçlar temizlenir ve uyarı toast'ı verilir."""
    analysis_id = "01J60TESTINCOMPATIBLE000001"
    row = AnalysisRow(
        id=analysis_id,
        created_at=datetime.now(UTC),
        cache_key="key_incompat_1",
        language="c",
        engine="standalone",
        question_id=None,
        session_id=None,
        provider="fake",
        model="fake",
        early_exit=False,
        degraded=False,
        tokens_in=10,
        tokens_out=20,
        latency_ms=100,
        report_json='{"bilinmeyen_veya_eski": "format"}',
    )
    db = app.core.database()
    with db.session() as session:
        session.add(row)
        session.commit()

    test_code = "int x = 42;\n"
    runtime.save_source(analysis_id, test_code, app.prefs_dir)

    app.open_history(analysis_id)
    assert app.current_view == "analyze"
    assert app.analyze_view.editor.get() == test_code
    assert app.analyze_view.language == Language.C
    assert app.analyze_view.report is None
    assert "farklı bir CodeMentor sürümüyle" in _toast(app)


def test_open_history_incompatible_report_missing_source_falls_back(app: App) -> None:
    """Faz 60 Olumsuz test: Uyumsuz kaydın kodu saklanmamışsa 'kod saklanmamış' yazılır, çökmez."""
    analysis_id = "01J60TESTINCOMPATIBLE000002"
    row = AnalysisRow(
        id=analysis_id,
        created_at=datetime.now(UTC),
        cache_key="key_incompat_2",
        language="cpp",
        engine="standalone",
        question_id=None,
        session_id=None,
        provider="fake",
        model="fake",
        early_exit=False,
        degraded=False,
        tokens_in=10,
        tokens_out=20,
        latency_ms=100,
        report_json='{"eski": "sema"}',
    )
    db = app.core.database()
    with db.session() as session:
        session.add(row)
        session.commit()

    # Kaynak dosya kasıtlı olarak oluşturulmadı
    app.open_history(analysis_id)
    assert app.current_view == "analyze"
    assert "saklanmamış" in app.analyze_view.editor.get()
    assert app.analyze_view.language == Language.CPP
    assert "farklı bir CodeMentor sürümüyle" in _toast(app)


def test_open_history_incompatible_report_invalid_language_preserves_selection(app: App) -> None:
    """Faz 60 Olumsuz test: Kayıttaki dil tanınmıyorsa mevcut dil seçimi korunur, çökmez."""
    prev_lang = app.analyze_view.language
    analysis_id = "01J60TESTINCOMPATIBLE000003"
    row = AnalysisRow(
        id=analysis_id,
        created_at=datetime.now(UTC),
        cache_key="key_incompat_3",
        language="taninmayan_dil_xyz",
        engine="taninmayan_motor_xyz",
        question_id=None,
        session_id=None,
        provider="fake",
        model="fake",
        early_exit=False,
        degraded=False,
        tokens_in=10,
        tokens_out=20,
        latency_ms=100,
        report_json='{"eski": "sema"}',
    )
    db = app.core.database()
    with db.session() as session:
        session.add(row)
        session.commit()

    app.open_history(analysis_id)
    assert app.current_view == "analyze"
    assert app.analyze_view.language == prev_lang
    assert "farklı bir CodeMentor sürümüyle" in _toast(app)


# --- Faz 61: masaüstü advance_hint kararları ------------------------------------------------


def test_advance_hint_desktop_decisions(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    """Faz 61 (K3): Masaüstü advance_hint kararları:
    - İlk analiz / kod değişince: advance_hint=None
    - Aynı kodla 'Denetle' (son analiz sayılmışsa): advance_hint=False
    - 'Bir ipucu daha': advance_hint=True
    - Son analiz degraded ise aynı kodla 'Denetle': advance_hint=None
    """
    captured: list[AnalysisRequest] = []
    import codementor.desktop.app as app_module

    def fake_work(core: object, req: AnalysisRequest, cancel: object) -> object:
        captured.append(req)
        return lambda _emit: None

    def fake_submit(task: str, work: object, *, cancellation: object = None) -> None:
        app._last_counted = True
        app.analyze_view.set_busy(False)

    monkeypatch.setattr(app_module, "analysis_work", fake_work)
    monkeypatch.setattr(app.bridge, "submit", fake_submit)

    # 1. İlk analiz: advance_hint is None
    app.analyze_view.editor.set("int x = 1;\n", Language.C)
    app.analyze()
    assert len(captured) == 1
    assert captured[-1].options.advance_hint is None
    assert app._last_counted is True

    # 2. Aynı kodla 'Denetle': advance_hint is False
    app.analyze()
    assert len(captured) == 2
    assert captured[-1].options.advance_hint is False

    # 3. 'Bir ipucu daha' (socratic card next_hint): advance_hint is True
    app.analyze_view.actions.next_hint()
    assert len(captured) == 3
    assert captured[-1].options.advance_hint is True

    # 4. Kod değişince 'Denetle': advance_hint is None
    app.analyze_view.editor.set("int x = 2;\n", Language.C)
    app.analyze()
    assert len(captured) == 4
    assert captured[-1].options.advance_hint is None

    # 5. Son analiz degraded ise aynı kodla 'Denetle': advance_hint is None
    app._last_counted = False
    app.analyze()
    assert len(captured) == 5
    assert captured[-1].options.advance_hint is None
