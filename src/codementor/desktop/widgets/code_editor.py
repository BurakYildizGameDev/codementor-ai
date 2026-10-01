"""Kod editörü: satır numaraları, sözdizimi renkleri, bulgu işaretleri, arama ve alt bilgi."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.highlight import tokenize
from codementor.desktop.viewmodel import LineMark
from codementor.desktop.widgets.find_bar import FindBar
from codementor.models.enums import Language, Severity

HIGHLIGHT_DELAY_MS = 120
TAB = "    "


class CodeEditor(ctk.CTkFrame):  # type: ignore[misc]
    """`tk.Text` tabanlı editör; işaretli satırın mesajı imleç oradayken alt şeritte görünür."""

    def __init__(self, master: Any, on_change: Callable[[], None] | None = None) -> None:
        super().__init__(
            master,
            fg_color=theme.SURFACE,
            corner_radius=theme.RADIUS,
            border_width=1,
            border_color=theme.BORDER,
        )
        self._language = Language.C
        self._marks: dict[int, LineMark] = {}
        self._pending: str | None = None
        self._on_change = on_change
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        size = 13
        self.gutter = tk.Canvas(
            self, width=52, bg=theme.SURFACE, highlightthickness=0, borderwidth=0
        )
        self.gutter.grid(row=0, column=0, sticky="ns", padx=(10, 0), pady=(10, 0))
        self.text = tk.Text(
            self,
            wrap="none",
            undo=True,
            maxundo=200,
            font=theme.code_font(size),
            bg=theme.SURFACE,
            fg=theme.TEXT,
            insertbackground=theme.GOLD,
            insertwidth=2,
            selectbackground=theme.SURFACE_3,
            selectforeground=theme.TEXT,
            inactiveselectbackground=theme.SURFACE_2,
            borderwidth=0,
            highlightthickness=0,
            padx=12,
            pady=10,
            spacing1=2,
            spacing3=2,
        )
        self.text.grid(row=0, column=1, sticky="nsew", pady=(10, 0))
        yscroll = ctk.CTkScrollbar(
            self,
            command=self._yview,
            button_color=theme.SURFACE_3,
            button_hover_color=theme.BORDER_STRONG,
        )
        yscroll.grid(row=0, column=2, sticky="ns", padx=(0, 6), pady=10)
        xscroll = ctk.CTkScrollbar(
            self,
            orientation="horizontal",
            command=self.text.xview,
            button_color=theme.SURFACE_3,
            button_hover_color=theme.BORDER_STRONG,
            height=12,
        )
        xscroll.grid(row=1, column=1, sticky="ew")

        def on_yscroll(first: float, last: float) -> None:
            yscroll.set(first, last)
            self._redraw_gutter()

        self.text.configure(yscrollcommand=on_yscroll, xscrollcommand=xscroll.set)

        self.footer = ctk.CTkLabel(
            self,
            text="",
            font=theme.font(12),
            text_color=theme.MUTED,
            anchor="w",
            justify="left",
            height=30,
        )
        self.footer.grid(row=2, column=0, columnspan=3, sticky="ew", padx=18, pady=(2, 8))

        for token, color in theme.SYNTAX.items():
            self.text.tag_configure(token, foreground=color)
        self.text.tag_configure("comment", font=(theme.code_family(), size, "italic"))
        for level, color in theme.LINE_BACKGROUNDS.items():
            self.text.tag_configure(f"line_{level}", background=color)
        self.text.tag_configure("focus", background=theme.GOLD_DIM)
        self.text.tag_raise("sel")

        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<Tab>", self._insert_tab)
        self.text.bind("<KeyRelease>", lambda _e: self._update_footer(), add="+")
        self.text.bind("<ButtonRelease-1>", lambda _e: self._update_footer(), add="+")
        self.text.bind("<Configure>", lambda _e: self._redraw_gutter(), add="+")
        self.find_bar = FindBar(self, self.text)
        for sequence in ("<Control-f>", "<Control-F>"):
            self.text.bind(sequence, self._open_find)

    # --- Genel API ----------------------------------------------------------------------

    def get(self) -> str:
        return self.text.get("1.0", "end-1c")

    def set(self, code: str, language: Language | None = None) -> None:
        if language is not None:
            self._language = language
        self.text.delete("1.0", "end")
        self.text.insert("1.0", code)
        self.text.edit_reset()
        self.text.mark_set("insert", "1.0")
        self.text.see("1.0")
        self.set_marks([])
        self._highlight()

    def set_language(self, language: Language) -> None:
        self._language = language
        self._highlight()

    def line_count(self) -> int:
        return int(self.text.index("end-1c").split(".")[0])

    def set_marks(self, marks: list[LineMark]) -> None:
        """Bulgu satırlarını boyar; boş liste işaretleri temizler."""
        for level in Severity:
            self.text.tag_remove(f"line_{level}", "1.0", "end")
        self.text.tag_remove("focus", "1.0", "end")
        self._marks = {m.line: m for m in marks}
        for m in marks:
            self.text.tag_add(f"line_{m.level}", f"{m.line}.0", f"{m.line}.0 lineend+1c")
        self._redraw_gutter()
        self._update_footer()

    def goto(self, line: int) -> None:
        """Satırı görünür yapar, imleci oraya taşır ve kısa süre vurgular."""
        line = max(1, min(line, self.line_count()))
        self.text.tag_remove("focus", "1.0", "end")
        self.text.tag_add("focus", f"{line}.0", f"{line}.0 lineend+1c")
        self.text.mark_set("insert", f"{line}.0")
        self.text.see(f"{line}.0")
        self.text.focus_set()
        self._update_footer()
        self.after(1400, lambda: self.text.tag_remove("focus", "1.0", "end"))

    # --- İç işleyiş ---------------------------------------------------------------------

    def _yview(self, *args: Any) -> None:
        self.text.yview(*args)
        self._redraw_gutter()

    def _open_find(self, _event: Any) -> str:
        self.find_bar.open()
        return "break"

    def _insert_tab(self, _event: Any) -> str:
        self.text.insert("insert", TAB)
        return "break"

    def _on_modified(self, _event: Any) -> None:
        if not self.text.edit_modified():
            return
        self.text.edit_modified(False)
        if self._pending is not None:
            self.after_cancel(self._pending)
        self._pending = self.after(HIGHLIGHT_DELAY_MS, self._highlight)
        self._redraw_gutter()
        if self.find_bar.is_open:
            self.find_bar.refresh()
        if self._marks:  # işaretler analiz edilen koda aitti
            self.set_marks([])
        if self._on_change is not None:
            self._on_change()

    def _highlight(self) -> None:
        self._pending = None
        for token in theme.SYNTAX:
            self.text.tag_remove(token, "1.0", "end")
        for token, start, end in tokenize(self.get(), self._language):
            self.text.tag_add(token, f"1.0+{start}c", f"1.0+{end}c")

    def _redraw_gutter(self) -> None:
        self.gutter.delete("all")
        current = self.text.index("insert").split(".")[0]
        index = self.text.index("@0,0")
        while True:
            info = self.text.dlineinfo(index)
            if info is None:
                break
            y, height = info[1], info[3]
            line = int(index.split(".")[0])
            mark = self._marks.get(line)
            if mark is not None:
                self.gutter.create_rectangle(
                    46,
                    y + 3,
                    50,
                    y + height - 3,
                    fill=theme.SEVERITY_COLORS[mark.level],
                    outline="",
                )
            color = theme.TEXT_SOFT if str(line) == current else theme.FAINT
            self.gutter.create_text(
                38,
                y + height // 2,
                anchor="e",
                text=str(line),
                fill=color,
                font=theme.code_font(11),
            )
            next_index = self.text.index(f"{index}+1line")
            if next_index == index:
                break
            index = next_index

    def _update_footer(self) -> None:
        line = int(self.text.index("insert").split(".")[0])
        mark = self._marks.get(line)
        if mark is None:
            hint = (
                "Bulgu satırına tıkla ya da sağdaki karttan seç."
                if self._marks
                else "Ctrl+Enter ile denetle"
            )
            self.footer.configure(text=f"Satır {line}   {hint}", text_color=theme.MUTED)
        else:
            self.footer.configure(
                text=f"Satır {line}  ·  " + "   |   ".join(mark.messages),
                text_color=theme.SEVERITY_COLORS[mark.level],
            )
        self._redraw_gutter()
