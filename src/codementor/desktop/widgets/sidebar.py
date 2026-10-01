"""Sol menü: logo, gezinme, alt kısımda sağlayıcı durumu."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import customtkinter as ctk
from PIL import Image

from codementor import __version__
from codementor.desktop import theme

NAV_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("analyze", "◆", "Analiz"),
    ("questions", "❖", "Soru bankası"),
    ("history", "◷", "Geçmiş"),
    ("settings", "⚙", "Bağlantılar"),
)


class Sidebar(ctk.CTkFrame):  # type: ignore[misc]
    def __init__(self, master: Any, logo: Path | None, on_navigate: Callable[[str], None]) -> None:
        super().__init__(master, width=232, corner_radius=0, fg_color=theme.SIDEBAR)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._on_navigate = on_navigate

        brand = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        brand.grid(row=0, column=0, sticky="ew", padx=22, pady=(26, 30))
        if logo is not None and logo.is_file():
            image = ctk.CTkImage(Image.open(logo), size=(38, 38))
            ctk.CTkLabel(brand, image=image, text="").pack(side="left")
        names = ctk.CTkFrame(brand, fg_color="transparent", width=1, height=1)
        names.pack(side="left", padx=(12, 0))
        title = ctk.CTkFrame(names, fg_color="transparent", width=1, height=1)
        title.pack(anchor="w")
        ctk.CTkLabel(
            title, text="CodeMentor", font=theme.font(18, "bold"), text_color=theme.TEXT
        ).pack(side="left")
        ctk.CTkLabel(title, text=" AI", font=theme.font(18, "bold"), text_color=theme.GOLD).pack(
            side="left"
        )
        ctk.CTkLabel(
            names,
            text="Kodu düzeltmez, düşündürür.",
            font=theme.font(11),
            text_color=theme.MUTED,
            height=16,
        ).pack(anchor="w")

        nav = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        nav.grid(row=1, column=0, sticky="ew", padx=14)
        nav.grid_columnconfigure(0, weight=1)
        self._buttons: dict[str, tuple[ctk.CTkFrame, ctk.CTkButton]] = {}
        for i, (key, icon, label) in enumerate(NAV_ITEMS):
            row = ctk.CTkFrame(nav, fg_color="transparent", width=1, height=1)
            row.grid(row=i, column=0, sticky="ew", pady=2)
            row.grid_columnconfigure(1, weight=1)
            indicator = ctk.CTkFrame(
                row, width=3, height=22, corner_radius=2, fg_color="transparent"
            )
            indicator.grid(row=0, column=0, padx=(0, 6))
            button = ctk.CTkButton(
                row,
                text=f"{icon}   {label}",
                anchor="w",
                height=42,
                corner_radius=10,
                font=theme.font(14),
                fg_color="transparent",
                hover_color=theme.SURFACE,
                text_color=theme.TEXT_SOFT,
                command=lambda k=key: self._on_navigate(k),
            )
            button.grid(row=0, column=1, sticky="ew")
            self._buttons[key] = (indicator, button)

        footer = self.status_box = ctk.CTkFrame(
            self,
            fg_color=theme.SURFACE,
            corner_radius=theme.RADIUS_SM,
            border_width=1,
            border_color=theme.BORDER,
        )
        footer.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 18))
        footer.grid_columnconfigure(1, weight=1)
        self.status_dot = ctk.CTkLabel(
            footer, text="●", text_color=theme.FAINT, font=theme.font(12), width=14
        )
        self.status_dot.grid(row=0, column=0, padx=(12, 6), pady=(10, 0))
        self.status_text = ctk.CTkLabel(
            footer,
            text="Sağlayıcı denetleniyor…",
            anchor="w",
            font=theme.font(12, "bold"),
            text_color=theme.TEXT_SOFT,
        )
        self.status_text.grid(row=0, column=1, sticky="ew", pady=(10, 0), padx=(0, 10))
        self.status_detail = ctk.CTkLabel(
            footer, text="", anchor="w", font=theme.font(11), text_color=theme.MUTED, height=16
        )
        self.status_detail.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        ctk.CTkLabel(
            footer, text=f"v{__version__}", font=theme.font(10), text_color=theme.FAINT, height=14
        ).grid(row=2, column=1, sticky="w", pady=(0, 10))

    def on_status_click(self, callback: Callable[[], None]) -> None:
        """Sağlayıcı kutusuna tıklanınca (Bağlantılar ekranına git)."""
        self.status_box.configure(cursor="hand2")
        for widget in (self.status_box, *self.status_box.winfo_children()):
            widget.bind("<Button-1>", lambda _e: callback(), add="+")

    def select(self, key: str) -> None:
        for name, (indicator, button) in self._buttons.items():
            active = name == key
            indicator.configure(fg_color=theme.GOLD if active else "transparent")
            button.configure(
                fg_color=theme.SURFACE_2 if active else "transparent",
                text_color=theme.TEXT if active else theme.TEXT_SOFT,
                font=theme.font(14, "bold" if active else "normal"),
            )

    def set_provider(self, name: str, ready: bool | None, detail: str = "") -> None:
        """`ready=None`: denetim sürüyor."""
        color = theme.FAINT if ready is None else theme.OK if ready else theme.ERROR
        self.status_dot.configure(text_color=color)
        self.status_text.configure(text=name)
        self.status_detail.configure(
            text=detail
            or ("denetleniyor…" if ready is None else "hazır" if ready else "hazır değil")
        )
