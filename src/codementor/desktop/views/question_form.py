"""Kendi sorunu ekle/düzenle penceresi (Faz K, ADR-0028).

Alan değerleri metin olarak `on_submit`'e gider; doğrulama `questions_controller.draft_from_form`
ile yapılır. `on_submit` hata metni dönerse pencere açık kalır ve metni gösterir.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import (
    DIFFICULTY_LABELS,
    ENGINE_LABELS,
    LANGUAGE_LABELS,
    engines_for,
)
from codementor.models.enums import Difficulty, Engine, Language, has_complexity
from codementor.models.questions import UserQuestionDraft

FormValues = dict[str, str]
HINT_FIELDS = ("hint1", "hint2", "hint3")


def _label(master: Any, text: str) -> ctk.CTkLabel:
    return ctk.CTkLabel(
        master, text=text, font=theme.font(12, "bold"), text_color=theme.TEXT_SOFT, anchor="w"
    )


def _entry(master: Any, placeholder: str = "") -> ctk.CTkEntry:
    return ctk.CTkEntry(
        master,
        placeholder_text=placeholder,
        height=34,
        corner_radius=9,
        font=theme.font(13),
        fg_color=theme.SURFACE_2,
        border_color=theme.BORDER,
        text_color=theme.TEXT,
        placeholder_text_color=theme.FAINT,
    )


def _textbox(master: Any, height: int) -> ctk.CTkTextbox:
    return ctk.CTkTextbox(
        master,
        height=height,
        corner_radius=9,
        font=theme.font(13),
        fg_color=theme.SURFACE_2,
        border_color=theme.BORDER,
        border_width=1,
        text_color=theme.TEXT,
        wrap="word",
    )


def _menu(master: Any, values: list[str], command: Callable[[str], None] | None = None) -> Any:
    return ctk.CTkOptionMenu(
        master,
        values=values,
        command=command,
        height=34,
        corner_radius=9,
        font=theme.font(13),
        dropdown_font=theme.font(13),
        fg_color=theme.SURFACE_2,
        button_color=theme.SURFACE_2,
        button_hover_color=theme.SURFACE_3,
        text_color=theme.TEXT,
        dropdown_fg_color=theme.SURFACE_2,
        dropdown_hover_color=theme.SURFACE_3,
        dropdown_text_color=theme.TEXT,
        dynamic_resizing=False,
    )


def draft_values(draft: UserQuestionDraft) -> FormValues:
    """Düzenleme için taslaktan form değerleri."""
    hints = [*draft.hints, "", "", ""][:3]
    return {
        "title": draft.title,
        "prompt": draft.prompt,
        "language": LANGUAGE_LABELS[draft.language],
        "engine": ENGINE_LABELS[draft.engine],
        "difficulty": DIFFICULTY_LABELS[draft.difficulty],
        "constraints": "\n".join(draft.constraints),
        "expected_time": draft.expected_time or "",
        "expected_space": draft.expected_space or "",
        "concept_tags": ", ".join(draft.concept_tags),
        **dict(zip(HINT_FIELDS, hints, strict=True)),
    }


class QuestionForm(ctk.CTkToplevel):  # type: ignore[misc]
    """Soru formu; kaydet → `on_submit(values)`; hata metni dönerse gösterilir."""

    def __init__(
        self,
        master: Any,
        on_submit: Callable[[FormValues], str | None],
        initial: FormValues | None = None,
    ) -> None:
        super().__init__(master, fg_color=theme.BG)
        self.title("Soruyu düzenle" if initial else "Kendi sorunu ekle")
        self.geometry("620x760")
        self.minsize(520, 560)
        self._on_submit = on_submit
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        body.grid(row=0, column=0, sticky="nsew", padx=theme.PAD, pady=(theme.PAD, 0))
        body.grid_columnconfigure((0, 1), weight=1, uniform="half")
        self._build(body)
        self.error_label = ctk.CTkLabel(
            self, text="", font=theme.font(12), text_color=theme.ERROR, anchor="w", justify="left"
        )
        self.error_label.grid(row=1, column=0, sticky="ew", padx=theme.PAD, pady=(8, 0))
        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.grid(row=2, column=0, sticky="e", padx=theme.PAD, pady=theme.PAD)
        ctk.CTkButton(
            buttons,
            text="Vazgeç",
            command=self.destroy,
            fg_color="transparent",
            border_width=1,
            border_color=theme.BORDER,
            text_color=theme.TEXT_SOFT,
            hover_color=theme.SURFACE_2,
            font=theme.font(13),
        ).pack(side="left", padx=(0, 8))
        self.save_button = ctk.CTkButton(
            buttons,
            text="Kaydet",
            command=self.submit,
            fg_color=theme.GOLD,
            hover_color=theme.GOLD_HOVER,
            text_color=theme.GOLD_INK,
            font=theme.font(13, "bold"),
        )
        self.save_button.pack(side="left")
        if initial:
            self.set_values(initial)
        self._sync_language()
        self.after(50, self._focus)

    def _build(self, body: Any) -> None:
        row = 0

        def field(text: str, widget: Any, column: int = 0, span: int = 2) -> None:
            nonlocal row
            _label(body, text).grid(row=row, column=column, columnspan=span, sticky="w")
            widget.grid(
                row=row + 1,
                column=column,
                columnspan=span,
                sticky="ew",
                pady=(2, 10),
                padx=(0, 8) if span == 1 and column == 0 else 0,
            )
            if span == 2 or column == 1:
                row += 2

        self.title_entry = _entry(body, "ör. Bağlı listeyi tersine çevir")
        field("Başlık *", self.title_entry)
        self.prompt_box = _textbox(body, 120)
        field("Görev açıklaması *", self.prompt_box)
        self.language_menu = _menu(
            body, list(LANGUAGE_LABELS.values()), lambda _v: self._sync_language()
        )
        field("Dil *", self.language_menu, column=0, span=1)
        self.difficulty_menu = _menu(body, list(DIFFICULTY_LABELS.values()))
        self.difficulty_menu.set(DIFFICULTY_LABELS[Difficulty.EASY])
        field("Zorluk *", self.difficulty_menu, column=1, span=1)
        self.engine_menu = _menu(body, [ENGINE_LABELS[Engine.NONE]])
        field("Motor", self.engine_menu)
        self.constraints_box = _textbox(body, 70)
        field("Kısıtlar (isteğe bağlı, satır başına bir)", self.constraints_box)
        self.time_entry = _entry(body, "ör. O(n log n)")
        field("Hedef zaman (isteğe bağlı)", self.time_entry, column=0, span=1)
        self.space_entry = _entry(body, "ör. O(1)")
        field("Hedef bellek (isteğe bağlı)", self.space_entry, column=1, span=1)
        self.tags_entry = _entry(body, "ör. pointers, memory-management")
        field("Kavram etiketleri (isteğe bağlı, virgülle)", self.tags_entry)
        self.hint_entries = [_entry(body, "Boş bırakılırsa genel ipucu") for _ in HINT_FIELDS]
        for level, entry in enumerate(self.hint_entries, 1):
            field(f"{level}. seviye ipucu (isteğe bağlı)", entry)

    def _focus(self) -> None:
        with contextlib.suppress(Exception):  # pencere kapandıysa
            self.title_entry.focus_set()

    def _language(self) -> Language:
        label = self.language_menu.get()
        return next(lang for lang, text in LANGUAGE_LABELS.items() if text == label)

    def _sync_language(self) -> None:
        """Motor seçenekleri dile göre; HTML/CSS'te hedef karmaşıklık alanları kapalı."""
        language = self._language()
        engines = [ENGINE_LABELS[e] for e in engines_for(language)]
        self.engine_menu.configure(values=engines)
        if self.engine_menu.get() not in engines:
            self.engine_menu.set(engines[0])
        state = "normal" if has_complexity(language) else "disabled"
        for entry in (self.time_entry, self.space_entry):
            if state == "disabled":
                entry.delete(0, "end")
            entry.configure(state=state)

    def values(self) -> FormValues:
        """Formdaki ham metinler."""
        return {
            "title": self.title_entry.get(),
            "prompt": self.prompt_box.get("1.0", "end").strip(),
            "language": self.language_menu.get(),
            "engine": self.engine_menu.get(),
            "difficulty": self.difficulty_menu.get(),
            "constraints": self.constraints_box.get("1.0", "end").strip(),
            "expected_time": self.time_entry.get(),
            "expected_space": self.space_entry.get(),
            "concept_tags": self.tags_entry.get(),
            **{key: entry.get() for key, entry in zip(HINT_FIELDS, self.hint_entries, strict=True)},
        }

    def set_values(self, values: FormValues) -> None:
        """Formu doldurur (düzenleme)."""
        self.language_menu.set(values["language"])
        self._sync_language()
        self.engine_menu.set(values["engine"])
        self.difficulty_menu.set(values["difficulty"])
        for entry, key in (
            (self.title_entry, "title"),
            (self.time_entry, "expected_time"),
            (self.space_entry, "expected_space"),
            (self.tags_entry, "concept_tags"),
            *zip(self.hint_entries, HINT_FIELDS, strict=True),
        ):
            if str(entry.cget("state")) == "disabled":
                continue
            entry.delete(0, "end")
            if values.get(key):
                entry.insert(0, values[key])
        for box, key in ((self.prompt_box, "prompt"), (self.constraints_box, "constraints")):
            box.delete("1.0", "end")
            box.insert("1.0", values.get(key, ""))

    def submit(self) -> None:
        """Kaydet: hata yoksa pencere kapanır."""
        error = self._on_submit(self.values())
        if error:
            self.error_label.configure(text=error)
            return
        self.destroy()
