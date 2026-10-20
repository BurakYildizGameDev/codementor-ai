"""Pencere duman testi: gerçek Tk penceresi + FakeProvider. Ekran yoksa (Linux CI) atlanır.

Bölüm 5/5.
"""

from __future__ import annotations

import threading
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import customtkinter as ctk
import pytest

from codementor.desktop import history_controller
from codementor.desktop.app import App
from codementor.desktop.bridge import Cancellation
from codementor.desktop.views import history_view as history_view_module
from codementor.storage import cache
from codementor.storage.db import AnalysisRow
from tests.desktop.app_support import (
    _list_texts,
    _seed_history,
    _toast,
    pump,
    pump_history,
)


def test_save_as_for_new_unsaved_file(
    app: App, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz F (F5): Dosya yolu yoksa save() Farklı Kaydet açar."""
    from tkinter import filedialog

    new_file = tmp_path / "yeni.c"
    app.files.current_path = None
    app.files.mark_dirty()
    monkeypatch.setattr(filedialog, "asksaveasfilename", lambda **_k: str(new_file))

    app.files.save()
    assert new_file.is_file()
    assert app.files.is_dirty is False
    assert app.files.current_path == new_file


def test_save_preserves_original_crlf_newline(app: App, tmp_path: Path) -> None:
    """Faz F (F5): Orijinal dosyanın CRLF satır sonları kaydedilirken korunur."""
    crlf_file = tmp_path / "crlf.c"
    crlf_file.write_bytes(b"int x;\r\nint y;\r\n")

    app.files.load(str(crlf_file))
    assert app.files._newline == "\r\n"
    app.analyze_view.editor.text.insert("end", "int z;\n")
    app.files.save()

    raw = crlf_file.read_bytes()
    assert b"\r\n" in raw
    assert b"\n" not in raw.replace(b"\r\n", b"")


def test_save_oserror_shows_toast(app: App, tmp_path: Path) -> None:
    """Faz F (F5): Kaydetmede OSError oluşursa toast ile bildirilir."""
    dosya = tmp_path / "dosya"
    dosya.write_text("var", encoding="utf-8")
    app.files.current_path = dosya / "alt" / "test.c"

    toasts: list[str] = []
    app.toast = toasts.append
    app.files.save()
    assert len(toasts) == 1
    assert "kaydedilemedi" in toasts[0].lower()
    app.files.is_dirty = False


def test_close_with_unsaved_changes_confirm(app: App) -> None:
    """Faz F (F5): Kaydedilmemiş değişiklik varken kapatma onay ister;
    Hayır ise pencere açık kalır.
    """
    app.files.mark_dirty()
    app.confirm = lambda *a, **k: False
    app.close()
    assert app.winfo_exists()
    assert not app._closing
    app.files.mark_clean()


def test_close_while_busy_confirm(app: App) -> None:
    """Faz F (F7): Analiz sürerken kapatma onay ister; Hayır ise pencere açık kalır."""
    prompts: list[tuple[str, str]] = []

    def reject(title: str, message: str, **_kwargs: Any) -> bool:
        prompts.append((title, message))
        return False

    app.confirm = reject
    app.analyze_view.set_busy(True)
    app.close()
    assert prompts
    assert "sürüyor" in prompts[0][1]
    assert app.winfo_exists()
    assert not app._closing
    app.analyze_view.set_busy(False)


def test_close_while_downloading_confirm(app: App) -> None:
    """Faz F (F7): Derleyici (zig) indirmesi sürerken de kapatma onay ister."""
    app.connections.download_cancellation = Cancellation()
    app.confirm = lambda *_a, **_k: False
    app.close()
    assert app.winfo_exists()
    assert not app._closing
    app.connections.download_cancellation = None


def test_history_view_pagination_and_search(app: App) -> None:
    """Faz F (F6): Geçmiş ekranında sayfalama (50 + daha fazla) ve arama (% ve _ joker kaçışı)."""
    db = app.core.database()
    now = datetime.now(UTC)
    with db.session() as s:
        for i in range(60):
            qid = (
                "c-medium"
                if i == 5
                else ("c_underscore" if i == 6 else ("100%_done" if i == 7 else None))
            )
            s.add(
                AnalysisRow(
                    id=f"hist_{i:03d}",
                    created_at=now + timedelta(seconds=i),
                    cache_key=f"k_{i}",
                    language="c",
                    engine="none",
                    question_id=qid,
                    provider="ollama" if i % 2 == 0 else "fake",
                    report_json="{}",
                )
            )
        s.commit()

    # 1. İlk yükleme: 50 satır ve Daha Fazla butonu görünür
    app.history_view.search_entry.delete(0, "end")
    app.history_view.refresh()
    pump_history(app)  # F11: sayfa arka planda okunur
    assert len(app.history_view._rows) == 50
    assert app.history_view._next_cursor is not None

    # 2. Daha fazla yükle: kalan 10 satır eklenir, toplam 60 satır olur ve buton gizlenir
    app.history_view._handle_load_more()
    pump_history(app)  # F11: sonraki sayfa da arka planda okunur
    assert len(app.history_view._rows) == 60
    assert app.history_view._next_cursor is None

    # 3. Arama: "c-medium" -> yalnız 1 eşleşen (c-medium)
    app.history_view.search_entry.delete(0, "end")
    app.history_view.search_entry.insert(0, "c-medium")
    app.history_view.on_search()
    pump_history(app)
    assert len(app.history_view._rows) == 1
    assert app.history_view._rows[0].question_id == "c-medium"

    # 4. Joker kaçışı: "_" içeren arama ("c_") "c-medium" ile eşleşmez,
    # sadece "c_underscore" ile eşleşir
    app.history_view.search_entry.delete(0, "end")
    app.history_view.search_entry.insert(0, "c_")
    app.history_view.on_search()
    pump_history(app)
    assert len(app.history_view._rows) == 1
    assert app.history_view._rows[0].question_id == "c_underscore"

    # 5. Joker kaçışı: "%" içeren arama ("100%") sadece "100%_done" ile eşleşir
    app.history_view.search_entry.delete(0, "end")
    app.history_view.search_entry.insert(0, "100%")
    app.history_view.on_search()
    pump_history(app)
    assert len(app.history_view._rows) == 1
    assert app.history_view._rows[0].question_id == "100%_done"


def test_history_list_loads_off_main_thread(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    """F11: liste DB'den arka plan iş parçacığında okunur, arada "Yükleniyor…" görünür."""
    _seed_history(app, "01J11LIST0000000000000001")
    seen: list[bool] = []
    release = threading.Event()
    real_page = history_controller.list_analyses_page

    def slow_page(*args: Any, **kwargs: Any) -> Any:
        seen.append(threading.current_thread() is threading.main_thread())
        assert release.wait(10)  # bu sırada ana iş parçacığı arayüzü çizebilmeli
        return real_page(*args, **kwargs)

    monkeypatch.setattr(history_controller, "list_analyses_page", slow_page)
    app.navigate("history")
    assert app.history_view.loading
    assert history_view_module.LOADING_TEXT in _list_texts(app)
    release.set()
    pump_history(app)
    assert seen == [False]  # DB işi ana iş parçacığında DEĞİL
    assert [row.id for row in app.history_view._rows] == ["01J11LIST0000000000000001"]


def test_history_page_renders_rows_and_totals(app: App) -> None:
    """F11: arka plandan gelen sayfa satırları ve toplam etiketi çizer."""
    _seed_history(app, "01J11TOTAL000000000000001", "01J11TOTAL000000000000002")
    app.navigate("history")
    pump_history(app)
    assert not app.history_view.loading
    assert {row.id for row in app.history_view._rows} == {
        "01J11TOTAL000000000000001",
        "01J11TOTAL000000000000002",
    }
    assert app.history_view.totals_label.cget("text").startswith("Toplam: 2 analiz")
    assert any(isinstance(w, ctk.CTkFrame) for w in app.history_view.list.winfo_children())


def test_history_page_error_is_shown_in_turkish(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    """F11: DB okunamazsa liste Türkçe hata metni gösterir; arayüz çökmez."""
    monkeypatch.setattr(
        history_controller,
        "list_analyses_page",
        lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("veritabanı kapalı")),
    )
    app.navigate("history")
    pump_history(app)
    assert app.history_view._rows == []
    assert "Beklenmeyen bir hata" in _list_texts(app)


def test_history_stale_page_result_is_dropped(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    """F11: yeni yükleme başlarken eski iş parçacığının geç gelen sonucu listeye yazılmaz."""
    _seed_history(app, "01J11STALE000000000000001")
    release = threading.Event()
    started = threading.Event()
    calls = 0
    real_page = history_controller.list_analyses_page

    def page(*args: Any, **kwargs: Any) -> Any:
        nonlocal calls
        calls += 1
        if calls == 1:  # ilk yükleme: ikinci yükleme bitene kadar bekler
            started.set()
            assert release.wait(10)
            return real_page(*args, **kwargs)
        return [], None

    monkeypatch.setattr(history_controller, "list_analyses_page", page)
    app.navigate("history")  # 1. yükleme (beklemede)
    pump(app, lambda: started.is_set())
    assert calls == 1
    app.history_view.refresh()  # 2. yükleme: kuşağı ilerletir
    pump_history(app)
    assert app.history_view._rows == []
    release.set()  # 1. yükleme geç biter
    pump(app, lambda: not app.bridge.is_running("history"))
    for _ in range(5):
        app.update()
        time.sleep(0.02)
    assert app.history_view._rows == []


def test_history_delete_runs_off_main_thread(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    """F11: silme DB işi arka planda koşar; kayıt listeden ve diskten düşer."""
    _seed_history(app, "01J11DELETE00000000000001")
    app.navigate("history")
    pump_history(app)
    assert app.history_view._rows
    seen: list[bool] = []
    real_delete = history_controller.delete_analysis

    def spy(db: Any, analysis_id: str) -> bool:
        seen.append(threading.current_thread() is threading.main_thread())
        return real_delete(db, analysis_id)

    monkeypatch.setattr(history_controller, "delete_analysis", spy)
    app.delete_history("01J11DELETE00000000000001")
    pump(app, lambda: cache.get_row(app.core.database(), "01J11DELETE00000000000001") is None)
    pump_history(app)
    assert seen == [False]
    assert app.history_view._rows == []
    assert "geçmişten silindi" in _toast(app)


def test_history_clear_runs_off_main_thread(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    """F11: "Tümünü temizle" DB işi arka planda; liste, oturumlar ve tercihler sıfırlanır."""
    _seed_history(app, "01J11CLEAR000000000000001")
    app.navigate("history")
    pump_history(app)
    seen: list[bool] = []
    real_clear = history_controller.clear_analyses

    def spy(db: Any) -> int:
        seen.append(threading.current_thread() is threading.main_thread())
        return real_clear(db)

    monkeypatch.setattr(history_controller, "clear_analyses", spy)
    app.confirm = lambda *_a, **_k: True  # type: ignore[method-assign]
    app.save_prefs(recent_files=["test.c"])
    app.clear_history()
    pump(app, lambda: "Geçmiş temizlendi" in _toast(app))
    pump_history(app)
    assert seen == [False]
    assert app.history_view._rows == []
    assert app.prefs.recent_files == []
