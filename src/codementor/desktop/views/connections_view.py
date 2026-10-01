"""Bağlantılar (ADR-0014): sağlayıcı kartları, derleyici durumu, veri konumları."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.connections import PROVIDERS
from codementor.desktop.views.questions_view import page_header
from codementor.desktop.widgets.common import Card, Pill, clear, muted_label
from codementor.desktop.widgets.provider_card import CardActions, ProviderCard
from codementor.models.api import CompilerStatus

_COMPILER_TARGETS = {"c": "C", "cpp": "C++", "unreal": "Unreal (C++)", "csharp": "C# (Roslyn)"}


class ConnectionsView(ctk.CTkFrame):  # type: ignore[misc]
    def __init__(
        self,
        master: Any,
        actions: CardActions,
        open_folder: Callable[[str], None],
        locations: list[tuple[str, str]],
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        page_header(
            self,
            "Bağlantılar",
            "Mentorun hangi modelle düşüneceğini seç; oturum aç ya da API anahtarını ekle.",
        ).grid(row=0, column=0, sticky="w", pady=(0, 16))

        area = ctk.CTkScrollableFrame(
            self, fg_color="transparent", scrollbar_button_color=theme.SURFACE_3
        )
        area.grid(row=1, column=0, sticky="nsew")
        area.grid_columnconfigure((0, 1), weight=1, uniform="cards")
        self.cards: dict[str, ProviderCard] = {}
        for i, info in enumerate(PROVIDERS):
            r, c = divmod(i, 2)
            card = ProviderCard(area, info, actions)
            card.grid(
                row=r,
                column=c,
                sticky="nsew",
                padx=(0, theme.GAP) if c == 0 else 0,
                pady=(0, theme.GAP),
            )
            self.cards[info.name] = card
        row = (len(PROVIDERS) + 1) // 2

        compilers = Card(area, title="Derleme denetimi (Tier 1)")
        compilers.grid(row=row, column=0, sticky="nsew", padx=(0, theme.GAP), pady=(0, theme.GAP))
        self.compiler_status = compilers.body
        muted_label(self.compiler_status, "Denetleniyor…").grid(row=0, column=0, sticky="w")

        where = Card(area, title="Konumlar")
        where.grid(row=row, column=1, sticky="nsew", pady=(0, theme.GAP))
        where.body.grid_columnconfigure(0, weight=1)
        for i, (label, path) in enumerate(locations):
            ctk.CTkLabel(
                where.body,
                text=label,
                font=theme.font(12, "bold"),
                text_color=theme.TEXT_SOFT,
                anchor="w",
            ).grid(row=2 * i, column=0, sticky="w", pady=(6 if i else 0, 0))
            ctk.CTkLabel(
                where.body,
                text=path,
                font=ctk.CTkFont(*theme.code_font(11)),
                text_color=theme.MUTED,
                anchor="w",
            ).grid(row=2 * i + 1, column=0, sticky="ew")
            ctk.CTkButton(
                where.body,
                text="Aç",
                width=54,
                height=28,
                corner_radius=8,
                fg_color=theme.SURFACE_2,
                hover_color=theme.SURFACE_3,
                text_color=theme.TEXT_SOFT,
                font=theme.font(12),
                command=lambda p=path: open_folder(p),
            ).grid(row=2 * i, column=1, rowspan=2, padx=(10, 0))

    def show_compilers(self, compilers: list[CompilerStatus]) -> None:
        clear(self.compiler_status)
        for i, compiler in enumerate(compilers):
            ctk.CTkLabel(
                self.compiler_status,
                text=_COMPILER_TARGETS.get(compiler.target, compiler.target),
                font=theme.font(13),
                text_color=theme.TEXT_SOFT,
                anchor="w",
                width=130,
            ).grid(row=i, column=0, sticky="w", pady=4)
            tool, color = (
                (compiler.tool, theme.OK) if compiler.tool else ("bulunamadı", theme.FAINT)
            )
            Pill(self.compiler_status, tool, color).grid(row=i, column=1, sticky="w")
        muted_label(
            self.compiler_status,
            "Derleyici yoksa bu adım atlanır; statik analiz ve mentorluk yine çalışır.",
            size=11,
            wraplength=360,
        ).grid(row=len(compilers), column=0, columnspan=2, sticky="ew", pady=(10, 0))
