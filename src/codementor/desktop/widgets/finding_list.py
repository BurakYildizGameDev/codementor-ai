"""Bulgu kartları ve derleyici tanıları; kart tıklanınca editör ilgili satıra gider.

Faz 36: önce hatalar ve tanılar; öneriler "Öneriler (n)" düğmesinin altında katlı.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import CATEGORY_LABELS, SEVERITY_LABELS, split_findings
from codementor.desktop.widgets.common import Card, Pill, clear, muted_label, wrap_label
from codementor.models.findings import Diagnostic, Finding

_DIAG_COLORS = {"error": theme.ERROR, "warning": theme.WARN, "note": theme.INFO}
_DIAG_LABELS = {"error": "Hata", "warning": "Uyarı", "note": "Not"}


class FindingList(Card):
    def __init__(self, master: Any, on_select: Callable[[int], None]) -> None:
        super().__init__(master, title="Hatalar")
        self._on_select = on_select
        self.suggestion_toggle: ctk.CTkButton | None = None
        self.suggestion_body: ctk.CTkFrame | None = None
        self.count = ctk.CTkLabel(
            self.header_right, text="", font=theme.font(12, "bold"), text_color=theme.TEXT_SOFT
        )
        self.count.pack(side="right")

    def show(self, findings: list[Finding], diagnostics: list[Diagnostic]) -> None:
        clear(self.body)
        self.suggestion_toggle = self.suggestion_body = None
        issues, suggestions = split_findings(findings)
        visible = [d for d in diagnostics if d.severity != "note"]
        self.count.configure(text=str(len(issues) + len(visible)))
        row = 0
        for d in visible:
            self._item(
                self.body,
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
        for f in issues:
            self._finding(self.body, row, f)
            row += 1
        if row == 0:
            text = "Hata bulunmadı." if suggestions else "Bu kodda işaretlenecek bir şey bulunmadı."
            muted_label(self.body, text).grid(row=0, column=0, sticky="w")
            row += 1
        if suggestions:
            self._suggestions(row, suggestions)

    def _suggestions(self, row: int, suggestions: list[Finding]) -> None:
        """Öneriler katlı başlar; düğme açıp kapatır (öğrenci önce hataları görür)."""
        label = f"Öneriler ({len(suggestions)})"
        body = ctk.CTkFrame(self.body, fg_color="transparent")
        body.grid_columnconfigure(0, weight=1)
        for i, f in enumerate(suggestions):
            self._finding(body, i, f)

        def toggle() -> None:
            if body.grid_info():
                body.grid_forget()
                button.configure(text=f"{label} ▸")
            else:
                body.grid(row=row + 1, column=0, sticky="ew")
                button.configure(text=f"{label} ▾")

        button = ctk.CTkButton(
            self.body,
            text=f"{label} ▸",
            command=toggle,
            fg_color="transparent",
            hover_color=theme.SURFACE_2,
            text_color=theme.TEXT_SOFT,
            font=theme.font(12, "bold"),
            anchor="w",
        )
        button.grid(row=row, column=0, sticky="w", pady=(4, 8))
        self.suggestion_toggle, self.suggestion_body = button, body

    def _finding(self, parent: Any, row: int, f: Finding) -> None:
        self._item(
            parent,
            row,
            SEVERITY_LABELS[f.severity],
            theme.SEVERITY_COLORS[f.severity],
            CATEGORY_LABELS[f.category],
            f.line_start,
            f.line_end,
            f.description,
            f.evidence,
        )

    def _item(
        self,
        parent: Any,
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
            parent,
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
