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
from codementor.models.enums import Engine, Language
from codementor.storage.db import AnalysisRow


class HistoryView(ctk.CTkFrame):  # type: ignore[misc]
    def __init__(
        self,
        master: Any,
        load: Callable[[], list[AnalysisRow]],
        on_open: Callable[[str], None],
        on_delete: Callable[[str], None] | None = None,
        on_clear: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self._load = load
        self._on_open = on_open
        self._on_delete = on_delete
        self._on_clear = on_clear
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 16))
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

        self.list = ctk.CTkScrollableFrame(
            self, fg_color="transparent", scrollbar_button_color=theme.SURFACE_3
        )
        self.list.grid(row=1, column=0, sticky="nsew")
        self.list.grid_columnconfigure(0, weight=1)

    def _handle_clear(self) -> None:
        if self._on_clear is not None:
            self._on_clear()

    def _handle_delete(self, analysis_id: str) -> None:
        if self._on_delete is not None:
            self._on_delete(analysis_id)

    def refresh(self) -> None:
        clear(self.list)
        try:
            rows = self._load()
        except Exception:  # veritabanı açılamazsa ekran yine açılır
            rows = []
        if not rows:
            self.clear_btn.configure(state="disabled")
            ctk.CTkLabel(
                self.list,
                text="Henüz analiz yok. İlk denetimin burada görünecek.",
                font=theme.font(13),
                text_color=theme.MUTED,
            ).grid(row=0, column=0, pady=40)
            return
        self.clear_btn.configure(state="normal")
        for i, row in enumerate(rows):
            self._row(i, row)

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

        del_btn = ctk.CTkButton(
            item,
            text="Sil",
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
