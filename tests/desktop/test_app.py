"""Pencere duman testi: gerçek Tk penceresi + FakeProvider. Ekran yoksa (Linux CI) atlanır.

Bölüm 1/5.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import customtkinter as ctk

from codementor.api.state import ApiState
from codementor.desktop import runtime
from codementor.desktop.app import App
from codementor.desktop.connections import KeyStore
from codementor.models.enums import Engine, Language
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.storage import cache, sessions
from codementor.storage.db import AnalysisRow
from tests.desktop.app_support import (
    HTML_PAGE,
    PY_LINE,
    _toast,
    analyze,
    next_hint,
    pump,
    pump_history,
)
from tests.integration.conftest import LINKED_LIST


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
    pump_history(app)  # F11: liste arka plan iş parçacığında okunur
    assert app.history_view.list.winfo_children()

    app.open_history(report.analysis_id)
    assert app.current_view == "analyze"
    assert app.analyze_view.editor.get() == LINKED_LIST
    assert app.analyze_view.report == report


def test_delete_history_removes_record_and_resets_active_report(app: App, prefs_dir: Path) -> None:
    """Faz 62: delete_history DB kaydını ve saklanan kodu siler; açık raporu sıfırlar."""
    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    report = app.analyze_view.report
    assert report is not None
    analysis_id = report.analysis_id
    assert app._shown_analysis_id == analysis_id

    # DB ve diskte mevcut
    assert cache.get_analysis(app.core.database(), analysis_id) is not None
    assert runtime.load_source(analysis_id, prefs_dir) == LINKED_LIST

    # Sil
    app.delete_history(analysis_id)
    pump(app, lambda: cache.get_analysis(app.core.database(), analysis_id) is None)
    pump_history(app)  # F11: silme ve liste yenilemesi arka planda
    assert cache.get_analysis(app.core.database(), analysis_id) is None
    assert runtime.load_source(analysis_id, prefs_dir) is None
    assert app.analyze_view.report is None
    assert app._shown_analysis_id is None

    # Zaten silinmiş analizi tekrar silme
    app.delete_history(analysis_id)
    pump(app, lambda: "bulunamadı" in _toast(app))  # F11: silme arka planda


def test_clear_history_confirmation_and_cleanup(app: App, prefs_dir: Path) -> None:
    """Faz 62: clear_history onay verilirse tüm geçmişi, saklanan kodları ve oturumları temizler."""
    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    report = app.analyze_view.report
    assert report is not None
    analysis_id = report.analysis_id

    # Oturum denemesi de ekle
    sessions.reserve_attempt(app.core.database(), "s1", "q1")

    # 1. Onay verilmezse silinmez (enjekte edilebilir self.confirm)
    prompts: list[tuple[str, str]] = []

    def reject(title: str, message: str, **_kwargs: Any) -> bool:
        prompts.append((title, message))
        return False

    app.confirm = reject
    app.clear_history()
    assert len(prompts) == 1
    assert "Emin misin?" in prompts[0][1]
    assert cache.get_analysis(app.core.database(), analysis_id) is not None
    assert runtime.load_source(analysis_id, prefs_dir) is not None
    assert sessions.next_attempt(app.core.database(), "s1", "q1") == 2

    # 2. Onay verilirse temizlenir
    app.save_prefs(recent_files=["test.c"])
    assert app.prefs.recent_files == ["test.c"]

    def accept(title: str, message: str, **_kwargs: Any) -> bool:
        prompts.append((title, message))
        return True

    app.confirm = accept
    app.clear_history()
    pump(app, lambda: "Geçmiş temizlendi" in _toast(app))  # F11: temizlik arka planda
    pump_history(app)
    assert cache.get_analysis(app.core.database(), analysis_id) is None
    assert runtime.load_source(analysis_id, prefs_dir) is None
    assert app.analyze_view.report is None
    assert app._shown_analysis_id is None
    assert app.prefs.recent_files == []
    # Oturumlar da silindi:
    assert sessions.next_attempt(app.core.database(), "s1", "q1") == 1
    assert "Geçmiş temizlendi (1 analiz)." in _toast(app)


def test_delete_history_incompatible_report_resets_shown_analysis(
    app: App, prefs_dir: Path
) -> None:
    """Faz 62: Uyumsuz eski rapor ekranda açıkken silinirse gösterim sıfırlanır."""
    analysis_id = "01J62TESTINCOMPATIBLE000001"
    row = AnalysisRow(
        id=analysis_id,
        created_at=datetime.now(UTC),
        cache_key="key_incompat_del",
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
        report_json='{"eski": "format"}',
    )
    db = app.core.database()
    with db.session() as session:
        session.add(row)
        session.commit()
    runtime.save_source(analysis_id, "int a = 1;\n", prefs_dir)

    app.open_history(analysis_id)
    assert app._shown_analysis_id == analysis_id
    assert app.analyze_view.report is None  # şema uyumsuz

    app.delete_history(analysis_id)
    pump(app, lambda: app._shown_analysis_id is None and not app.history_view.loading)
    assert app._shown_analysis_id is None
    assert cache.get_row(db, analysis_id) is None
    assert runtime.load_source(analysis_id, prefs_dir) is None


def test_history_view_buttons_trigger_callbacks(app: App) -> None:
    """Faz 62: HistoryView sil butonu on_delete çağırır; Tümünü temizle on_clear çağırır."""
    deleted: list[str] = []
    cleared = False

    def on_del(aid: str) -> None:
        deleted.append(aid)

    def on_clr() -> None:
        nonlocal cleared
        cleared = True

    app.history_view._on_delete = on_del
    app.history_view._on_clear = on_clr

    app.analyze_view.editor.set(LINKED_LIST, Language.C)
    analyze(app)
    report = app.analyze_view.report
    assert report is not None

    app.navigate("history")
    pump_history(app)  # F11: satırlar arka planda yüklenir
    # "Tümünü temizle" butonuna tıkla
    app.history_view.clear_btn.invoke()
    assert cleared is True

    # Satırdaki "Sil" butonunu bul ve tıkla
    del_btns = [
        child
        for w in app.history_view.list.winfo_children()
        if isinstance(w, ctk.CTkFrame)
        for child in w.winfo_children()
        if isinstance(child, ctk.CTkButton) and child.cget("text") == "Sil"
    ]
    assert len(del_btns) == 1
    del_btns[0].invoke()
    assert deleted == [report.analysis_id]


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
