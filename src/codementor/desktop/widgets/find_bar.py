"""Editör içi arama/değiştirme çubuğu (Ctrl+F / Ctrl+H, Faz 24 ve 33): yazdıkça boyar,
Enter/Shift+Enter ile gezer; büyük/küçük harf ve tam sözcük seçenekleri."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.search import Match, find_all, replace_all, step

TAG_ALL = "search"
TAG_CURRENT = "search_current"
_NAV_KEYS = {"Return", "Escape", "Shift_L", "Shift_R", "Up", "Down"}


class FindBar(ctk.CTkFrame):  # type: ignore[misc]
    """Editörün sağ üstünde açılan çubuk; `text` içindeki eşleşmeleri etiketlerle boyar.

    `notify` değiştirme sonucunu kullanıcıya bildirir (uygulamanın toast'ı)."""

    def __init__(
        self, master: Any, text: tk.Text, notify: Callable[[str], None] | None = None
    ) -> None:
        super().__init__(
            master,
            fg_color=theme.SURFACE_2,
            corner_radius=theme.RADIUS_SM,
            border_width=1,
            border_color=theme.BORDER_STRONG,
        )
        self.text = text
        self.notify = notify
        self.matches: list[Match] = []
        self.current: int | None = None
        self.replace_open = False
        self.case_var = tk.BooleanVar(value=False)
        self.word_var = tk.BooleanVar(value=False)

        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.pack(side="top", fill="x")
        self.entry = self._entry(search_row, "Ara")
        self.entry.pack(side="left", padx=(8, 6), pady=6)
        # "Aa": büyük/küçük harf duyarlı · "ab|": tam sözcük
        for label, var in (("Aa", self.case_var), ("ab|", self.word_var)):
            ctk.CTkCheckBox(
                search_row,
                text=label,
                variable=var,
                command=self.refresh,
                width=20,
                checkbox_width=16,
                checkbox_height=16,
                font=theme.font(11),
                text_color=theme.TEXT_SOFT,
            ).pack(side="left", padx=(0, 6))
        self.count = ctk.CTkLabel(
            search_row, text="", width=64, font=theme.font(12), text_color=theme.MUTED
        )
        self.count.pack(side="left")
        for label, command in (("↑", self.previous), ("↓", self.next), ("✕", self.close)):
            self._button(search_row, label, command).pack(side="left", padx=(0, 4))

        self.replace_row = ctk.CTkFrame(self, fg_color="transparent")
        self.replace_entry = self._entry(self.replace_row, "Değiştir")
        self.replace_entry.pack(side="left", padx=(8, 6), pady=(0, 6))
        self._button(self.replace_row, "Değiştir", self.replace_current, width=72).pack(
            side="left", padx=(0, 4), pady=(0, 6)
        )
        self._button(self.replace_row, "Tümü", self.replace_every, width=52).pack(
            side="left", padx=(0, 4), pady=(0, 6)
        )

        text.tag_configure(TAG_ALL, background=theme.VIOLET_DIM)
        text.tag_configure(TAG_CURRENT, background=theme.GOLD_DIM, foreground=theme.GOLD_HOVER)
        text.tag_raise(TAG_ALL)
        text.tag_raise(TAG_CURRENT)
        text.tag_raise("sel")
        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.bind("<Return>", lambda _e: self._nav(forward=True))
        self.entry.bind("<Shift-Return>", lambda _e: self._nav(forward=False))
        self.entry.bind("<Escape>", lambda _e: self._close_event())
        self.replace_entry.bind("<Return>", lambda _e: self._replace_event())
        self.replace_entry.bind("<Escape>", lambda _e: self._close_event())

    @staticmethod
    def _entry(master: Any, placeholder: str) -> ctk.CTkEntry:
        return ctk.CTkEntry(
            master,
            width=200,
            height=30,
            placeholder_text=placeholder,
            font=theme.font(12),
            fg_color=theme.SURFACE,
            border_color=theme.BORDER,
            text_color=theme.TEXT,
        )

    @staticmethod
    def _button(
        master: Any, label: str, command: Callable[[], None], width: int = 28
    ) -> ctk.CTkButton:
        return ctk.CTkButton(
            master,
            text=label,
            width=width,
            height=28,
            command=command,
            fg_color="transparent",
            hover_color=theme.SURFACE_3,
            text_color=theme.TEXT_SOFT,
            font=theme.font(12),
        )

    # --- Genel API ----------------------------------------------------------------------

    @property
    def is_open(self) -> bool:
        return bool(self.winfo_manager() == "place")

    @property
    def query(self) -> str:
        return str(self.entry.get())

    @property
    def replacement(self) -> str:
        return str(self.replace_entry.get())

    def open(self, *, replace: bool = False) -> None:
        """Çubuğu gösterir; tek satırlık seçim varsa sorgu olarak alır. `replace` (Ctrl+H)
        değiştirme satırını da açar."""
        try:
            selected = self.text.get("sel.first", "sel.last")
        except tk.TclError:
            selected = ""
        if selected and "\n" not in selected:
            self.entry.delete(0, "end")
            self.entry.insert(0, selected)
        self._show_replace(replace)
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
        """Eşleşmeleri metne göre yeniden hesaplar (metin, sorgu ya da seçenek değişince)."""
        self._clear_tags()
        self.matches = find_all(
            self.text.get("1.0", "end-1c"),
            self.query,
            case_sensitive=bool(self.case_var.get()),
            whole_word=bool(self.word_var.get()),
        )
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

    def replace_current(self) -> None:
        """Seçili eşleşmeyi değiştirir ve sıradakine geçer."""
        if self.current is None or not self.matches:
            return
        match = self.matches[self.current]
        self.text.delete(match.start, match.end)
        self.text.insert(match.start, self.replacement)
        self.text.mark_set("insert", f"{match.line}.{match.column + len(self.replacement)}")
        self.refresh()

    def replace_every(self) -> None:
        """Tüm eşleşmeleri tek düzenlemede değiştirir (Ctrl+Z ile tek adımda geri alınır)."""
        original = self.text.get("1.0", "end-1c")
        updated, count = replace_all(
            original,
            self.query,
            self.replacement,
            case_sensitive=bool(self.case_var.get()),
            whole_word=bool(self.word_var.get()),
        )
        if count:
            self.text.edit_separator()
            self.text.delete("1.0", "end")
            self.text.insert("1.0", updated)
            self.text.edit_separator()
        if self.notify is not None:
            self.notify(f"{count} eşleşme değiştirildi" if count else "Değiştirilecek eşleşme yok")
        self.refresh()

    # --- İç işleyiş ---------------------------------------------------------------------

    def _show_replace(self, show: bool) -> None:
        self.replace_open = show
        if show:
            self.replace_row.pack(side="top", fill="x")
        else:
            self.replace_row.pack_forget()

    def _on_key(self, event: Any) -> None:
        if getattr(event, "keysym", "") not in _NAV_KEYS:
            self.refresh()

    def _nav(self, *, forward: bool) -> str:
        if forward:
            self.next()
        else:
            self.previous()
        return "break"

    def _replace_event(self) -> str:
        self.replace_current()
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
