"""Ayarlar: sağlayıcı seçimi ve denetimi, derleyici durumu, veri konumları."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.views.questions_view import page_header
from codementor.desktop.widgets.common import Card, Pill, clear, muted_label
from codementor.models.api import CompilerStatus
from codementor.models.provider import ProviderStatus

DEFAULT_LABEL = "Varsayılan ({name})"
_COMPILER_TARGETS = {"c": "C", "cpp": "C++", "unreal": "Unreal (C++)", "csharp": "C# (Roslyn)"}


@dataclass
class SettingsActions:
    providers: tuple[str, ...]
    default_provider: str
    choose_provider: Callable[[str | None], None]
    check: Callable[[], None]
    open_folder: Callable[[str], None]


class SettingsView(ctk.CTkFrame):  # type: ignore[misc]
    def __init__(
        self,
        master: Any,
        actions: SettingsActions,
        current: str | None,
        locations: list[tuple[str, str]],
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self.actions = actions
        self.grid_columnconfigure((0, 1), weight=1, uniform="settings")
        page_header(self, "Ayarlar", "Mentorun hangi modelle düşüneceğini ve ortamı yönet.").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
        )

        provider = Card(self, title="LLM sağlayıcı")
        provider.grid(row=1, column=0, sticky="nsew", padx=(0, theme.GAP), pady=(0, theme.GAP))
        default = DEFAULT_LABEL.format(name=actions.default_provider)
        self._default_label = default
        self.picker = ctk.CTkOptionMenu(
            provider.body,
            values=[default, *actions.providers],
            command=self._on_pick,
            height=36,
            corner_radius=10,
            font=theme.font(13),
            fg_color=theme.SURFACE_2,
            button_color=theme.SURFACE_2,
            button_hover_color=theme.SURFACE_3,
            dropdown_fg_color=theme.SURFACE_2,
            dropdown_hover_color=theme.SURFACE_3,
            text_color=theme.TEXT,
            dropdown_text_color=theme.TEXT,
            dynamic_resizing=False,
        )
        self.picker.set(current or default)
        self.picker.grid(row=0, column=0, sticky="ew")
        muted_label(
            provider.body,
            "Bulut sağlayıcıların anahtarı ortam değişkeninden okunur; uygulama anahtarı saklamaz.",
            wraplength=380,
        ).grid(row=1, column=0, sticky="ew", pady=(8, 12))
        ctk.CTkButton(
            provider.body,
            text="Bağlantıyı denetle",
            command=actions.check,
            height=36,
            corner_radius=10,
            font=theme.font(13, "bold"),
            fg_color=theme.GOLD,
            hover_color=theme.GOLD_HOVER,
            text_color=theme.GOLD_INK,
        ).grid(row=2, column=0, sticky="w")
        self.provider_status = ctk.CTkFrame(
            provider.body, fg_color="transparent", width=1, height=1
        )
        self.provider_status.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        self.provider_status.grid_columnconfigure(1, weight=1)

        compilers = Card(self, title="Derleme denetimi (Tier 1)")
        compilers.grid(row=1, column=1, sticky="nsew", pady=(0, theme.GAP))
        self.compiler_status = compilers.body
        muted_label(self.compiler_status, "Denetleniyor…").grid(row=0, column=0, sticky="w")

        where = Card(self, title="Konumlar")
        where.grid(row=2, column=0, columnspan=2, sticky="ew")
        where.body.grid_columnconfigure(0, weight=0)
        where.body.grid_columnconfigure(1, weight=1)
        for i, (label, path) in enumerate(locations):
            ctk.CTkLabel(
                where.body,
                text=label,
                font=theme.font(12, "bold"),
                text_color=theme.TEXT_SOFT,
                width=150,
                anchor="w",
            ).grid(row=i, column=0, sticky="w", pady=4)
            ctk.CTkLabel(
                where.body,
                text=path,
                font=ctk.CTkFont(*theme.code_font(11)),
                text_color=theme.MUTED,
                anchor="w",
            ).grid(row=i, column=1, sticky="ew")
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
                command=lambda p=path: actions.open_folder(p),
            ).grid(row=i, column=2, padx=(10, 0))

    def _on_pick(self, value: str) -> None:
        self.actions.choose_provider(None if value == self._default_label else value)

    def show_providers(
        self, statuses: list[ProviderStatus] | None, error: str | None = None
    ) -> None:
        """`None`: denetim sürüyor."""
        clear(self.provider_status)
        if error:
            muted_label(self.provider_status, error, text_color=theme.ERROR).grid(
                row=0, column=0, columnspan=3, sticky="w"
            )
            return
        if statuses is None:
            muted_label(self.provider_status, "Denetleniyor…").grid(row=0, column=0, sticky="w")
            return
        for i, status in enumerate(statuses):
            color = theme.OK if status.ready else theme.ERROR
            Pill(self.provider_status, "hazır" if status.ready else "hazır değil", color).grid(
                row=2 * i, column=0, sticky="w", pady=(4, 0)
            )
            ctk.CTkLabel(
                self.provider_status,
                text=f"{status.name}  ·  {status.model or '—'}",
                font=theme.font(13, "bold"),
                text_color=theme.TEXT,
            ).grid(row=2 * i, column=1, sticky="w", padx=10, pady=(4, 0))
            muted_label(self.provider_status, status.detail, size=11, wraplength=360).grid(
                row=2 * i + 1, column=1, sticky="ew", padx=10
            )

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
            if compiler.tool:
                Pill(self.compiler_status, compiler.tool, theme.OK).grid(
                    row=i, column=1, sticky="w"
                )
            else:
                Pill(self.compiler_status, "bulunamadı", theme.FAINT).grid(
                    row=i, column=1, sticky="w"
                )
        muted_label(
            self.compiler_status,
            "Derleyici yoksa bu adım atlanır; statik analiz ve mentorluk yine çalışır.",
            size=11,
            wraplength=360,
        ).grid(row=len(compilers), column=0, columnspan=2, sticky="ew", pady=(10, 0))
