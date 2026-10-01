"""Karmaşıklık kartı: büyük Big-O rozeti, alan karmaşıklığı, optimallik ve gerekçe adımları."""

from __future__ import annotations

from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.widgets.common import Card, Pill, clear, wrap_label
from codementor.models.report import ComplexityResult

MAX_STEPS = 3


class ComplexityCard(Card):
    def __init__(self, master: Any) -> None:
        super().__init__(master, title="Karmaşıklık")

    def show(self, result: ComplexityResult) -> None:
        clear(self.body)
        top = ctk.CTkFrame(self.body, fg_color="transparent", width=1, height=1)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            top, text=result.display_time, font=theme.font(30, "bold"), text_color=theme.GOLD
        ).grid(row=0, column=0, rowspan=2, sticky="w")
        ctk.CTkLabel(top, text="zaman", font=theme.font(11), text_color=theme.MUTED).grid(
            row=0, column=1, sticky="sw", padx=(10, 0)
        )
        ctk.CTkLabel(
            top,
            text=f"alan O({result.space_complexity})",
            font=theme.font(12),
            text_color=theme.TEXT_SOFT,
        ).grid(row=1, column=1, sticky="nw", padx=(10, 0))
        badge = self._badge(top, result)
        if badge is not None:
            badge.grid(row=0, column=2, rowspan=2, sticky="e")

        if result.optimal_time_target and result.is_optimal is False:
            wrap_label(
                self.body,
                f"Hedef O({result.optimal_time_target}): daha iyisi mümkün.",
                size=12,
                color=theme.WARN,
            ).grid(row=1, column=0, sticky="ew", pady=(8, 0))
        for i, step in enumerate(result.reasoning_steps[:MAX_STEPS]):
            wrap_label(self.body, f"•  {step}", size=12, color=theme.MUTED).grid(
                row=2 + i, column=0, sticky="ew", pady=(6 if i == 0 else 2, 0)
            )

    @staticmethod
    def _badge(master: Any, result: ComplexityResult) -> Pill | None:
        if result.is_optimal is True:
            return Pill(master, "✓ Optimal", theme.OK)
        if result.is_optimal is False:
            return Pill(master, "↗ İyileştirilebilir", theme.WARN)
        if result.agreement == "conflicts":
            return Pill(master, "Statik ipucuyla çelişiyor", theme.WARN)
        return None
