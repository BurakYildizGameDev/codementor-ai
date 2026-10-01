"""Editör içi arama çubuğu (Ctrl+F, Faz 24): yazdıkça boyar, Enter/Shift+Enter ile gezer."""

from __future__ import annotations

import tkinter as tk
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.search import Match, find_all, step

TAG_ALL = "search"
TAG_CURRENT = "search_current"
_NAV_KEYS = {"Return", "Escape", "Shift_L", "Shift_R", "Up", "Down"}


class FindBar(ctk.CTkFrame):  # type: ignore[misc]
    """Editörün sağ üstünde açılan çubuk; `text` içindeki eşleşmeleri etiketlerle boyar."""

    def __init__(self, master: Any, text: tk.Text) -> None:
        super().__init__(
            master,
            fg_color=theme.SURFACE_2,
            corner_radius=theme.RADIUS_SM,
            border_width=1,
            border_color=theme.BORDER_STRONG,
        )
        self.text = text
        self.matches: list[Match] = []
        self.current: int | None = None
        self.entry = ctk.CTkEntry(
            self,
            width=200,
            height=30,
            placeholder_text="Ara",
            font=theme.font(12),
            fg_color=theme.SURFACE,
            border_color=theme.BORDER,
            text_color=theme.TEXT,
        )
        self.entry.pack(side="left", padx=(8, 6), pady=6)
        self.count = ctk.CTkLabel(
            self, text="", width=64, font=theme.font(12), text_color=theme.MUTED
        )
        self.count.pack(side="left")
        for label, command in (("↑", self.previous), ("↓", self.next), ("✕", self.close)):
            ctk.CTkButton(
                self,
                text=label,
                width=28,
                height=28,
                command=command,
                fg_color="transparent",
                hover_color=theme.SURFACE_3,
                text_color=theme.TEXT_SOFT,
                font=theme.font(12),
            ).pack(side="left", padx=(0, 4))

        text.tag_configure(TAG_ALL, background=theme.VIOLET_DIM)
        text.tag_configure(TAG_CURRENT, background=theme.GOLD_DIM, foreground=theme.GOLD_HOVER)
        text.tag_raise(TAG_ALL)
        text.tag_raise(TAG_CURRENT)
        text.tag_raise("sel")
        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.bind("<Return>", lambda _e: self._nav(forward=True))
        self.entry.bind("<Shift-Return>", lambda _e: self._nav(forward=False))
        self.entry.bind("<Escape>", lambda _e: self._close_event())

    # --- Genel API ----------------------------------------------------------------------

    @property
    def is_open(self) -> bool:
        return bool(self.winfo_manager() == "place")

    @property
    def query(self) -> str:
        return str(self.entry.get())

    def open(self) -> None:
        """Çubuğu gösterir; tek satırlık seçim varsa sorgu olarak alır."""
        try:
            selected = self.text.get("sel.first", "sel.last")
        except tk.TclError:
            selected = ""
        if selected and "\n" not in selected:
            self.entry.delete(0, "end")
            self.entry.insert(0, selected)
        self.place(relx=1.0, x=-28, y=14, anchor="ne")
        self.lift()
        self.entry.focus_set()
        self.entry.select_range(0, "end")
        self.refresh()

    def close(self) -> None:
        self.place_forget()
        self._clear_tags()
        self.matches, self.current = [], None
        self.text.focus_set()

    def refresh(self) -> None:
        """Eşleşmeleri metne göre yeniden hesaplar (metin ya da sorgu değişince)."""
        self._clear_tags()
        self.matches = find_all(self.text.get("1.0", "end-1c"), self.query)
        for match in self.matches:
            self.text.tag_add(TAG_ALL, match.start, match.end)
        self.current = self._first_after_cursor()
        self._show_current()

    def next(self) -> None:
        self.current = step(self.current, len(self.matches), forward=True)
        self._show_current()

    def previous(self) -> None:
        self.current = step(self.current, len(self.matches), forward=False)
        self._show_current()

    # --- İç işleyiş ---------------------------------------------------------------------

    def _on_key(self, event: Any) -> None:
        if getattr(event, "keysym", "") not in _NAV_KEYS:
            self.refresh()

    def _nav(self, *, forward: bool) -> str:
        if forward:
            self.next()
        else:
            self.previous()
        return "break"

    def _close_event(self) -> str:
        self.close()
        return "break"  # uygulamanın Esc'i (analizi durdur) tetiklenmesin

    def _clear_tags(self) -> None:
        self.text.tag_remove(TAG_ALL, "1.0", "end")
        self.text.tag_remove(TAG_CURRENT, "1.0", "end")

    def _first_after_cursor(self) -> int | None:
        if not self.matches:
            return None
        line, column = (int(part) for part in self.text.index("insert").split("."))
        for number, match in enumerate(self.matches):
            if (match.line, match.column) >= (line, column):
                return number
        return 0

    def _show_current(self) -> None:
        self.text.tag_remove(TAG_CURRENT, "1.0", "end")
        if not self.query:
            self.count.configure(text="", text_color=theme.MUTED)
            return
        if self.current is None:
            self.count.configure(text="Sonuç yok", text_color=theme.ERROR)
            return
        match = self.matches[self.current]
        self.text.tag_add(TAG_CURRENT, match.start, match.end)
        self.text.see(match.start)
        self.count.configure(
            text=f"{self.current + 1}/{len(self.matches)}", text_color=theme.TEXT_SOFT
        )
