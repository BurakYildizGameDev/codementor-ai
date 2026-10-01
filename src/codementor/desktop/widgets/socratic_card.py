"""Sokratik mentor kartı: ana kavram, ipucu merdiveni, yönlendirici sorular, sonraki adım."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import HINT_LEVEL_LABELS, MAX_HINT_LEVEL
from codementor.desktop.widgets.common import Card, clear, muted_label, wrap_label
from codementor.models.report import SocraticResult


class SocraticCard(Card):
    """Arayüzün merkezi: cevabı değil, doğru soruyu gösterir."""

    def __init__(
        self, master: Any, on_next_hint: Callable[[], None], on_restart: Callable[[], None]
    ) -> None:
        super().__init__(master, title="Sokratik mentor", accent=theme.VIOLET)
        self._on_next_hint = on_next_hint
        self._on_restart = on_restart
        self.show_empty()

    def show_empty(self) -> None:
        clear(self.body)
        wrap_label(
            self.body, "Kodunu yaz ya da aç, sonra Denetle'ye bas.", size=16, weight="bold"
        ).grid(row=0, column=0, sticky="ew")
        wrap_label(
            self.body,
            "CodeMentor kodunu düzeltmez. Hatayı kendin bulman için sana doğru soruyu sorar; "
            "takılırsan ipucunu adım adım açar.",
            size=13,
            color=theme.MUTED,
        ).grid(row=1, column=0, sticky="ew", pady=(6, 0))

    def show_busy(self) -> None:
        clear(self.body)
        wrap_label(
            self.body, "Mentor kodunu inceliyor…", size=16, weight="bold", color=theme.VIOLET
        ).grid(row=0, column=0, sticky="ew")
        muted_label(
            self.body,
            "Hangi adımda olduğunu yukarıdaki akıştan izleyebilirsin.",
            wraplength=360,
        ).grid(row=1, column=0, sticky="ew", pady=(6, 0))

    def show(self, result: SocraticResult | None, busy: bool = False) -> None:
        clear(self.body)
        if result is None:
            wrap_label(
                self.body, "Bu analizde mentor sorusu üretilmedi.", size=14, color=theme.MUTED
            ).grid(row=0, column=0, sticky="ew")
            return
        wrap_label(self.body, result.key_flaw_concept, size=18, weight="bold").grid(
            row=0, column=0, sticky="ew"
        )
        self._ladder(result.hint_level).grid(row=1, column=0, sticky="ew", pady=(10, 14))

        questions = ctk.CTkFrame(self.body, fg_color="transparent", width=1, height=1)
        questions.grid(row=2, column=0, sticky="ew")
        questions.grid_columnconfigure(1, weight=1)
        for i, question in enumerate(result.guiding_questions):
            ctk.CTkLabel(
                questions,
                text="?",
                width=26,
                height=26,
                corner_radius=13,
                fg_color=theme.VIOLET_DIM,
                text_color=theme.VIOLET,
                font=theme.font(13, "bold"),
            ).grid(row=i, column=0, sticky="nw", pady=(2, 10))
            wrap_label(questions, question, size=14).grid(
                row=i, column=1, sticky="ew", padx=(12, 0), pady=(2, 10)
            )

        if result.next_step_hint:
            hint = ctk.CTkFrame(self.body, fg_color=theme.SURFACE_2, corner_radius=theme.RADIUS_SM)
            hint.grid(row=3, column=0, sticky="ew", pady=(4, 0))
            hint.grid_columnconfigure(1, weight=1)
            ctk.CTkFrame(hint, width=3, height=1, corner_radius=2, fg_color=theme.GOLD).grid(
                row=0, column=0, rowspan=2, sticky="ns", padx=(10, 0), pady=10
            )
            ctk.CTkLabel(
                hint, text="SONRAKİ ADIM", font=theme.font(10, "bold"), text_color=theme.GOLD
            ).grid(row=0, column=1, sticky="w", padx=12, pady=(10, 0))
            wrap_label(hint, result.next_step_hint, size=13, color=theme.TEXT_SOFT).grid(
                row=1, column=1, sticky="ew", padx=12, pady=(2, 12)
            )

        actions = ctk.CTkFrame(self.body, fg_color="transparent", width=1, height=1)
        actions.grid(row=4, column=0, sticky="ew", pady=(16, 0))
        at_max = result.hint_level >= MAX_HINT_LEVEL
        ctk.CTkButton(
            actions,
            text="En açık ipucundasın" if at_max else "Bir ipucu daha  →",
            command=self._on_next_hint,
            state="disabled" if at_max or busy else "normal",
            height=36,
            corner_radius=18,
            font=theme.font(13, "bold"),
            fg_color=theme.VIOLET_DIM,
            hover_color="#2E2860",
            text_color=theme.VIOLET,
            text_color_disabled=theme.FAINT,
            border_width=1,
            border_color="#3B3478",
        ).pack(side="left")
        ctk.CTkButton(
            actions,
            text="Baştan başla",
            command=self._on_restart,
            height=36,
            width=110,
            fg_color="transparent",
            hover_color=theme.SURFACE_2,
            text_color=theme.MUTED,
            font=theme.font(12),
            state="disabled" if busy else "normal",
        ).pack(side="left", padx=(8, 0))

    def _ladder(self, level: int) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.body, fg_color="transparent", width=1, height=1)
        for step in range(1, MAX_HINT_LEVEL + 1):
            ctk.CTkFrame(
                frame,
                width=34,
                height=5,
                corner_radius=3,
                fg_color=theme.VIOLET if step <= level else theme.SURFACE_3,
            ).pack(side="left", padx=(0, 4))
        ctk.CTkLabel(
            frame,
            text=f"Seviye {level}/{MAX_HINT_LEVEL} · {HINT_LEVEL_LABELS[level]}",
            font=theme.font(11),
            text_color=theme.MUTED,
        ).pack(side="left", padx=(8, 0))
        return frame
