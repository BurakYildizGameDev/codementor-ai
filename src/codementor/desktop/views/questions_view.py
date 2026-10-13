"""Soru bankası: dil ve zorluk filtreli görev kartları; seçilen görev analiz ekranına açılır."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import DIFFICULTY_LABELS, ENGINE_LABELS, LANGUAGE_LABELS
from codementor.desktop.widgets.common import Pill, clear, wrap_label
from codementor.desktop.widgets.task_card import DIFFICULTY_COLORS
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import QuestionPublic

ALL = "Tümü"
MINE = "Kendi sorularım"  # Faz K
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
        load: Callable[[Language | None, Difficulty | None], list[QuestionPublic] | None],
        on_start: Callable[[QuestionPublic], None],
        on_add: Callable[[], object] | None = None,
        on_edit: Callable[[QuestionPublic], object] | None = None,
        on_delete: Callable[[QuestionPublic], object] | None = None,
        warnings: Callable[[], list[str]] | None = None,
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self._load = load
        self._on_start = on_start
        self._on_edit = on_edit
        self._on_delete = on_delete
        self._warnings = warnings
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        header.grid_columnconfigure(0, weight=1)
        page_header(
            header,
            "Soru bankası",
            "Bir görev seç; CodeMentor çözümünü bu görevin hedefine göre değerlendirir.",
        ).grid(row=0, column=0, sticky="w")
        if on_add is not None:  # Faz K: kendi sorunu ekle
            self.add_button = ctk.CTkButton(
                header,
                text="+ Soru ekle",
                command=on_add,
                height=34,
                corner_radius=10,
                font=theme.font(13, "bold"),
                fg_color=theme.GOLD,
                hover_color=theme.GOLD_HOVER,
                text_color=theme.GOLD_INK,
            )
            self.add_button.grid(row=0, column=1, sticky="e")
        filters = ctk.CTkFrame(self, fg_color="transparent")
        filters.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        filters.grid_columnconfigure(2, weight=1)
        self.filter = self._segmented(filters, [ALL, *LANGUAGE_LABELS.values()])
        self.filter.grid(row=0, column=0, sticky="w")
        # Faz 30: soru sayısı arttı; zorluk filtresi dil filtresiyle birlikte (VE) uygulanır
        self.difficulty_filter = self._segmented(filters, [ALL, *DIFFICULTY_LABELS.values()])
        self.difficulty_filter.grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.origin_filter = self._segmented(filters, [ALL, MINE])
        self.origin_filter.grid(row=0, column=2, sticky="e")
        self.count_label = ctk.CTkLabel(
            filters, text="", font=theme.font(12), text_color=theme.MUTED
        )
        self.count_label.grid(row=1, column=2, sticky="e")
        self.grid_area = ctk.CTkScrollableFrame(
            self, fg_color="transparent", scrollbar_button_color=theme.SURFACE_3
        )
        self.grid_area.grid(row=2, column=0, sticky="nsew")
        self.grid_area.grid_columnconfigure((0, 1), weight=1, uniform="cards")

    def _segmented(self, master: Any, values: list[str]) -> ctk.CTkSegmentedButton:
        button = ctk.CTkSegmentedButton(
            master,
            values=values,
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
        button.set(ALL)
        return button

    def refresh(self) -> None:
        clear(self.grid_area)
        label, level = self.filter.get(), self.difficulty_filter.get()
        language = next((lang for lang, text in LANGUAGE_LABELS.items() if text == label), None)
        difficulty = next((d for d, text in DIFFICULTY_LABELS.items() if text == level), None)
        loaded = self._load(language, difficulty)
        questions = loaded or []
        mine = self.origin_filter.get() == MINE
        if mine:
            questions = [q for q in questions if q.origin == "user"]
        skipped = len(self._warnings()) if self._warnings is not None else 0
        # denetim (K O-5): okunamayan kendi soru dosyaları sessizce kaybolmasın (ADR-0028 §6)
        note = f" · {skipped} kendi soru dosyası okunamadı (log'a bakın)" if skipped else ""
        self.count_label.configure(text=f"{len(questions)} soru{note}")
        if not questions:
            filtered = language is not None or difficulty is not None
            if loaded is None:
                text = "Soru bankası boş ya da okunamadı."
            elif mine and not filtered:
                text = "Henüz kendi sorun yok. “+ Soru ekle” ile ekleyebilirsin."
            elif filtered or mine:
                text = "Bu filtrelerle eşleşen soru yok."
            else:
                text = "Soru bankası boş ya da okunamadı."
            ctk.CTkLabel(
                self.grid_area,
                text=text,
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
        if q.origin == "user":
            Pill(tags, "Kendi sorum", theme.GOLD).pack(side="left", padx=(6, 0))
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
        actions = ctk.CTkFrame(card, fg_color="transparent", width=1, height=1)
        actions.grid(row=3, column=0, sticky="ew", padx=18, pady=(12, 16))
        ctk.CTkButton(
            actions,
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
        ).pack(side="left")
        if q.origin == "user":
            self._owner_buttons(actions, q)
        return card

    def _owner_buttons(self, master: Any, q: QuestionPublic) -> None:
        """Kendi soruların için Düzenle / Sil (Faz K)."""
        for text, callback in (("Sil", self._on_delete), ("Düzenle", self._on_edit)):
            if callback is None:
                continue
            ctk.CTkButton(
                master,
                text=text,
                command=lambda cb=callback: cb(q),
                width=70,
                height=30,
                corner_radius=9,
                font=theme.font(12),
                fg_color="transparent",
                hover_color=theme.SURFACE_3,
                text_color=theme.MUTED,
                border_width=1,
                border_color=theme.BORDER,
            ).pack(side="right", padx=(6, 0))
