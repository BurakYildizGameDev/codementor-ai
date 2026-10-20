"""Pencere duman testi: gerçek Tk penceresi + FakeProvider. Ekran yoksa (Linux CI) atlanır.

Bölüm 2/5.
"""

from __future__ import annotations

import sys
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from codementor.config import CONFIG_FILE_ENV
from codementor.desktop import connections_controller as controller_module
from codementor.desktop import runtime
from codementor.desktop.app import App
from codementor.desktop.connections import PROVIDERS, KeyStore, Probe
from codementor.models.enums import Language
from codementor.models.provider import ProviderStatus
from codementor.models.validation import DownloadProgress
from tests.desktop.app_support import (
    PY_LINE,
    _toast,
    _usage_report,
    pump,
    pump_history,
)
from tests.desktop.conftest import StallingProvider
from tests.integration.conftest import LINKED_LIST


def test_purge_legacy_keys_button(app: App, store: KeyStore) -> None:
    """F8: 'Eski anahtarları temizle' düğmesi kalıntı anahtarları siler, sonucu bildirir."""
    app.connections.check = lambda _name: None  # type: ignore[method-assign]
    store.set("openai", "sk-eski-openai")
    store.set("deepseek", "sk-eski-deepseek")
    store.set("gemini", "sk-guncel-1234")

    app.settings_view.purge_legacy_button.invoke()

    assert "2 eski anahtar" in app.toast_label.cget("text")
    assert store.get("openai") is None
    assert store.get("deepseek") is None
    assert store.get("gemini") == "sk-guncel-1234"

    app.settings_view.purge_legacy_button.invoke()  # ikinci kez: silinecek yok
    assert "bulunamadı" in app.toast_label.cget("text")


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
    pump_history(stalled_app)  # F11: geçmiş listesi arka planda yüklenir
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
        "1.540 token (giriş 1.200 · çıkış 340) · ~$0.0123"
    )
    # Faz K: token harcanmadıysa da görünür
    assert report_usage(_usage_report(tokens=(0, 0), cost=None)) == "token 0 (model çağrılmadı)"


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
