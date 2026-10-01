"""Bağlantılar ekranındaki sağlayıcı kartı: durum, model, yetkilendirme, eylemler."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.connections import KeySource, Probe, ProviderInfo
from codementor.desktop.widgets.common import Pill, wrap_label

Action = Callable[[str], None]
ValueAction = Callable[[str, str], None]

_KEY_TEXT: dict[KeySource, tuple[str, str]] = {
    "vault": ("Anahtar Windows kimlik kasasında kayıtlı", theme.OK),
    "environment": ("Anahtar ortam değişkeninden geliyor", theme.OK),
    "missing": ("Anahtar yok", theme.MUTED),
}


@dataclass
class CardActions:
    make_default: Action
    check: Action
    login: Action
    try_connection: Action
    delete_key: Action
    set_model: ValueAction
    set_base_url: ValueAction
    save_key: ValueAction
    allow_tool_agent: Callable[[str, bool], None]


def _button(master: Any, text: str, command: Callable[[], None], primary: bool = False) -> Any:
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        height=32,
        corner_radius=9,
        width=40,
        font=theme.font(12, "bold" if primary else "normal"),
        fg_color=theme.GOLD if primary else theme.SURFACE_2,
        hover_color=theme.GOLD_HOVER if primary else theme.SURFACE_3,
        text_color=theme.GOLD_INK if primary else theme.TEXT_SOFT,
        border_width=0 if primary else 1,
        border_color=theme.BORDER,
    )


def _entry(master: Any, placeholder: str, secret: bool = False) -> Any:
    return ctk.CTkEntry(
        master,
        placeholder_text=placeholder,
        show="•" if secret else "",
        height=34,
        corner_radius=9,
        font=theme.font(13),
        fg_color=theme.SURFACE_2,
        border_color=theme.BORDER,
        text_color=theme.TEXT,
        placeholder_text_color=theme.FAINT,
    )


class ProviderCard(ctk.CTkFrame):  # type: ignore[misc]
    """Tek sağlayıcı. Durum `set_probe(None)` ile "denetleniyor"a döner."""

    def __init__(self, master: Any, info: ProviderInfo, actions: CardActions) -> None:
        super().__init__(
            master,
            fg_color=theme.SURFACE,
            corner_radius=theme.RADIUS,
            border_width=1,
            border_color=theme.BORDER,
        )
        self.info = info
        self.actions = actions
        self.grid_columnconfigure(0, weight=1)
        name = info.name

        head = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        head.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 0))
        head.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            head, text=info.label, font=theme.font(16, "bold"), text_color=theme.TEXT
        ).grid(row=0, column=0, sticky="w")
        self.default_pill = Pill(head, "VARSAYILAN", theme.GOLD)
        self.status_pill = Pill(head, "denetleniyor", theme.FAINT)
        self.status_pill.grid(row=0, column=2, sticky="e")
        ctk.CTkLabel(
            head, text=info.blurb, font=theme.font(12), text_color=theme.MUTED, anchor="w"
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(2, 0))

        body = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        body.grid(row=1, column=0, sticky="ew", padx=18, pady=(12, 0))
        body.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            body,
            text="Model",
            font=theme.font(12),
            text_color=theme.TEXT_SOFT,
            width=64,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")
        self.model = ctk.CTkComboBox(
            body,
            values=[""],
            height=34,
            corner_radius=9,
            font=theme.font(13),
            dropdown_font=theme.font(13),
            fg_color=theme.SURFACE_2,
            border_color=theme.BORDER,
            button_color=theme.SURFACE_3,
            button_hover_color=theme.BORDER_STRONG,
            dropdown_fg_color=theme.SURFACE_2,
            dropdown_hover_color=theme.SURFACE_3,
            text_color=theme.TEXT,
            dropdown_text_color=theme.TEXT,
            command=lambda value: actions.set_model(name, value),
        )
        self.model.grid(row=0, column=1, sticky="ew")
        self.model.bind("<Return>", lambda _e: actions.set_model(name, self.model.get()))
        self.model.bind("<FocusOut>", lambda _e: self._commit_model())
        self._model_value = ""

        self.auth = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        self.auth.grid(row=2, column=0, sticky="ew", padx=18, pady=(10, 0))
        self.auth.grid_columnconfigure(0, weight=1)
        self.key_entry: Any = None
        self.url_entry: Any = None
        self.tool_switch: Any = None
        self.key_label: Any = None
        self._build_auth()

        self.detail = wrap_label(self, "", size=12, color=theme.MUTED)
        self.detail.grid(row=3, column=0, sticky="ew", padx=18, pady=(10, 0))

        bar = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        bar.grid(row=4, column=0, sticky="ew", padx=18, pady=(12, 16))
        self.default_button = _button(
            bar, "Varsayılan yap", lambda: actions.make_default(name), primary=True
        )
        self.default_button.pack(side="left", padx=(0, 6))
        _button(bar, "Denetle", lambda: actions.check(name)).pack(side="left", padx=(0, 6))
        if info.kind == "cli":
            _button(bar, "Oturum aç", lambda: actions.login(name)).pack(side="left", padx=(0, 6))
        if info.kind in ("api", "local"):
            _button(bar, "Bağlantıyı dene", lambda: actions.try_connection(name)).pack(side="left")

    def _build_auth(self) -> None:
        name, actions = self.info.name, self.actions
        if self.info.kind == "api":
            self.key_entry = _entry(self.auth, "API anahtarını yapıştır", secret=True)
            self.key_entry.grid(row=0, column=0, sticky="ew")
            _button(self.auth, "Kaydet", self._save_key).grid(row=0, column=1, padx=(6, 0))
            _button(self.auth, "Sil", lambda: actions.delete_key(name)).grid(
                row=0, column=2, padx=(6, 0)
            )
            self.key_label = ctk.CTkLabel(
                self.auth, text="", font=theme.font(11), text_color=theme.MUTED, anchor="w"
            )
            self.key_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(4, 0))
        elif self.info.kind == "local":
            self.url_entry = _entry(self.auth, "http://127.0.0.1:11434")
            self.url_entry.grid(row=0, column=0, sticky="ew")
            _button(
                self.auth,
                "Adresi kaydet",
                lambda: actions.set_base_url(name, self.url_entry.get().strip()),
            ).grid(row=0, column=1, padx=(6, 0))
        elif name == "agy":
            self.tool_switch = ctk.CTkSwitch(
                self.auth,
                text="Kodu araç kullanabilen ajana vermeyi kabul ediyorum (ADR-0012)",
                font=theme.font(12),
                text_color=theme.TEXT_SOFT,
                progress_color=theme.GOLD,
                button_color=theme.TEXT_SOFT,
                fg_color=theme.SURFACE_3,
                command=lambda: actions.allow_tool_agent(name, bool(self.tool_switch.get())),
            )
            self.tool_switch.grid(row=0, column=0, sticky="w")

    def _save_key(self) -> None:
        key = self.key_entry.get().strip()
        if key:
            self.actions.save_key(self.info.name, key)
        self.key_entry.delete(0, "end")

    def _commit_model(self) -> None:
        value = self.model.get().strip()
        if value and value != self._model_value:
            self.actions.set_model(self.info.name, value)

    # --- Güncelleme ---------------------------------------------------------------------

    def set_default(self, default: bool) -> None:
        if default:
            self.default_pill.grid(row=0, column=1, sticky="e", padx=(0, 6))
            self.default_button.configure(state="disabled", text="Varsayılan")
        else:
            self.default_pill.grid_forget()
            self.default_button.configure(state="normal", text="Varsayılan yap")

    def set_model(self, model: str, choices: list[str]) -> None:
        self._model_value = model
        values = list(dict.fromkeys([*([model] if model else []), *choices])) or [""]
        self.model.configure(values=values)
        self.model.set(model)

    def set_base_url(self, url: str | None) -> None:
        if self.url_entry is not None:
            self.url_entry.delete(0, "end")
            if url:
                self.url_entry.insert(0, url)

    def set_tool_agent(self, allowed: bool) -> None:
        if self.tool_switch is not None:
            (self.tool_switch.select if allowed else self.tool_switch.deselect)()

    def set_key_source(self, source: KeySource, env: str | None) -> None:
        if self.key_label is None:
            return
        text, color = _KEY_TEXT[source]
        if source == "environment" and env:
            text += f" ({env})"
        self.key_label.configure(text=text, text_color=color)

    def set_probe(self, probe: Probe | None) -> None:
        if probe is None:
            self.status_pill.set("denetleniyor", theme.FAINT)
            self.detail.configure(text="", text_color=theme.MUTED)
            self.configure(border_color=theme.BORDER)
            return
        ready = probe.ready
        self.status_pill.set(
            "hazır" if ready else "hazır değil", theme.OK if ready else theme.ERROR
        )
        self.detail.configure(text=probe.status.detail, text_color=theme.MUTED)

    def set_message(self, text: str, ok: bool) -> None:
        self.detail.configure(text=text, text_color=theme.OK if ok else theme.ERROR)
