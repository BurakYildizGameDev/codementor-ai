"""Geçmiş ve dışa aktarma denetleyicisi — Faz F (F0) bölmesi (`app.py`'den).

Kayıtlı analizleri listeleme, açma, silme, temizleme ve farklı biçimlerde dışa aktarma.
Tkinter/CustomTkinter en üstte içe aktarılmaz; Linux CI'da tkinter'sız içe aktarılabilir.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from codementor.desktop import runtime
from codementor.desktop.services import render_export
from codementor.models.enums import Engine, Language
from codementor.storage.cache import (
    clear_analyses,
    delete_analysis,
    get_analysis,
    get_row,
    list_analyses,
)
from codementor.storage.db import AnalysisRow
from codementor.storage.sessions import clear_sessions

if TYPE_CHECKING:
    from codementor.desktop.app import App

_EXPORT_SUFFIX = {"md": ".md", "sarif": ".sarif", "json": ".json"}


def export(app: App, fmt: str) -> None:
    """Aktif raporu seçilen biçimde dışa aktarır."""
    from tkinter import filedialog

    report = app.analyze_view.report
    if report is None:
        return
    suffix = _EXPORT_SUFFIX[fmt]
    path = filedialog.asksaveasfilename(
        title="Raporu dışa aktar",
        defaultextension=suffix,
        initialfile=f"codementor-{report.analysis_id}{suffix}",
    )
    if not path:
        return
    try:
        Path(path).write_text(render_export(report, fmt), encoding="utf-8")
        app.toast(f"Rapor kaydedildi: {Path(path).name}")
    except OSError as exc:
        app.toast(f"Rapor kaydedilemedi: {exc.strerror or exc}")


def history_rows(app: App) -> list[AnalysisRow]:
    """Tüm geçmiş satırlarını döndürür."""
    return list_analyses(app.core.database())


def open_history(app: App, analysis_id: str) -> None:
    """Seçilen geçmiş analizini açar ve editör ile sonuç panellerini günceller."""
    report = get_analysis(app.core.database(), analysis_id)
    if report is not None:
        app._shown_analysis_id = analysis_id
        view = app.analyze_view
        view.select(report.language, report.engine, report.question_id)
        code = runtime.load_source(analysis_id, app.prefs_dir)
        view.editor.set(code or "// Bu analizin kodu saklanmamış.\n", report.language)
        app.files.current_path = None
        app.files.is_dirty = False
        app.tracker.reset()
        app.tracker.finish()
        view.reset_results()
        view.show_report(report)
        app.navigate("analyze")
        return

    row = get_row(app.core.database(), analysis_id)
    if row is None:
        app.toast("Bu analiz artık bulunamıyor.")
        return

    app._shown_analysis_id = analysis_id
    view = app.analyze_view
    try:
        lang = Language(row.language)
    except ValueError:
        lang = view.language
    try:
        eng = Engine(row.engine)
    except ValueError:
        eng = view.engine

    view.select(lang, eng, row.question_id)
    code = runtime.load_source(analysis_id, app.prefs_dir)
    view.editor.set(code or "// Bu analizin kodu saklanmamış.\n", lang)
    app.files.current_path = None
    app.files.is_dirty = False
    app.tracker.reset()
    app.tracker.finish()
    view.reset_results()
    app.toast(
        "Bu rapor farklı bir CodeMentor sürümüyle oluşturulduğu için gösterilemiyor. "
        "Kodu editöre açtım; yeniden denetleyebilirsin."
    )
    app.navigate("analyze")


def delete_history(app: App, analysis_id: str) -> None:
    """Kayıtlı bir analizi ve saklanan kodunu siler (Faz 62)."""
    deleted_db = delete_analysis(app.core.database(), analysis_id)
    deleted_file = runtime.delete_source(analysis_id, app.prefs_dir)
    if not deleted_db and not deleted_file:
        app.toast("Analiz bulunamadı.")
        return
    if app._shown_analysis_id == analysis_id:
        app._shown_analysis_id = None
        app.analyze_view.report = None
        app.analyze_view.reset_results()
    app.history_view.refresh()
    app.toast("Analiz geçmişten silindi.")


def clear_history(app: App) -> None:
    """Tüm analiz geçmişini, saklanan kodları ve oturumları temizler (Faz 62, Faz F)."""
    if app.analyze_view.busy:  # biten analiz oturumu ve kaydı yeniden yazardı (denetim O2)
        app.toast("Analiz sürerken geçmiş temizlenemez; önce Durdur'a bas.")
        return
    if not app.confirm(
        "Geçmişi Temizle",
        "Tüm analiz geçmişi, saklanan kodlar ve ipucu ilerlemen silinecek. Emin misin?",
        parent=app,
    ):
        return
    count = clear_analyses(app.core.database())
    clear_sessions(app.core.database())
    runtime.clear_sources(app.prefs_dir)
    app.save_prefs(recent_files=[])
    app._shown_analysis_id = None
    app._last_code, app._last_question_id, app._last_counted = "", None, None
    app.analyze_view.report = None
    app.analyze_view.reset_results()
    app.history_view.refresh()
    app.toast(f"Geçmiş temizlendi ({count} analiz).")
