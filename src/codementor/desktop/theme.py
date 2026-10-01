"""Tasarım tokenları: renkler, yazı tipleri, boşluklar. Arayüzdeki tüm görsel kararlar buradan.

Dil: derin lacivert-grafit zemin, ince kenarlıklar, tek vurgu rengi altın; ikincil vurgu mor
(Sokratik mentor). Önem renkleri yumuşak tonlu; hiçbir yerde saf beyaz/siyah yok.
"""

from __future__ import annotations

import sys
import tkinter as tk
import tkinter.font as tkfont
from functools import cache

import customtkinter as ctk

from codementor.models.enums import Severity

# --- Renkler ---
BG = "#0A0E16"
SIDEBAR = "#0D121C"
SURFACE = "#111826"
SURFACE_2 = "#172034"
SURFACE_3 = "#1E2A42"
BORDER = "#222E46"
BORDER_STRONG = "#2E3D5C"
TEXT = "#E8ECF4"
TEXT_SOFT = "#B9C1D3"
MUTED = "#8691A8"
FAINT = "#56607A"

GOLD = "#E8B04B"
GOLD_HOVER = "#F3C66E"
GOLD_DIM = "#3A2F17"
GOLD_INK = "#1A1306"
VIOLET = "#9A8CFF"
VIOLET_DIM = "#231F45"

OK = "#4ADE80"
WARN = "#FBBF24"
ERROR = "#F87171"
INFO = "#60A5FA"

SEVERITY_COLORS: dict[Severity, str] = {
    Severity.HIGH: ERROR,
    Severity.MEDIUM: WARN,
    Severity.LOW: INFO,
}
# Editörde işaretli satırın zemini (önem renginin koyu tonu)
LINE_BACKGROUNDS: dict[Severity, str] = {
    Severity.HIGH: "#2C161C",
    Severity.MEDIUM: "#2B2414",
    Severity.LOW: "#13213A",
}
SYNTAX: dict[str, str] = {
    "comment": "#5F6B85",
    "string": "#A5D6A7",
    "preproc": "#C792EA",
    "keyword": "#F3C66E",
    "type": "#82AAFF",
    "number": "#F78C6C",
    "function": "#89DDFF",
}

# --- Ölçüler ---
RADIUS = 14
RADIUS_SM = 9
PAD = 20
GAP = 12

_UI_CANDIDATES = ("Segoe UI Variable Display", "Segoe UI", "Inter", "Helvetica Neue", "Arial")
_CODE_CANDIDATES = ("Cascadia Code", "Cascadia Mono", "JetBrains Mono", "Consolas", "Menlo")


@cache
def _family(candidates: tuple[str, ...]) -> str:
    available = set(tkfont.families())
    return next((name for name in candidates if name in available), candidates[-1])


def ui_family() -> str:
    """Kullanılabilir ilk arayüz yazı tipi (Tk kökü oluşturulduktan sonra çağrılmalı)."""
    return _family(_UI_CANDIDATES)


def code_family() -> str:
    return _family(_CODE_CANDIDATES)


def font(size: int = 13, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=ui_family(), size=size, weight=weight)


def code_font(size: int = 13) -> tuple[str, int]:
    """tk.Text için (aile, boyut) çifti."""
    return (code_family(), size)


def apply_window_chrome(window: tk.Misc) -> None:
    """Windows 11: koyu başlık çubuğu ve başlık rengini zeminle eşler (diğer sistemlerde yok)."""
    if sys.platform != "win32":
        return
    try:
        import ctypes

        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        dark = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(dark), 4)
        # COLORREF 0x00BBGGRR
        r, g, b = (int(BG[i : i + 2], 16) for i in (1, 3, 5))
        caption = ctypes.c_int(b << 16 | g << 8 | r)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(caption), 4)
    except (AttributeError, OSError):
        pass
