"""Seçili soru bankası görevinin özeti (başlık, zorluk, problem metni, kısıtlar)."""

from __future__ import annotations

from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import DIFFICULTY_LABELS
from codementor.desktop.widgets.common import Pill, clear, wrap_label
from codementor.models.enums import Difficulty
from codementor.models.questions import QuestionPublic

DIFFICULTY_COLORS: dict[Difficulty, str] = {
    Difficulty.VERY_EASY: theme.OK,
    Difficulty.EASY: theme.OK,
    Difficulty.MEDIUM: theme.WARN,
    Difficulty.HARD: theme.ERROR,
}


class TaskCard(ctk.CTkFrame):  # type: ignore[misc]
    """Editörün üstünde, altın kenarlı görev şeridi; açılıp kapanabilir."""

    def __init__(self, master: Any) -> None:
        super().__init__(
            master,
            fg_color=theme.SURFACE,
            corner_radius=theme.RADIUS,
            border_width=1,
            border_color=theme.GOLD_DIM,
        )
        self.grid_columnconfigure(0, weight=1)
        self._expanded = True
        self._question: QuestionPublic | None = None

    def show(self, question: QuestionPublic) -> None:
        self._question = question
        self._render()

    def _toggle(self) -> None:
        self._expanded = not self._expanded
        self._render()

    def _render(self) -> None:
        clear(self)
        q = self._question
        if q is None:
            return
        head = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        head.grid(row=0, column=0, sticky="ew", padx=18, pady=(12, 12 if not self._expanded else 4))
        head.grid_columnconfigure(2, weight=1)
        ctk.CTkLabel(head, text="GÖREV", font=theme.font(10, "bold"), text_color=theme.GOLD).grid(
            row=0, column=0, padx=(0, 10)
        )
        ctk.CTkLabel(head, text=q.title, font=theme.font(14, "bold"), text_color=theme.TEXT).grid(
            row=0, column=1, sticky="w"
        )
        Pill(head, DIFFICULTY_LABELS[q.difficulty], DIFFICULTY_COLORS[q.difficulty]).grid(
            row=0, column=2, sticky="w", padx=10
        )
        ctk.CTkButton(
            head,
            text="Gizle ▴" if self._expanded else "Göster ▾",
            width=74,
            height=26,
            fg_color="transparent",
            hover_color=theme.SURFACE_2,
            text_color=theme.MUTED,
            font=theme.font(11),
            command=self._toggle,
        ).grid(row=0, column=3, sticky="e")
        if not self._expanded:
            return
        wrap_label(self, q.prompt.strip(), size=13, color=theme.TEXT_SOFT).grid(
            row=1, column=0, sticky="ew", padx=18, pady=(2, 4)
        )
        for i, constraint in enumerate(q.constraints):
            wrap_label(self, f"•  {constraint}", size=12, color=theme.MUTED).grid(
                row=2 + i,
                column=0,
                sticky="ew",
                padx=18,
                pady=(0, 12 if i == len(q.constraints) - 1 else 0),
            )
