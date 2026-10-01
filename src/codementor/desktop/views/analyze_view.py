"""Analiz ekranı: araç çubuğu, görev şeridi, kod editörü ve sonuç paneli.

Görünüm iş mantığı içermez; düğmeler kurucuya verilen geri çağrıları çağırır, sonuçlar
`show_*` yöntemleriyle çizilir.
"""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Any

import customtkinter as ctk

from codementor.desktop import theme
from codementor.desktop.viewmodel import (
    ENGINE_LABELS,
    LANGUAGE_LABELS,
    StageTracker,
    engines_for,
    format_ms,
    line_marks,
    report_headline,
    report_notices,
)
from codementor.desktop.widgets.code_editor import CodeEditor
from codementor.desktop.widgets.common import Card, clear, wrap_label
from codementor.desktop.widgets.complexity_card import ComplexityCard
from codementor.desktop.widgets.finding_list import FindingList
from codementor.desktop.widgets.socratic_card import SocraticCard
from codementor.desktop.widgets.stage_timeline import StageTimeline
from codementor.desktop.widgets.task_card import TaskCard
from codementor.models.enums import Engine, Language
from codementor.models.questions import QuestionPublic
from codementor.models.report import AnalysisReport

FREE_MODE = "Serbest çalışma"
EXPORT_FORMATS: tuple[tuple[str, str], ...] = (
    ("md", "Markdown raporu (.md)"),
    ("sarif", "SARIF (.sarif)"),
    ("json", "JSON raporu (.json)"),
)


@dataclass
class AnalyzeActions:
    """Görünümün tetiklediği işlemler (uygulama denetleyicisi sağlar)."""

    analyze: Callable[[], None]
    next_hint: Callable[[], None]
    restart: Callable[[], None]
    open_file: Callable[[], None]
    load_sample: Callable[[], None]
    export: Callable[[str], None]
    questions: Callable[[Language, Engine], list[QuestionPublic]]


class AnalyzeView(ctk.CTkFrame):  # type: ignore[misc]
    def __init__(self, master: Any, actions: AnalyzeActions, language: Language) -> None:
        super().__init__(master, fg_color="transparent")
        self.actions = actions
        self.language = language
        self.engine = Engine.NONE
        self.question: QuestionPublic | None = None
        self._questions: list[QuestionPublic] = []
        self.report: AnalysisReport | None = None
        self.busy = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build_toolbar()
        self.task = TaskCard(self)

        content = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        content.grid(row=2, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=5, uniform="content")
        content.grid_columnconfigure(1, weight=4, uniform="content")
        content.grid_rowconfigure(0, weight=1)
        self.editor = CodeEditor(content)
        self.editor.grid(row=0, column=0, sticky="nsew", padx=(0, theme.GAP))

        self.panel = ctk.CTkScrollableFrame(
            content,
            fg_color="transparent",
            scrollbar_button_color=theme.SURFACE_3,
            scrollbar_button_hover_color=theme.BORDER_STRONG,
        )
        self.panel.grid(row=0, column=1, sticky="nsew")
        self.panel.grid_columnconfigure(0, weight=1)
        self.summary = ctk.CTkFrame(self.panel, fg_color="transparent", width=1, height=1)
        self.summary.grid(row=0, column=0, sticky="ew")
        self.summary.grid_columnconfigure(0, weight=1)
        self.timeline = StageTimeline(self.panel)
        self.timeline.grid(row=1, column=0, sticky="ew", pady=(0, theme.GAP))
        self.socratic = SocraticCard(self.panel, actions.next_hint, actions.restart)
        self.socratic.grid(row=2, column=0, sticky="ew", pady=(0, theme.GAP))
        self.complexity = ComplexityCard(self.panel)
        self.findings = FindingList(self.panel, self.editor.goto)
        self._refresh_engines()

    # --- Araç çubuğu ----------------------------------------------------------------------

    def _build_toolbar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        bar.grid(row=0, column=0, sticky="ew", pady=(0, theme.GAP))
        bar.grid_columnconfigure(3, weight=1)
        self.language_picker = ctk.CTkSegmentedButton(
            bar,
            values=list(LANGUAGE_LABELS.values()),
            command=self._on_language,
            height=36,
            corner_radius=10,
            font=theme.font(13, "bold"),
            fg_color=theme.SURFACE,
            selected_color=theme.SURFACE_3,
            selected_hover_color=theme.BORDER_STRONG,
            unselected_color=theme.SURFACE,
            unselected_hover_color=theme.SURFACE_2,
            text_color=theme.TEXT,
        )
        self.language_picker.set(LANGUAGE_LABELS[self.language])
        self.language_picker.grid(row=0, column=0, padx=(0, 10))
        self.engine_picker = self._menu(bar, [], self._on_engine, width=130)
        self.engine_picker.grid(row=0, column=1, padx=(0, 10))
        self.question_picker = self._menu(bar, [FREE_MODE], self._on_question, width=280)
        self.question_picker.grid(row=0, column=2, sticky="w")

        right = ctk.CTkFrame(bar, fg_color="transparent", width=1, height=1)
        right.grid(row=0, column=4, sticky="e")
        self._ghost(right, "Dosya aç", self.actions.open_file).pack(side="left", padx=(0, 6))
        self._ghost(right, "Örnek", self.actions.load_sample).pack(side="left", padx=(0, 6))
        self.export_button = self._ghost(right, "Dışa aktar ▾", self._export_menu)
        self.export_button.configure(state="disabled")
        self.export_button.pack(side="left", padx=(0, 12))
        self.run_button = ctk.CTkButton(
            right,
            text="Denetle",
            command=self.actions.analyze,
            width=150,
            height=40,
            corner_radius=12,
            font=theme.font(15, "bold"),
            fg_color=theme.GOLD,
            hover_color=theme.GOLD_HOVER,
            text_color=theme.GOLD_INK,
            text_color_disabled=theme.GOLD,
        )
        self.run_button.pack(side="left")
        ctk.CTkLabel(
            right, text="Ctrl+Enter", font=theme.font(10), text_color=theme.FAINT, height=12
        ).pack(side="left", padx=(8, 0))

    @staticmethod
    def _menu(
        master: Any, values: list[str], command: Callable[[str], None], width: int
    ) -> ctk.CTkOptionMenu:
        return ctk.CTkOptionMenu(
            master,
            values=values or [""],
            command=command,
            width=width,
            height=36,
            corner_radius=10,
            font=theme.font(13),
            dropdown_font=theme.font(13),
            fg_color=theme.SURFACE,
            button_color=theme.SURFACE,
            button_hover_color=theme.SURFACE_2,
            text_color=theme.TEXT,
            dropdown_fg_color=theme.SURFACE_2,
            dropdown_hover_color=theme.SURFACE_3,
            dropdown_text_color=theme.TEXT,
            dynamic_resizing=False,
        )

    @staticmethod
    def _ghost(master: Any, text: str, command: Callable[[], None]) -> ctk.CTkButton:
        return ctk.CTkButton(
            master,
            text=text,
            command=command,
            width=96,
            height=36,
            corner_radius=10,
            font=theme.font(13),
            fg_color=theme.SURFACE,
            hover_color=theme.SURFACE_2,
            text_color=theme.TEXT_SOFT,
            text_color_disabled=theme.FAINT,
            border_width=1,
            border_color=theme.BORDER,
        )

    def _export_menu(self) -> None:
        menu = tk.Menu(
            self,
            tearoff=0,
            bg=theme.SURFACE_2,
            fg=theme.TEXT,
            activebackground=theme.SURFACE_3,
            activeforeground=theme.TEXT,
            borderwidth=0,
            font=(theme.ui_family(), 11),
        )
        for fmt, label in EXPORT_FORMATS:
            menu.add_command(label=label, command=partial(self.actions.export, fmt))
        button = self.export_button
        menu.tk_popup(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height() + 4)

    # --- Seçimler -------------------------------------------------------------------------

    def _on_language(self, label: str) -> None:
        language = next(lang for lang, text in LANGUAGE_LABELS.items() if text == label)
        if language is self.language:
            return
        self.language = language
        self.editor.set_language(language)
        self._refresh_engines()

    def _on_engine(self, label: str) -> None:
        self.engine = next(e for e, text in ENGINE_LABELS.items() if text == label)
        self._refresh_questions()

    def _on_question(self, label: str) -> None:
        self.question = next((q for q in self._questions if q.title == label), None)
        if self.question is None:
            self.task.grid_forget()
        else:
            self.task.show(self.question)
            self.task.grid(row=1, column=0, sticky="ew", pady=(0, theme.GAP))

    def _refresh_engines(self) -> None:
        engines = engines_for(self.language)
        if self.engine not in engines:
            self.engine = engines[0]
        self.engine_picker.configure(values=[ENGINE_LABELS[e] for e in engines])
        self.engine_picker.set(ENGINE_LABELS[self.engine])
        self._refresh_questions()

    def _refresh_questions(self) -> None:
        self._questions = self.actions.questions(self.language, self.engine)
        self.question_picker.configure(values=[FREE_MODE, *(q.title for q in self._questions)])
        keep = self.question is not None and self.question in self._questions
        self.question_picker.set(self.question.title if keep and self.question else FREE_MODE)
        self._on_question(self.question_picker.get())

    def select(self, language: Language, engine: Engine, question_id: str | None) -> None:
        """Dışarıdan seçim (soru bankası, geçmiş, tercihler)."""
        self.language = language
        self.language_picker.set(LANGUAGE_LABELS[language])
        self.editor.set_language(language)
        self.engine = engine
        self.question = None
        self._refresh_engines()
        if question_id:
            match = next((q for q in self._questions if q.id == question_id), None)
            if match is not None:
                self.question_picker.set(match.title)
                self._on_question(match.title)

    # --- Durum ve sonuçlar ----------------------------------------------------------------

    def set_busy(self, busy: bool) -> None:
        self.busy = busy
        self.run_button.configure(
            state="disabled" if busy else "normal",
            text="Denetleniyor…" if busy else "Denetle",
            fg_color=theme.GOLD_DIM if busy else theme.GOLD,
        )
        if busy:
            self.socratic.show_busy()
            self._clear_summary()
            self.complexity.grid_forget()
            self.findings.grid_forget()
        self.export_button.configure(state="disabled" if busy or not self.report else "normal")

    def show_progress(self, tracker: StageTracker) -> None:
        self.timeline.update_groups(
            tracker.groups(), tracker.completed_ratio(), tracker.total_ms(), self.busy
        )

    def show_report(self, report: AnalysisReport) -> None:
        self.report = report
        self.editor.set_marks(
            line_marks(report.findings, report.compilation.diagnostics, self.editor.line_count())
        )
        self._clear_summary()
        total = sum(report.meta.stage_latency_ms.values())
        headline = ctk.CTkFrame(self.summary, fg_color="transparent", width=1, height=1)
        headline.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkLabel(
            headline,
            text=report_headline(report),
            font=theme.font(13, "bold"),
            text_color=theme.TEXT,
        ).pack(side="left")
        ctk.CTkLabel(
            headline,
            text=f"{format_ms(total)} · {report.meta.provider or 'LLM yok'}",
            font=theme.font(12),
            text_color=theme.MUTED,
        ).pack(side="right")
        notices = report_notices(report)
        if notices:
            self._notice(notices, theme.WARN, row=1)
        self.socratic.show(report.socratic)
        if report.complexity is not None:
            self.complexity.show(report.complexity)
            self.complexity.grid(row=3, column=0, sticky="ew", pady=(0, theme.GAP))
        else:
            self.complexity.grid_forget()
        self.findings.show(report.findings, report.compilation.diagnostics)
        self.findings.grid(row=4, column=0, sticky="ew", pady=(0, theme.GAP))
        self.export_button.configure(state="normal")
        self.panel._parent_canvas.yview_moveto(0)

    def show_error(self, message: str) -> None:
        self._clear_summary()
        self._notice([message], theme.ERROR, row=0)
        self.socratic.show_empty()

    def reset_results(self) -> None:
        self.report = None
        self._clear_summary()
        self.socratic.show_empty()
        self.complexity.grid_forget()
        self.findings.grid_forget()
        self.editor.set_marks([])
        self.export_button.configure(state="disabled")
        self.timeline.update_groups(StageTracker().groups(), 0, 0, busy=False)

    def _clear_summary(self) -> None:
        clear(self.summary)

    def _notice(self, lines: list[str], color: str, row: int) -> None:
        card = Card(self.summary)
        card.configure(border_color=color)
        card.grid(row=row, column=0, sticky="ew", pady=(0, theme.GAP))
        for i, line in enumerate(lines):
            wrap_label(card.body, line, size=13, color=color).grid(
                row=i, column=0, sticky="ew", pady=(0, 4)
            )
