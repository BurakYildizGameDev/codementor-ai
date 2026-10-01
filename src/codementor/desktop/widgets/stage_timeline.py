"""Analiz adımları zaman çizelgesi: 6 adım, canlı durum noktaları, süreler, ilerleme çubuğu."""

from __future__ import annotations

from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import STAGE_GROUPS, GroupStatus, GroupView, format_ms
from codementor.desktop.widgets.common import Card

PULSE_MS = 420

_DOT: dict[GroupStatus, tuple[str, str]] = {
    "pending": ("○", theme.FAINT),
    "running": ("●", theme.GOLD),
    "done": ("●", theme.OK),
    "skipped": ("◌", theme.FAINT),
    "failed": ("●", theme.ERROR),
}
_TEXT: dict[GroupStatus, str] = {
    "pending": theme.FAINT,
    "running": theme.TEXT,
    "done": theme.TEXT_SOFT,
    "skipped": theme.FAINT,
    "failed": theme.ERROR,
}


class StageTimeline(Card):
    """`update_groups(...)` ile yeniden çizilir; koşan adımın noktası nabız atar."""

    def __init__(self, master: Any) -> None:
        super().__init__(master, title="Analiz akışı")
        self.total = ctk.CTkLabel(
            self.header_right, text="", font=theme.font(12, "bold"), text_color=theme.GOLD
        )
        self.total.pack(side="right")
        self.bar = ctk.CTkProgressBar(
            self.body,
            height=4,
            corner_radius=2,
            fg_color=theme.SURFACE_3,
            progress_color=theme.GOLD,
        )
        self.bar.set(0)
        self.bar.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 12))
        self._rows: list[tuple[ctk.CTkLabel, ctk.CTkLabel, ctk.CTkLabel]] = []
        grid = ctk.CTkFrame(self.body, fg_color="transparent", width=1, height=1)
        grid.grid(row=1, column=0, sticky="ew")
        grid.grid_columnconfigure((1, 4), weight=1)
        for i, group in enumerate(STAGE_GROUPS):
            r, c = divmod(i, 2)
            col = c * 3
            dot = ctk.CTkLabel(
                grid, text="○", font=theme.font(13), text_color=theme.FAINT, width=18
            )
            dot.grid(row=r, column=col, sticky="w", pady=3)
            name = ctk.CTkLabel(
                grid, text=group.label, font=theme.font(12), text_color=theme.FAINT, anchor="w"
            )
            name.grid(row=r, column=col + 1, sticky="w", padx=(6, 0))
            time = ctk.CTkLabel(grid, text="", font=theme.font(11), text_color=theme.FAINT)
            time.grid(row=r, column=col + 2, sticky="e", padx=(4, 18 if c == 0 else 0))
            self._rows.append((dot, name, time))
        self._pulse_on = False
        self._pulse_job: str | None = None
        self._running: set[int] = set()

    def update_groups(
        self, groups: list[GroupView], ratio: float, total_ms: int, busy: bool
    ) -> None:
        self._running = set()
        for i, (view, (dot, name, time)) in enumerate(zip(groups, self._rows, strict=True)):
            symbol, color = _DOT[view.status]
            dot.configure(text=symbol, text_color=color)
            name.configure(text_color=_TEXT[view.status])
            show = view.status in ("done", "failed") and view.duration_ms > 0
            time.configure(text=format_ms(view.duration_ms) if show else "")
            if view.status == "running":
                self._running.add(i)
        self.bar.set(ratio)
        self.bar.configure(progress_color=theme.GOLD if busy or ratio < 1 else theme.OK)
        self.total.configure(text=format_ms(total_ms) if total_ms else "")
        if busy and self._pulse_job is None:
            self._pulse()
        elif not busy and self._pulse_job is not None:
            self.after_cancel(self._pulse_job)
            self._pulse_job = None

    def _pulse(self) -> None:
        self._pulse_on = not self._pulse_on
        for i in self._running:
            self._rows[i][0].configure(text_color=theme.GOLD if self._pulse_on else theme.GOLD_DIM)
        self._pulse_job = self.after(PULSE_MS, self._pulse)
