"""Bulgu kartları ve derleyici tanıları; kart tıklanınca editör ilgili satıra gider."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import CATEGORY_LABELS, SEVERITY_LABELS
from codementor.desktop.widgets.common import Card, Pill, clear, muted_label, wrap_label
from codementor.models.enums import Severity
from codementor.models.findings import Diagnostic, Finding

_DIAG_COLORS = {"error": theme.ERROR, "warning": theme.WARN, "note": theme.INFO}
_DIAG_LABELS = {"error": "Hata", "warning": "Uyarı", "note": "Not"}
_ORDER = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}


class FindingList(Card):
    def __init__(self, master: Any, on_select: Callable[[int], None]) -> None:
        super().__init__(master, title="Bulgular")
        self._on_select = on_select
        self.count = ctk.CTkLabel(
            self.header_right, text="", font=theme.font(12, "bold"), text_color=theme.TEXT_SOFT
        )
        self.count.pack(side="right")

    def show(self, findings: list[Finding], diagnostics: list[Diagnostic]) -> None:
        clear(self.body)
        visible = [d for d in diagnostics if d.severity != "note"]
        self.count.configure(text=str(len(findings) + len(visible)))
        row = 0
        for d in visible:
            self._item(
                row,
                _DIAG_LABELS[d.severity],
                _DIAG_COLORS[d.severity],
                d.tool,
                d.line,
                None,
                d.message,
                None,
            )
            row += 1
        for f in sorted(findings, key=lambda f: (_ORDER[f.severity], f.line_start)):
            self._item(
                row,
                SEVERITY_LABELS[f.severity],
                theme.SEVERITY_COLORS[f.severity],
                CATEGORY_LABELS[f.category],
                f.line_start,
                f.line_end,
                f.description,
                f.evidence,
            )
            row += 1
        if row == 0:
            muted_label(self.body, "Bu kodda işaretlenecek bir şey bulunmadı.").grid(
                row=0, column=0, sticky="w"
            )

    def _item(
        self,
        row: int,
        level: str,
        color: str,
        title: str,
        line: int,
        line_end: int | None,
        description: str,
        evidence: str | None,
    ) -> None:
        item = ctk.CTkFrame(
            self.body,
            fg_color=theme.SURFACE_2,
            corner_radius=theme.RADIUS_SM,
            border_width=1,
            border_color=theme.SURFACE_2,
            cursor="hand2",
        )
        item.grid(row=row, column=0, sticky="ew", pady=(0, 8))
        item.grid_columnconfigure(2, weight=1)
        ctk.CTkFrame(item, width=3, height=1, corner_radius=2, fg_color=color).grid(
            row=0, column=0, rowspan=3, sticky="ns", padx=(8, 0), pady=10
        )
        Pill(item, level, color).grid(row=0, column=1, sticky="w", padx=(12, 8), pady=(10, 0))
        ctk.CTkLabel(item, text=title, font=theme.font(12, "bold"), text_color=theme.TEXT).grid(
            row=0, column=2, sticky="w", pady=(10, 0)
        )
        span = f"Satır {line}" if not line_end or line_end == line else f"Satır {line}-{line_end}"
        ctk.CTkLabel(item, text=span, font=theme.font(11), text_color=theme.MUTED).grid(
            row=0, column=3, sticky="e", padx=12, pady=(10, 0)
        )
        wrap_label(item, description, size=13, color=theme.TEXT_SOFT).grid(
            row=1, column=1, columnspan=3, sticky="ew", padx=12, pady=(6, 0 if evidence else 10)
        )
        if evidence:
            ctk.CTkLabel(
                item,
                text=evidence.strip(),
                font=ctk.CTkFont(*theme.code_font(11)),
                text_color=theme.MUTED,
                anchor="w",
                justify="left",
            ).grid(row=2, column=1, columnspan=3, sticky="ew", padx=12, pady=(4, 10))

        def select(_event: Any = None) -> None:
            self._on_select(line)

        def hover(on: bool) -> None:
            item.configure(border_color=theme.BORDER_STRONG if on else theme.SURFACE_2)

        for widget in (item, *item.winfo_children()):
            widget.bind("<Button-1>", select, add="+")
            widget.bind("<Enter>", lambda _e: hover(True), add="+")
            widget.bind("<Leave>", lambda _e: hover(False), add="+")
