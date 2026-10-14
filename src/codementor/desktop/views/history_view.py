"""Geçmiş: kayıtlı analizlerin listesi; satıra tıklayınca rapor (ve saklanan kod) yeniden açılır."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import ENGINE_LABELS, LANGUAGE_LABELS, format_ms
from codementor.desktop.views.questions_view import page_header
from codementor.desktop.widgets.common import Pill, clear
from codementor.log import get_logger
from codementor.models.enums import Engine, Language
from codementor.storage.db import AnalysisRow

log = get_logger("codementor.desktop")


LoadPageFn = Callable[[int, str | None, str | None], tuple[list[AnalysisRow], str | None]]
# Faz F (F11): DB işini arka planda başlatan istek (limit, imleç, arama, listeye ekle)
RequestPageFn = Callable[[int, str | None, str | None, bool], None]

LOADING_TEXT = "Yükleniyor…"
PAGE_SIZE = 50


class HistoryView(ctk.CTkFrame):  # type: ignore[misc]
    def __init__(
        self,
        master: Any,
        load: Callable[[], list[AnalysisRow]] | None = None,
        on_open: Callable[[str], None] = lambda _aid: None,
        on_delete: Callable[[str], None] | None = None,
        on_clear: Callable[[], None] | None = None,
        totals: Callable[[], str | None] | None = None,
        is_busy: Callable[[], bool] | None = None,
        load_page: LoadPageFn | None = None,
        request_page: RequestPageFn | None = None,
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self._load = load
        self._on_open = on_open
        self._on_delete = on_delete
        self._on_clear = on_clear
        self._totals = totals
        self._is_busy = is_busy

        def _fallback_page(
            limit: int, before: str | None, search: str | None
        ) -> tuple[list[AnalysisRow], str | None]:
            rows = self._load() if self._load is not None else []
            return rows[:limit], None

        self._load_page = load_page or _fallback_page
        self._request_page = request_page
        self._rows: list[AnalysisRow] = []
        self._next_cursor: str | None = None
        self._page_size = PAGE_SIZE
        self._loading = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header_frame.grid_columnconfigure(0, weight=1)

        page_header(header_frame, "Geçmiş", "Son analizlerin; açmak için bir satıra tıkla.").grid(
            row=0, column=0, sticky="w"
        )
        self.clear_btn = ctk.CTkButton(
            header_frame,
            text="Tümünü temizle",
            font=theme.font(12),
            fg_color="transparent",
            text_color=theme.MUTED,
            hover_color=theme.SURFACE_2,
            border_width=1,
            border_color=theme.BORDER,
            height=28,
            command=self._handle_clear,
        )
        self.clear_btn.grid(row=0, column=1, sticky="e")
        # Faz K: kayıtlı analizlerin toplam token/maliyeti
        self.totals_label = ctk.CTkLabel(
            header_frame, text="", font=theme.font(12), text_color=theme.MUTED, anchor="w"
        )
        self.totals_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # Faz F (F6): Arama kutusu
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Geçmişte ara (soru, dil, sağlayıcı)...",
            font=theme.font(12),
            height=30,
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.search_entry.bind("<Return>", lambda _e: self.on_search())

        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Ara",
            width=56,
            height=30,
            font=theme.font(12),
            fg_color=theme.SURFACE_2,
            hover_color=theme.SURFACE_3,
            text_color=theme.TEXT,
            command=self.on_search,
        )
        self.search_btn.grid(row=0, column=1)

        self.list = ctk.CTkScrollableFrame(
            self, fg_color="transparent", scrollbar_button_color=theme.SURFACE_3
        )
        self.list.grid(row=2, column=0, sticky="nsew")
        self.list.grid_columnconfigure(0, weight=1)
        self.load_more_btn: ctk.CTkButton | None = None

    def _handle_clear(self) -> None:
        if self._on_clear is not None:
            self._on_clear()

    def _handle_delete(self, analysis_id: str) -> None:
        if self._on_delete is not None:
            self._on_delete(analysis_id)

    def on_search(self) -> None:
        """Arama metni değiştiğinde veya Ara tıklandığında listeyi baştan tazeler."""
        self.refresh()

    @property
    def page_size(self) -> int:
        """Sayfa boyutu (denetleyici arka plan isteğini bununla kurar)."""
        return self._page_size

    @property
    def loading(self) -> bool:
        """Arka plan yüklemesi sürüyor mu (F11; testler sonucu bununla bekler)."""
        return self._loading

    def show_loading(self, *, append: bool = False) -> None:
        """Yükleme boyunca listeyi (ya da "Daha fazla" düğmesini) "Yükleniyor…" yapar (F11)."""
        self._loading = True
        if append:
            if self.load_more_btn is not None:
                self.load_more_btn.configure(text=LOADING_TEXT, state="disabled")
            return
        clear(self.list)
        self._rows, self._next_cursor, self.load_more_btn = [], None, None
        self.clear_btn.configure(state="disabled")
        ctk.CTkLabel(
            self.list, text=LOADING_TEXT, font=theme.font(13), text_color=theme.MUTED
        ).grid(row=0, column=0, pady=40)

    def apply_page(
        self,
        rows: list[AnalysisRow],
        next_cursor: str | None,
        *,
        totals: str | None = None,
        search_active: bool = False,
        append: bool = False,
    ) -> None:
        """Arka plandan gelen sayfayı çizer; `append` ise mevcut satırların altına ekler (F11)."""
        self._loading = False
        if totals is not None:
            self.totals_label.configure(text=totals)
        self._rows = [*self._rows, *rows] if append else list(rows)
        self._next_cursor = next_cursor
        self._render_rows(search_active=search_active)

    def apply_error(self, message: str) -> None:
        """Yükleme başarısızsa Türkçe metni liste yerine gösterir (F11)."""
        self._loading = False
        self._rows, self._next_cursor, self.load_more_btn = [], None, None
        clear(self.list)
        self.clear_btn.configure(state="disabled")
        ctk.CTkLabel(
            self.list,
            text=message,
            font=theme.font(13),
            text_color=theme.ERROR,
            wraplength=760,
            justify="left",
        ).grid(row=0, column=0, padx=16, pady=40, sticky="w")

    def refresh(self) -> None:
        """Listeyi baştan yükler; DB işi arka planda koşar (Faz F, F11)."""
        search_text = self.search_entry.get().strip()
        if self._request_page is not None:
            self.show_loading()
            self._request_page(self._page_size, None, search_text or None, False)
            return
        self._loading = False  # arka plan isteği yoksa (tek başına görünüm) eşzamanlı yol
        self.totals_label.configure(text=self._totals_text())
        try:
            rows, next_cursor = self._load_page(self._page_size, None, search_text or None)
        except Exception:
            rows, next_cursor = [], None
        self._rows = list(rows)
        self._next_cursor = next_cursor
        self._render_rows(search_active=bool(search_text))

    def _render_rows(self, *, search_active: bool = False) -> None:
        clear(self.list)
        if not self._rows:
            self.load_more_btn = None
            self.clear_btn.configure(state="disabled")
            msg = (
                "Arama kriterine uygun analiz bulunamadı."
                if search_active
                else "Henüz analiz yok. İlk denetimin burada görünecek."
            )
            ctk.CTkLabel(
                self.list,
                text=msg,
                font=theme.font(13),
                text_color=theme.MUTED,
            ).grid(row=0, column=0, pady=40)
            return
        self.clear_btn.configure(state="normal")
        for i, row in enumerate(self._rows):
            self._row(i, row)
        if self._next_cursor is not None:
            self.load_more_btn = ctk.CTkButton(
                self.list,
                text="Daha fazla yükle",
                font=theme.font(12),
                fg_color=theme.SURFACE_2,
                hover_color=theme.SURFACE_3,
                text_color=theme.TEXT,
                height=32,
                command=self._handle_load_more,
            )
            self.load_more_btn.grid(row=len(self._rows), column=0, sticky="ew", pady=(8, 16))
        else:
            self.load_more_btn = None

    def _handle_load_more(self) -> None:
        if self._next_cursor is None or self._loading:
            return
        search_text = self.search_entry.get().strip()
        if self._request_page is not None:  # F11: sonraki sayfa da arka planda okunur
            self.show_loading(append=True)
            self._request_page(self._page_size, self._next_cursor, search_text or None, True)
            return
        try:
            more_rows, next_cursor = self._load_page(
                self._page_size, self._next_cursor, search_text or None
            )
        except Exception:
            more_rows, next_cursor = [], None
        self._rows.extend(more_rows)
        self._next_cursor = next_cursor
        self._render_rows(search_active=bool(search_text))

    def _totals_text(self) -> str:
        if self._totals is None:
            return ""
        try:
            return self._totals() or ""
        except Exception as exc:  # veritabanı okunamazsa toplam gösterilmez (iz log'da)
            log.warning("usage_totals_failed", error=type(exc).__name__)
            return ""

    def _row(self, index: int, row: AnalysisRow) -> None:
        item = ctk.CTkFrame(
            self.list,
            fg_color=theme.SURFACE,
            corner_radius=theme.RADIUS_SM,
            border_width=1,
            border_color=theme.BORDER,
            cursor="hand2",
        )
        item.grid(row=index, column=0, sticky="ew", pady=(0, 8))
        item.grid_columnconfigure(2, weight=1)
        created = row.created_at.replace(tzinfo=row.created_at.tzinfo or UTC).astimezone()
        ctk.CTkLabel(
            item,
            text=created.strftime("%d.%m.%Y  %H:%M"),
            font=theme.font(13, "bold"),
            text_color=theme.TEXT,
            width=140,
            anchor="w",
        ).grid(row=0, column=0, padx=(18, 10), pady=14)
        language = LANGUAGE_LABELS.get(Language(row.language), row.language)
        engine = Engine(row.engine)
        label = language if engine is Engine.NONE else f"{language} · {ENGINE_LABELS[engine]}"
        Pill(item, label, theme.TEXT_SOFT).grid(row=0, column=1, padx=(0, 10))
        ctk.CTkLabel(
            item,
            text=row.question_id or "Serbest çalışma",
            font=theme.font(13),
            text_color=theme.TEXT_SOFT,
            anchor="w",
        ).grid(row=0, column=2, sticky="w")
        meta = ctk.CTkFrame(item, fg_color="transparent", width=1, height=1)
        meta.grid(row=0, column=3, sticky="e", padx=10)
        if row.degraded:
            Pill(meta, "yalnız statik", theme.WARN).pack(side="left", padx=(0, 6))
        if row.early_exit:
            Pill(meta, "derleme hatası", theme.ERROR).pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            meta,
            text=f"{row.provider or '—'} · {format_ms(row.latency_ms)}",
            font=theme.font(12),
            text_color=theme.MUTED,
        ).pack(side="left")

        busy = bool(self._is_busy()) if self._is_busy is not None else False
        del_btn = ctk.CTkButton(
            item,
            text="Sil",
            state="disabled" if busy else "normal",
            font=theme.font(11),
            fg_color="transparent",
            text_color=theme.MUTED,
            hover_color=theme.SURFACE_3,
            border_width=1,
            border_color=theme.BORDER,
            width=42,
            height=24,
            command=lambda aid=row.id: self._handle_delete(aid),
        )
        del_btn.grid(row=0, column=4, padx=(0, 14), sticky="e")

        def open_row(_event: Any = None, analysis_id: str = row.id) -> None:
            self._on_open(analysis_id)

        def hover(on: bool) -> None:
            item.configure(border_color=theme.BORDER_STRONG if on else theme.BORDER)

        clickable = [
            w for w in (item, *item.winfo_children(), *meta.winfo_children()) if w is not del_btn
        ]
        for widget in clickable:
            widget.bind("<Button-1>", open_row, add="+")
            widget.bind("<Enter>", lambda _e: hover(True), add="+")
            widget.bind("<Leave>", lambda _e: hover(False), add="+")
