"""Bağlantılar (ADR-0014): sağlayıcı kartları, derleyici durumu, veri konumları."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.buildinfo import build_info, describe
from codementor.desktop import theme
from codementor.desktop.connections import PROVIDERS
from codementor.desktop.views.questions_view import page_header
from codementor.desktop.widgets.common import Card, Pill, clear, muted_label
from codementor.desktop.widgets.provider_card import CardActions, ProviderCard
from codementor.models.api import CompilerStatus

_COMPILER_TARGETS = {
    "c": "C",
    "cpp": "C++",
    "unreal": "Unreal (C++)",
    "csharp": "C# (Roslyn)",
    "python": "Python",
}
_ORIGINS = {"downloaded": "indirilen", "bundled": "gömülü"}  # PATH'teki araçta ek yok


def _tool_label(compiler: CompilerStatus) -> str:
    suffix = _ORIGINS.get(compiler.origin or "", "")
    return f"{compiler.tool} ({suffix})" if suffix else str(compiler.tool)


class ConnectionsView(ctk.CTkFrame):  # type: ignore[misc]
    def __init__(
        self,
        master: Any,
        actions: CardActions,
        open_folder: Callable[[str], None],
        locations: list[tuple[str, str]],
        write_config: Callable[[], None] | None = None,
        reload_config: Callable[[], None] | None = None,
        download: Callable[[], None] | None = None,
        cancel_download: Callable[[], None] | None = None,
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
        compilers.body.grid_columnconfigure(0, weight=1)
        self.compiler_status = ctk.CTkFrame(compilers.body, fg_color="transparent")
        self.compiler_status.grid(row=0, column=0, sticky="ew")
        muted_label(self.compiler_status, "Denetleniyor…").grid(row=0, column=0, sticky="w")
        self._build_download(compilers.body, download, cancel_download)

        where = Card(area, title="Konumlar")
        where.grid(row=row, column=1, sticky="nsew", pady=(0, theme.GAP))
        where.body.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            where.body,
            text=f"Sürüm: {describe(build_info())}",
            font=theme.font(11),
            text_color=theme.MUTED,
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        for i, (label, path) in enumerate(locations):
            r = 1 + 2 * i
            ctk.CTkLabel(
                where.body,
                text=label,
                font=theme.font(12, "bold"),
                text_color=theme.TEXT_SOFT,
                anchor="w",
            ).grid(row=r, column=0, sticky="w", pady=(6 if i else 0, 0))
            ctk.CTkLabel(
                where.body,
                text=path,
                font=ctk.CTkFont(*theme.code_font(11)),
                text_color=theme.MUTED,
                anchor="w",
            ).grid(row=r + 1, column=0, sticky="ew")
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
            ).grid(row=r, column=1, rowspan=2, padx=(10, 0))
        btn_row = 1 + 2 * len(locations)
        if write_config is not None:  # Faz 24: CLI/API de aynı modeli kullansın
            self.write_config_button = ctk.CTkButton(
                where.body,
                text="Seçimleri codementor.toml'a yaz",
                height=32,
                corner_radius=8,
                fg_color=theme.SURFACE_2,
                hover_color=theme.SURFACE_3,
                text_color=theme.TEXT,
                font=theme.font(12, "bold"),
                command=write_config,
            )
            self.write_config_button.grid(
                row=btn_row, column=0, columnspan=2, sticky="w", pady=(14, 0)
            )
            btn_row += 1
        if reload_config is not None:  # Faz 33: elle düzenlenen toml'u yeniden başlatmadan uygula
            self.reload_config_button = ctk.CTkButton(
                where.body,
                text="codementor.toml'dan yeniden yükle",
                height=32,
                corner_radius=8,
                fg_color=theme.SURFACE_2,
                hover_color=theme.SURFACE_3,
                text_color=theme.TEXT,
                font=theme.font(12, "bold"),
                command=reload_config,
            )
            self.reload_config_button.grid(
                row=btn_row, column=0, columnspan=2, sticky="w", pady=(8, 0)
            )

    def _build_download(
        self,
        master: Any,
        download: Callable[[], None] | None,
        cancel_download: Callable[[], None] | None,
    ) -> None:
        """Faz 29: derleyicisi olmayan için zig indirme düğmesi, ilerleme ve iptal."""
        box = ctk.CTkFrame(master, fg_color="transparent")
        box.grid_columnconfigure(0, weight=1)
        self.download_box = box
        self.download_button = ctk.CTkButton(
            box,
            text="Derleyiciyi indir (~100 MB)",
            height=32,
            corner_radius=8,
            fg_color=theme.GOLD,
            hover_color=theme.GOLD_HOVER,
            text_color=theme.GOLD_INK,
            font=theme.font(12, "bold"),
            command=download or (lambda: None),
        )
        self.download_button.grid(row=0, column=0, sticky="w")
        self.download_cancel = ctk.CTkButton(
            box,
            text="İptal",
            width=64,
            height=32,
            corner_radius=8,
            fg_color=theme.STOP,
            hover_color=theme.STOP_HOVER,
            text_color=theme.TEXT,
            font=theme.font(12),
            command=cancel_download or (lambda: None),
        )
        self.download_bar = ctk.CTkProgressBar(
            box, height=6, corner_radius=3, fg_color=theme.SURFACE_3, progress_color=theme.GOLD
        )
        self.download_text = muted_label(
            box,
            "C/C++/Unreal derleme denetimi için zig indirilir (bir kez, kullanıcı dizinine).",
            size=11,
            wraplength=360,
        )
        self.download_text.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.downloading = False

    def set_download_running(self, text: str, fraction: float | None) -> None:
        """İndirme sürüyor: düğme gizli, çubuk + İptal görünür."""
        self.downloading = True
        self.download_box.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        self.download_button.grid_remove()
        self.download_cancel.grid(row=0, column=1, sticky="e", padx=(10, 0))
        self.download_bar.grid(row=0, column=0, sticky="ew")
        if fraction is None:
            if self.download_bar.cget("mode") != "indeterminate":
                self.download_bar.configure(mode="indeterminate")
                self.download_bar.start()
        else:
            if self.download_bar.cget("mode") != "determinate":
                self.download_bar.stop()
                self.download_bar.configure(mode="determinate")
            self.download_bar.set(fraction)
        self.download_text.configure(text=text, text_color=theme.MUTED)

    def set_download_cancelling(self) -> None:
        """İptal istendi; işçi yarım dosyaları silip bitene kadar bekleniyor."""
        self.download_cancel.configure(state="disabled")
        self.download_text.configure(text="İptal ediliyor…", text_color=theme.MUTED)

    def set_download_idle(self, text: str, *, ok: bool, offer: bool) -> None:
        """İndirme bitti/iptal/hata: mesaj gösterilir; `offer` ise düğme yeniden görünür."""
        self.downloading = False
        self.download_bar.stop()
        self.download_bar.grid_remove()
        self.download_cancel.grid_remove()
        self.download_cancel.configure(state="normal")
        if offer:
            self.download_button.grid(row=0, column=0, sticky="w")
        else:
            self.download_button.grid_remove()
        self.download_text.configure(text=text, text_color=theme.TEXT_SOFT if ok else theme.ERROR)
        self.download_box.grid(row=1, column=0, sticky="ew", pady=(12, 0))

    def show_compilers(
        self, compilers: list[CompilerStatus], *, offer_download: bool = False
    ) -> None:
        if not self.downloading:
            if offer_download:
                self.download_button.grid(row=0, column=0, sticky="w")
                self.download_box.grid(row=1, column=0, sticky="ew", pady=(12, 0))
            else:
                self.download_box.grid_remove()
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
                (_tool_label(compiler), theme.OK) if compiler.tool else ("bulunamadı", theme.FAINT)
            )
            Pill(self.compiler_status, tool, color).grid(row=i, column=1, sticky="w")
        muted_label(
            self.compiler_status,
            "Derleyici yoksa bu adım atlanır; statik analiz ve mentorluk yine çalışır.",
            size=11,
            wraplength=360,
        ).grid(row=len(compilers), column=0, columnspan=2, sticky="ew", pady=(10, 0))
