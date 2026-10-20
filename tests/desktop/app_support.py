"""`test_app.py` için ortak düzenek: sabitler, yardımcılar, fixture'lar."""

from __future__ import annotations

import gc
import time
import tkinter as tk
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import customtkinter as ctk
import pytest

from codementor.api.state import ApiState
from codementor.desktop.app import App
from codementor.desktop.bridge import Message
from codementor.desktop.connections import KeyStore
from codementor.desktop.views import analyze_view as analyze_view_module
from codementor.models.api import CompilerStatus
from codementor.storage.db import AnalysisRow

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


def pump_history(app: App) -> None:
    """Faz F (F11): geçmiş listesi arka planda okunur; yükleme bitene kadar bekler."""
    pump(app, lambda: not app.history_view.loading)


def analyze(app: App) -> None:
    app.analyze()
    assert app.analyze_view.busy
    pump(app, lambda: not app.analyze_view.busy)


def next_hint(app: App) -> None:
    app.analyze_view.actions.next_hint()
    assert app.analyze_view.busy
    pump(app, lambda: not app.analyze_view.busy)


@pytest.fixture
def no_stop_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    """Durdur testlerinde çift tıklama korumasını kapatır (koruma ayrıca sınanır)."""
    monkeypatch.setattr(analyze_view_module, "STOP_GUARD_S", 0.0)


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


def _compilers_message(tool: str | None) -> Message:
    """`bridge` sonucu gibi bir derleyici özeti mesajı (denetleyici doğrudan sürülür)."""
    payload = [CompilerStatus(target="c", tool=tool)]
    return Message(task="compilers", kind="result", payload=payload, generation=0)


# --- Faz F (F11): SQLite işleri arka plan iş parçacığında --------------------------------------


def _list_texts(app: App) -> str:
    """Geçmiş listesindeki etiket metinleri (yükleme/boş/hata mesajları buradan okunur)."""
    labels = [
        str(child.cget("text"))
        for child in app.history_view.list.winfo_children()
        if isinstance(child, ctk.CTkLabel)
    ]
    return "\n".join(labels)


def _seed_history(app: App, *analysis_ids: str) -> None:
    """Geçmiş listesi testleri için DB'ye rapor gövdesiz kayıtlar ekler."""
    db = app.core.database()
    with db.session() as session:
        for analysis_id in analysis_ids:
            session.add(
                AnalysisRow(
                    id=analysis_id,
                    created_at=datetime.now(UTC),
                    cache_key=f"key_{analysis_id}",
                    language="c",
                    engine="none",
                    question_id=None,
                    session_id=None,
                    provider="fake",
                    model="fake",
                    early_exit=False,
                    degraded=False,
                    tokens_in=10,
                    tokens_out=20,
                    latency_ms=100,
                    report_json="{}",
                )
            )
        session.commit()
