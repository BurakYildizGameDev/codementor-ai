"""Geçmiş ve dışa aktarma denetleyicisi — Faz F (F0) bölmesi (`app.py`'den).

Kayıtlı analizleri listeleme, açma, silme, temizleme ve farklı biçimlerde dışa aktarma.
Faz F (F11): SQLite işleri (liste, silme, temizleme) `Bridge` üzerinden arka plan iş
parçacığında koşar; sonuçlar ana iş parçacığında `handle` ile arayüze uygulanır, liste o sırada
"Yükleniyor…" gösterir. Tkinter/CustomTkinter en üstte içe aktarılmaz; Linux CI'da tkinter'sız
içe aktarılabilir.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from codementor.desktop import runtime
from codementor.desktop.bridge import Emit, Message
from codementor.desktop.services import render_export
from codementor.models.enums import Engine, Language
from codementor.models.report import AnalysisReport
from codementor.report.usage import usage_totals_label
from codementor.storage.cache import (
    clear_analyses,
    delete_analysis,
    get_analysis,
    get_row,
    list_analyses_page,
    usage_totals,
)
from codementor.storage.db import AnalysisRow
from codementor.storage.sessions import clear_sessions

if TYPE_CHECKING:
    from codementor.desktop.app import App

_EXPORT_SUFFIX = {"md": ".md", "sarif": ".sarif", "json": ".json"}
# Faz F (F11): geçmiş DB işleri arka plan görevleri (köprü kuşağı eski sonuçları atar)
PAGE_TASK = "history"
DELETE_TASK = "history_delete"
CLEAR_TASK = "history_clear"
OPEN_TASK = "history_open"  # Sonraya #40: kayıt açma da arka planda
HISTORY_TASKS = (PAGE_TASK, DELETE_TASK, CLEAR_TASK, OPEN_TASK)


@dataclass(frozen=True)
class HistoryPage:
    """Arka planda okunan geçmiş sayfası (Faz F, F11)."""

    rows: list[AnalysisRow]
    next_cursor: str | None
    totals: str | None  # yalnız ilk sayfada hesaplanır; "daha fazla"da None
    search_active: bool
    append: bool


@dataclass(frozen=True)
class HistoryDeleted:
    """Silme sonucu: kayıt ya da saklanan kod bulundu mu (Faz F, F11)."""

    analysis_id: str
    deleted: bool


@dataclass(frozen=True)
class HistoryOpened:
    """Arka planda okunan kayıt: rapor (uyumluysa) ya da yalnız satır + saklanan kod (#40)."""

    analysis_id: str
    report: AnalysisReport | None
    row: AnalysisRow | None
    code: str | None


@dataclass(frozen=True)
class HistoryCleared:
    """Temizlik sonucu: silinen analiz sayısı (Faz F, F11)."""

    count: int


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


def refresh(app: App, *, limit: int, before: str | None, search: str | None, append: bool) -> None:
    """Geçmiş sayfasını arka planda okur; liste o sırada "Yükleniyor…" gösterir (F11).

    `append` verilirse sonuç mevcut satırların altına eklenir ve toplam etiketi yeniden
    hesaplanmaz. Aynı görev yeniden başlatılırsa köprü eski iş parçacığının sonucunu atar.
    """
    db = app.core.database()
    search_active = bool(search)

    def work(_emit: Emit) -> HistoryPage:
        rows, next_cursor = list_analyses_page(db, limit=limit, before=before, search=search)
        totals = None if append else usage_totals_label(usage_totals(db))
        return HistoryPage(list(rows), next_cursor, totals, search_active, append)

    app.bridge.submit(PAGE_TASK, work)


def delete(app: App, analysis_id: str) -> None:
    """Kaydı ve saklanan kodu arka planda siler (Faz 62, Faz F; F11: DB işi iş parçacığında)."""
    if app.analyze_view.busy:
        app.toast("Analiz sürerken silinemez; önce Durdur'a bas.")
        return
    db = app.core.database()
    prefs_dir = app.prefs_dir

    def work(_emit: Emit) -> HistoryDeleted:
        deleted_db = delete_analysis(db, analysis_id)
        deleted_file = runtime.delete_source(analysis_id, prefs_dir)
        return HistoryDeleted(analysis_id, deleted_db or deleted_file)

    app.history_view.show_loading()  # silme + liste yenilemesi boyunca "Yükleniyor…" (F11)
    app.bridge.submit(DELETE_TASK, work)


def clear(app: App) -> None:
    """Tüm geçmişi, saklanan kodları ve oturumları arka planda temizler (Faz 62, Faz F, F11)."""
    if app.analyze_view.busy:  # biten analiz oturumu ve kaydı yeniden yazardı (denetim O2)
        app.toast("Analiz sürerken geçmiş temizlenemez; önce Durdur'a bas.")
        return
    if not app.confirm(
        "Geçmişi Temizle",
        "Tüm analiz geçmişi, saklanan kodlar ve ipucu ilerlemen silinecek. Emin misin?",
        parent=app,
    ):
        return
    db = app.core.database()
    prefs_dir = app.prefs_dir

    def work(_emit: Emit) -> HistoryCleared:
        count = clear_analyses(db)
        clear_sessions(db)
        runtime.clear_sources(prefs_dir)
        return HistoryCleared(count)

    app.history_view.show_loading()  # temizlik + liste yenilemesi boyunca "Yükleniyor…" (F11)
    app.bridge.submit(CLEAR_TASK, work)


def handle(app: App, message: Message) -> None:
    """Köprüden gelen geçmiş sonuçlarını ana iş parçacığında arayüze uygular (F11)."""
    if message.kind == "error":  # köprü istisnayı Türkçe metne çevirdi
        text = str(message.payload)
        if message.task == OPEN_TASK:
            app._opening_analysis_id = None
            app.toast(text)
        elif message.task == PAGE_TASK:
            app.history_view.apply_error(text)
        else:
            app.history_view.refresh()  # hata sonrası liste "Yükleniyor…"da kalmaz (F11)
            app.toast(text)
        return
    payload = message.payload
    if isinstance(payload, HistoryPage):
        app.history_view.apply_page(
            payload.rows,
            payload.next_cursor,
            totals=payload.totals,
            search_active=payload.search_active,
            append=payload.append,
        )
    elif isinstance(payload, HistoryDeleted):
        _apply_deleted(app, payload)
    elif isinstance(payload, HistoryCleared):
        _apply_cleared(app, payload)
    elif isinstance(payload, HistoryOpened):
        _apply_opened(app, payload)


def _apply_deleted(app: App, result: HistoryDeleted) -> None:
    app.history_view.refresh()  # yükleme gösterimi kapanır, liste güncel kalır (F11)
    if not result.deleted:
        app.toast("Analiz bulunamadı.")
        return
    if app._shown_analysis_id == result.analysis_id:
        app._shown_analysis_id = None
        app.analyze_view.report = None
        app.analyze_view.reset_results()
    app.toast("Analiz geçmişten silindi.")


def _apply_cleared(app: App, result: HistoryCleared) -> None:
    app.save_prefs(recent_files=[])
    app._shown_analysis_id = None
    app._last_code, app._last_question_id, app._last_counted = "", None, None
    app.analyze_view.report = None
    app.analyze_view.reset_results()
    app.history_view.refresh()
    app.toast(f"Geçmiş temizlendi ({result.count} analiz).")


def open_history(app: App, analysis_id: str) -> None:
    """Seçilen geçmiş analizini açar (Faz F; Sonraya #40: kayıt ve kod arka planda okunur).

    Kaydedilmemiş değişiklik onayı ana iş parçacığında sorulur; rapor, satır ve saklanan kod
    `Bridge` iş parçacığında okunur, editör ve sonuç panelleri `handle` ile güncellenir.
    Art arda iki açmada köprü kuşağı eskisinin sonucunu atar.
    """
    if not app.files.confirm_discard():
        return
    db = app.core.database()
    prefs_dir = app.prefs_dir

    def work(_emit: Emit) -> HistoryOpened:
        report = get_analysis(db, analysis_id)
        row = None if report is not None else get_row(db, analysis_id)
        code = runtime.load_source(analysis_id, prefs_dir) if report or row else None
        return HistoryOpened(analysis_id, report, row, code)

    app._opening_analysis_id = analysis_id
    app.bridge.submit(OPEN_TASK, work)


def _apply_opened(app: App, result: HistoryOpened) -> None:
    app._opening_analysis_id = None
    if result.report is None and result.row is None:
        app.toast("Bu analiz artık bulunamıyor.")
        return
    view = app.analyze_view
    app._shown_analysis_id = result.analysis_id
    if result.report is not None:
        language, engine = result.report.language, result.report.engine
        question_id = result.report.question_id
    else:
        assert result.row is not None
        language = _enum(Language, result.row.language, view.language)
        engine = _enum(Engine, result.row.engine, view.engine)
        question_id = result.row.question_id
    view.select(language, engine, question_id)
    view.editor.set(result.code or "// Bu analizin kodu saklanmamış.\n", language)
    app.files.current_path = None
    app.files.is_dirty = False
    app.tracker.reset()
    app.tracker.finish()
    view.reset_results()
    if result.report is not None:
        view.show_report(result.report)
    else:
        app.toast(
            "Bu rapor farklı bir CodeMentor sürümüyle oluşturulduğu için gösterilemiyor. "
            "Kodu editöre açtım; yeniden denetleyebilirsin."
        )
    app.navigate("analyze")


def _enum[E: (Language, Engine)](kind: type[E], value: str, fallback: E) -> E:
    """Kayıttaki dil/motor değeri; tanınmazsa mevcut seçim korunur (Faz 60)."""
    try:
        return kind(value)
    except ValueError:
        return fallback
