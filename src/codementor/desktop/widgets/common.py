"""Ortak yapı taşları: kart, başlık, rozet."""

from __future__ import annotations

import tkinter as tk
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme


class Card(ctk.CTkFrame):  # type: ignore[misc]
    """Yuvarlatılmış, ince kenarlıklı yüzey; isteğe bağlı vurgu çizgili başlık."""

    def __init__(
        self,
        master: Any,
        title: str | None = None,
        accent: str = theme.GOLD,
        subtitle: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            master,
            fg_color=theme.SURFACE,
            corner_radius=theme.RADIUS,
            border_width=1,
            border_color=theme.BORDER,
            **kwargs,
        )
        self.grid_columnconfigure(0, weight=1)
        self.body = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        row = 0
        if title:
            header = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
            header.grid(row=0, column=0, sticky="ew", padx=theme.PAD, pady=(16, 0))
            header.grid_columnconfigure(1, weight=1)
            ctk.CTkFrame(header, width=3, height=16, corner_radius=2, fg_color=accent).grid(
                row=0, column=0, padx=(0, 10)
            )
            ctk.CTkLabel(
                header, text=title.upper(), font=theme.font(11, "bold"), text_color=theme.MUTED
            ).grid(row=0, column=1, sticky="w")
            self.header_right = ctk.CTkFrame(header, fg_color="transparent", width=1, height=1)
            self.header_right.grid(row=0, column=2, sticky="e")
            if subtitle:
                ctk.CTkLabel(
                    header, text=subtitle, font=theme.font(11), text_color=theme.FAINT
                ).grid(row=0, column=3, sticky="e")
            row = 1
        self.body.grid(
            row=row, column=0, sticky="nsew", padx=theme.PAD, pady=(10, 18) if title else 14
        )
        self.body.grid_columnconfigure(0, weight=1)


class Pill(ctk.CTkLabel):  # type: ignore[misc]
    """Küçük, yuvarlak rozet (önem, durum, zorluk)."""

    def __init__(self, master: Any, text: str, color: str = theme.MUTED, **kwargs: Any) -> None:
        super().__init__(
            master,
            text=f" {text} ",
            font=theme.font(11, "bold"),
            text_color=color,
            fg_color=theme.SURFACE_3,
            corner_radius=10,
            height=22,
            **kwargs,
        )

    def set(self, text: str, color: str) -> None:
        self.configure(text=f" {text} ", text_color=color)


def clear(frame: Any) -> None:
    """Bir çerçevenin tüm çocuklarını kaldırır."""
    for child in frame.winfo_children():
        child.destroy()


def muted_label(master: Any, text: str, size: int = 12, **kwargs: Any) -> ctk.CTkLabel:
    kwargs.setdefault("text_color", theme.MUTED)
    return ctk.CTkLabel(
        master, text=text, font=theme.font(size), justify="left", anchor="w", **kwargs
    )


def wrap_label(
    master: Any, text: str, size: int = 13, color: str = theme.TEXT, **kwargs: Any
) -> ctk.CTkLabel:
    """Kart genişliğine göre satır kaydıran metin (genişlik değişince yeniden kaydırır)."""
    label = ctk.CTkLabel(
        master,
        text=text,
        font=theme.font(size, kwargs.pop("weight", "normal")),
        text_color=color,
        justify="left",
        anchor="w",
        wraplength=380,
        **kwargs,
    )

    def rewrap(event: Any) -> None:
        # olay piksel verir, wraplength ölçeklenmemiş birim bekler (yüksek DPI)
        scaling = ctk.ScalingTracker.get_widget_scaling(label)
        width = max(int(event.width / scaling) - 8, 120)
        if abs(int(label.cget("wraplength")) - width) > 4:
            label.configure(wraplength=width)

    # CTkLabel.bind iç etikete bağlar; dış çerçevenin genişliği grid'den gelir
    tk.Frame.bind(label, "<Configure>", rewrap, "+")
    return label
