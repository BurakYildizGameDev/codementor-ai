"""Soru bankası: dil filtreli görev kartları; seçilen görev analiz ekranına bağlamıyla açılır."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import DIFFICULTY_LABELS, ENGINE_LABELS, LANGUAGE_LABELS
from codementor.desktop.widgets.common import Pill, clear, wrap_label
from codementor.desktop.widgets.task_card import DIFFICULTY_COLORS
from codementor.models.enums import Engine, Language
from codementor.models.questions import QuestionPublic

ALL = "Tümü"
PREVIEW_CHARS = 170


def page_header(master: Any, title: str, subtitle: str) -> ctk.CTkFrame:
    """Ekran başlığı (büyük başlık + açıklama)."""
    header = ctk.CTkFrame(master, fg_color="transparent", width=1, height=1)
    ctk.CTkLabel(header, text=title, font=theme.font(24, "bold"), text_color=theme.TEXT).pack(
        anchor="w"
    )
    ctk.CTkLabel(header, text=subtitle, font=theme.font(13), text_color=theme.MUTED).pack(
        anchor="w", pady=(2, 0)
    )
    return header


class QuestionsView(ctk.CTkFrame):  # type: ignore[misc]
    def __init__(
        self,
        master: Any,
        load: Callable[[Language | None], list[QuestionPublic]],
        on_start: Callable[[QuestionPublic], None],
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self._load = load
        self._on_start = on_start
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        page_header(
            self,
            "Soru bankası",
            "Bir görev seç; CodeMentor çözümünü bu görevin hedefine göre değerlendirir.",
        ).grid(row=0, column=0, sticky="w", pady=(0, 16))
        self.filter = ctk.CTkSegmentedButton(
            self,
            values=[ALL, *LANGUAGE_LABELS.values()],
            command=lambda _v: self.refresh(),
            height=34,
            corner_radius=10,
            font=theme.font(13),
            fg_color=theme.SURFACE,
            selected_color=theme.SURFACE_3,
            selected_hover_color=theme.BORDER_STRONG,
            unselected_color=theme.SURFACE,
            unselected_hover_color=theme.SURFACE_2,
        )
        self.filter.set(ALL)
        self.filter.grid(row=1, column=0, sticky="w", pady=(0, 14))
        self.grid_area = ctk.CTkScrollableFrame(
            self, fg_color="transparent", scrollbar_button_color=theme.SURFACE_3
        )
        self.grid_area.grid(row=2, column=0, sticky="nsew")
        self.grid_area.grid_columnconfigure((0, 1), weight=1, uniform="cards")

    def refresh(self) -> None:
        clear(self.grid_area)
        label = self.filter.get()
        language = next((lang for lang, text in LANGUAGE_LABELS.items() if text == label), None)
        questions = self._load(language)
        if not questions:
            ctk.CTkLabel(
                self.grid_area,
                text="Soru bankası boş ya da okunamadı.",
                font=theme.font(13),
                text_color=theme.MUTED,
            ).grid(row=0, column=0)
        for i, question in enumerate(questions):
            r, c = divmod(i, 2)
            self._card(question).grid(
                row=r,
                column=c,
                sticky="nsew",
                padx=(0, theme.GAP) if c == 0 else 0,
                pady=(0, theme.GAP),
            )

    def _card(self, q: QuestionPublic) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            self.grid_area,
            fg_color=theme.SURFACE,
            corner_radius=theme.RADIUS,
            border_width=1,
            border_color=theme.BORDER,
        )
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(2, weight=1)
        tags = ctk.CTkFrame(card, fg_color="transparent", width=1, height=1)
        tags.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 0))
        Pill(tags, DIFFICULTY_LABELS[q.difficulty], DIFFICULTY_COLORS[q.difficulty]).pack(
            side="left"
        )
        Pill(tags, LANGUAGE_LABELS[q.language], theme.TEXT_SOFT).pack(side="left", padx=6)
        if q.engine is not Engine.NONE:
            Pill(tags, ENGINE_LABELS[q.engine], theme.VIOLET).pack(side="left")
        ctk.CTkLabel(tags, text=q.id, font=theme.font(10), text_color=theme.FAINT).pack(
            side="right"
        )
        wrap_label(card, q.title, size=15, weight="bold").grid(
            row=1, column=0, sticky="ew", padx=18, pady=(10, 4)
        )
        prompt = " ".join(q.prompt.split())
        if len(prompt) > PREVIEW_CHARS:
            prompt = prompt[:PREVIEW_CHARS].rsplit(" ", 1)[0] + "…"
        wrap_label(card, prompt, size=12, color=theme.MUTED).grid(
            row=2, column=0, sticky="new", padx=18
        )
        ctk.CTkButton(
            card,
            text="Bu görevi çalış  →",
            command=lambda: self._on_start(q),
            height=34,
            corner_radius=10,
            font=theme.font(13, "bold"),
            fg_color="transparent",
            hover_color=theme.GOLD_DIM,
            text_color=theme.GOLD,
            border_width=1,
            border_color=theme.GOLD_DIM,
        ).grid(row=3, column=0, sticky="w", padx=18, pady=(12, 16))
        return card
