"""Pencere duman testi: gerçek Tk penceresi + FakeProvider. Ekran yoksa (Linux CI) atlanır.

Bölüm 4/5.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import customtkinter as ctk
import pytest

from codementor.desktop.app import App
from codementor.models.enums import Language
from codementor.models.request import AnalysisRequest
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.storage import cache
from codementor.storage.db import AnalysisRow
from tests.desktop.app_support import (
    _toast,
    analyze,
    pump,
    pump_history,
)
from tests.integration.conftest import LINKED_LIST


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


def test_slow_llm_hint_shown_while_busy_and_cleared_after(app: App) -> None:
    """Faz 63: uzun LLM geçişinde "takılmadı, Durdur'a basabilirsin" uyarısı görünür."""
    from codementor.models.pipeline import StageEvent

    now = [100.0]
    app.tracker.clock = lambda: now[0]
    assert app.tracker.slow_hint_s == app.settings.pipeline.slow_llm_hint_s
    timeline = app.analyze_view.timeline
    app.analyze_view.set_busy(True)
    app.tracker.apply(StageEvent(analysis_id="A", stage="llm_a", status="started"))
    app._poll()
    assert timeline._hint_text is None
    now[0] += 90
    app._poll()
    assert timeline._hint_text is not None
    assert "90 sn" in timeline._hint_text
    app.analyze_view.set_busy(False)
    app.analyze_view.show_progress(app.tracker)
    assert timeline._hint_text is None


def test_slow_llm_hint_threshold_from_settings(app: App) -> None:
    app.base_settings = app.base_settings.model_copy(
        update={"pipeline": app.base_settings.pipeline.model_copy(update={"slow_llm_hint_s": None})}
    )
    app.apply_settings()
    assert app.tracker.slow_hint_s is None


def test_clear_history_while_analysis_running_is_blocked(app: App, prefs_dir: Path) -> None:
    """Denetim O2: analiz sürerken temizleme reddedilir; aksi halde biten analiz oturumu ve
    kaydı yeniden yazar, merdiven sıfırlanmamış olurdu."""
    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    report = app.analyze_view.report
    assert report is not None
    asked: list[str] = []

    def accept(title: str, message: str, **_kwargs: Any) -> bool:
        asked.append(message)
        return True

    app.confirm = accept
    app.analyze_view.set_busy(True)
    app.clear_history()
    assert asked == []  # onay bile sorulmaz
    assert cache.get_analysis(app.core.database(), report.analysis_id) is not None
    assert "Durdur" in _toast(app)
    app.analyze_view.set_busy(False)


def test_delete_history_while_analysis_running_is_blocked(app: App) -> None:
    """Faz F (D19): Analiz sürerken tekil silme işlemi engellenir ve toast gösterilir."""
    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    report = app.analyze_view.report
    assert report is not None
    aid = report.analysis_id

    app.analyze_view.set_busy(True)
    app.delete_history(aid)
    assert cache.get_analysis(app.core.database(), aid) is not None
    assert "Analiz sürerken silinemez" in _toast(app)
    app.analyze_view.set_busy(False)


def test_history_view_delete_button_disabled_when_busy(app: App) -> None:
    """Faz F (D19): Analiz meşgulken history_view satırlarındaki Sil butonu disabled olur."""
    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    app.analyze_view.set_busy(True)
    app.history_view.refresh()
    pump_history(app)  # F11: liste arka planda okunur

    item = next(w for w in app.history_view.list.winfo_children() if isinstance(w, ctk.CTkFrame))
    del_btn = next(
        c for c in item.winfo_children() if isinstance(c, ctk.CTkButton) and c.cget("text") == "Sil"
    )
    assert del_btn.cget("state") == "disabled"
    app.analyze_view.set_busy(False)
    app.history_view.refresh()
    pump_history(app)  # F11: liste arka planda okunur
    item_normal = next(
        w for w in app.history_view.list.winfo_children() if isinstance(w, ctk.CTkFrame)
    )
    del_btn_normal = next(
        c
        for c in item_normal.winfo_children()
        if isinstance(c, ctk.CTkButton) and c.cget("text") == "Sil"
    )
    assert del_btn_normal.cget("state") == "normal"


def test_clear_history_resets_last_attempt_state(app: App) -> None:
    """Denetim O2: temizlikten sonra aynı kod yeni deneme sayılır ("sayıldı" durumu kalmaz)."""
    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    assert app._last_counted is not None
    app.confirm = lambda *_a, **_k: True
    app.clear_history()
    pump(app, lambda: app._last_counted is None)  # F11: temizlik arka planda
    assert app._last_counted is None
    assert app._last_code == ""
    assert app._last_question_id is None


def test_degraded_report_is_not_counted_by_desktop(
    app: App, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Denetim O4 (Faz 61): `_on_message` bozulmuş raporu "sayılmadı" sayar; aynı kodla
    tekrar Denetle merdiveni ilerletmeyi engellemez (advance_hint=None)."""
    import codementor.desktop.app as app_module

    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    broken = FakeProvider(script=[FakeReply(error="500")], retry=RetryPolicy(max_retries=0))
    monkeypatch.setattr(app.core, "provider_factory", lambda _name: broken)
    analyze(app)
    report = app.analyze_view.report
    assert report is not None
    assert report.meta.degraded is True
    assert app._last_counted is False

    captured: list[AnalysisRequest] = []

    def fake_work(core: object, req: AnalysisRequest, cancel: object) -> object:
        captured.append(req)
        return lambda _emit: None

    monkeypatch.setattr(app_module, "analysis_work", fake_work)
    monkeypatch.setattr(app.bridge, "submit", lambda *_a, **_k: None)
    app.analyze()
    assert captured[-1].options.advance_hint is None


def test_history_delete_click_does_not_open_row(app: App) -> None:
    """Denetim O4 (Faz 62): "Sil"e tıklamak analizi açmaz; satırın kendisine tıklamak açar."""
    opened: list[str] = []
    deleted: list[str] = []
    app.history_view._on_open = opened.append
    app.history_view._on_delete = deleted.append
    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    app.navigate("history")
    pump_history(app)  # F11: liste arka planda okunur
    item = next(w for w in app.history_view.list.winfo_children() if isinstance(w, ctk.CTkFrame))
    del_btn = next(
        c for c in item.winfo_children() if isinstance(c, ctk.CTkButton) and c.cget("text") == "Sil"
    )
    for target in (del_btn, *del_btn.winfo_children()):
        target.event_generate("<Button-1>", x=2, y=2)
    app.update()
    assert opened == []
    item._canvas.event_generate("<Button-1>", x=2, y=2)
    app.update()
    assert len(opened) == 1  # karşılaştırma: satır bağı gerçekten çalışıyor


def test_report_callback_exception_shows_toast(app: App) -> None:
    toasts: list[str] = []
    app.toast = toasts.append
    app.report_callback_exception(RuntimeError, RuntimeError("deneme hatasi"), None)
    assert len(toasts) == 1
    assert "beklenmeyen" in toasts[0].lower()


def test_export_oserror_shows_toast(
    app: App, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz F (F2): Dışa aktarmada OSError toast ile bildirilir."""
    from tkinter import filedialog

    # Bir dosya oluşturup alt dizini varmış gibi bir yol verelim (yazılamaz)
    dosya = tmp_path / "dosya"
    dosya.write_text("var", encoding="utf-8")
    invalid_path = str(dosya / "alt" / "r.md")

    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    assert app.analyze_view.report is not None

    toasts: list[str] = []
    app.toast = toasts.append
    monkeypatch.setattr(filedialog, "asksaveasfilename", lambda **_k: invalid_path)

    app.export("md")
    assert len(toasts) == 1
    assert "kaydedilemedi" in toasts[0].lower()


def test_dirty_file_discard_confirm_and_save(
    app: App, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz F (F5): Değişiklik yapıldığında açma onayı ve Ctrl+S ile kaydetme."""
    src_file = tmp_path / "foo.c"
    src_file.write_text("int foo() { return 1; }\n", encoding="utf-8")
    bar_file = tmp_path / "bar.c"
    bar_file.write_text("int bar() { return 2; }\n", encoding="utf-8")

    app.files.load(str(src_file))
    assert app.files.current_path == src_file
    assert app.files.is_dirty is False

    # Metni düzenle
    app.analyze_view.editor.text.insert("end", "// ekleme\n")
    app.update()
    assert app.files.is_dirty is True

    # Başka dosya açmayı dene; kullanıcı 'Hayır' derse iptal edilir
    app.confirm = lambda *a, **k: False
    app.files.open_recent(str(bar_file))
    assert "// ekleme" in app.analyze_view.editor.get()
    assert app.files.current_path == src_file

    # Ctrl+S kısayolunu işlet (save)
    toasts: list[str] = []
    app.toast = toasts.append
    app.files.save()
    app.update()

    assert app.files.is_dirty is False
    assert "Kaydedildi: foo.c" in toasts[-1]
    assert "// ekleme" in src_file.read_text(encoding="utf-8")

    # Kaydettikten sonra başka dosya açınca confirm sorulmaz
    asked = False

    def no_confirm(*a: Any, **k: Any) -> bool:
        nonlocal asked
        asked = True
        return True

    app.confirm = no_confirm
    app.files.open_recent(str(bar_file))
    assert asked is False
    assert "int bar()" in app.analyze_view.editor.get()
