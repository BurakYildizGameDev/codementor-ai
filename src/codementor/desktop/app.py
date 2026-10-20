"""CodeMentor masaüstü uygulaması (ADR-0013): ana pencere ve denetleyici.

Çekirdek doğrudan çağrılır (sunucu yok): `ApiState` orkestratörü, veritabanını ve soru bankasını
sağlar; uzun işler `Bridge` üzerinden arka planda koşar, sonuçlar `after()` ile ana thread'de
işlenir.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from tkinter import messagebox
from typing import Any

import customtkinter as ctk

from codementor.api.state import ApiState
from codementor.config import Settings
from codementor.desktop import (
    config_controller,
    history_controller,
    questions_controller,
    runtime,
    theme,
)
from codementor.desktop.bridge import Bridge, Cancellation, Message, analysis_work
from codementor.desktop.connections import KeyStore
from codementor.desktop.connections_controller import ConnectionsController
from codementor.desktop.files import FileController
from codementor.desktop.viewmodel import SAMPLES, StageTracker
from codementor.desktop.views.analyze_view import AnalyzeActions, AnalyzeView
from codementor.desktop.views.connections_view import ConnectionsView
from codementor.desktop.views.history_view import HistoryView
from codementor.desktop.views.questions_view import QuestionsView
from codementor.desktop.widgets.sidebar import Sidebar
from codementor.log import get_logger
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.pipeline import StageEvent
from codementor.models.questions import QuestionPublic
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisOptions, AnalysisRequest
from codementor.providers.factory import PROVIDER_NAMES

ASSETS = Path(__file__).resolve().parent / "assets"
POLL_MS = 60
WINDOW_SIZE = (1480, 940)
TOAST_MS = 2600
CLOSE_JOIN_S = 2.0  # kapanışta süren analizin iptalini bekleme süresi
CONNECTIONS_TASKS = ("probe", "test", "compilers", "toolchain", "pull")  # F10: "pull"
log = get_logger("codementor.desktop")


class App(ctk.CTk):  # type: ignore[misc]
    """Ana pencere. Testler `state` (FakeProvider'lı) ve `prefs_dir` verip denetimleri kapatır."""

    def __init__(
        self,
        state: ApiState,
        prefs_dir: Path | None = None,
        check_on_start: bool = True,
        key_store: KeyStore | None = None,
    ) -> None:
        ctk.set_appearance_mode("dark")
        super().__init__(fg_color=theme.BG)
        self.core = state
        self.base_settings: Settings = state.settings  # toml + ortam; arayüz seçimleri üstüne
        self.prefs_dir = prefs_dir
        self.prefs = runtime.load_prefs(prefs_dir)
        if self.prefs.provider not in (None, *PROVIDER_NAMES):
            self.prefs = self.prefs.model_copy(update={"provider": None})
        self.settings: Settings = state.settings
        self.tracker = StageTracker()
        self.apply_settings()
        if not self.prefs.session_id:
            questions_controller.new_session(self)
        self.bridge = Bridge()
        self.connections = ConnectionsController(self, key_store or KeyStore())
        self.files = FileController(self)
        self._closing = False
        self._last_code: str = ""
        self._last_question_id: str | None = None
        self._last_counted: bool | None = None
        self._shown_analysis_id: str | None = None
        self._opening_analysis_id: str | None = None  # geçmiş kaydı arka planda açılıyor (#40)
        self.confirm: Callable[..., bool] = messagebox.askyesno

        self.title("CodeMentor AI")
        self._place_window()
        icon = ASSETS / "icon.ico"
        if sys.platform == "win32" and icon.is_file():
            self.iconbitmap(str(icon))
        # CTk mainloop başlarken başlık çubuğunu kendi rengine çevirir; ardından yeniden uygula
        self.after(250, lambda: theme.apply_window_chrome(self))
        self._build()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.bind_all("<Control-Return>", lambda _e: self.analyze())
        self.bind_all("<Escape>", lambda _e: self.on_escape())
        for seq in ("<Control-s>", "<Control-S>"):
            self.bind_all(seq, lambda _e: self.files.save())
        self.after(POLL_MS, self._poll)
        if check_on_start:
            self.after(300, self.check_environment)

    # --- Yerleşim -----------------------------------------------------------------------

    def _build(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar = Sidebar(self, ASSETS / "logo.png", self.navigate)
        self.sidebar.on_status_click(lambda: self.navigate("settings"))
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.set_provider(self.provider_name(), None)
        stage = ctk.CTkFrame(self, fg_color=theme.BG, corner_radius=0)
        stage.grid(row=0, column=1, sticky="nsew", padx=28, pady=(24, 20))
        stage.grid_columnconfigure(0, weight=1)
        stage.grid_rowconfigure(0, weight=1)

        self.analyze_view = AnalyzeView(
            stage,
            AnalyzeActions(
                analyze=self.analyze,
                stop=self.stop_analysis,
                next_hint=lambda: self.analyze(advance=True),
                restart=self.restart,
                open_file=self.files.open_dialog,
                recent_files=self.files.recent,
                open_recent=self.files.open_recent,
                load_sample=self.load_sample,
                export=self.export,
                questions=self.questions_for,
                notify=self.toast,
                on_code_change=self.files.mark_dirty,
            ),
            self.prefs.language,
        )
        self.analyze_view.select(self.prefs.language, self.prefs.engine, None)
        self.analyze_view.editor.set(SAMPLES[self.prefs.language], self.prefs.language)
        self.files.enable_drop(self.analyze_view.editor.text)
        self.questions_view = QuestionsView(
            stage,
            self._filtered_questions,
            self.start_question,
            on_add=lambda: questions_controller.open_add(self),
            on_edit=lambda q: questions_controller.open_edit(self, q),
            on_delete=lambda q: questions_controller.delete_user(self, q),
            warnings=lambda: questions_controller.bank_warnings(self.core),
        )
        self.history_view = HistoryView(
            stage,
            on_open=self.open_history,
            on_delete=self.delete_history,
            on_clear=self.clear_history,
            is_busy=lambda: self.analyze_view.busy,
            request_page=self._request_history_page,
        )
        self.settings_view = ConnectionsView(
            stage,
            self.connections.actions(),
            self.open_folder,
            self._locations(),
            write_config=self.write_config,
            reload_config=self.reload_config,
            download=self.connections.download_compiler,
            cancel_download=self.connections.cancel_download,
            purge_legacy=self.connections.purge_legacy_keys,
        )
        self.connections.attach(self.settings_view)
        self.views: dict[str, ctk.CTkFrame] = {
            "analyze": self.analyze_view,
            "questions": self.questions_view,
            "history": self.history_view,
            "settings": self.settings_view,
        }
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")
        self.toast_label = ctk.CTkLabel(
            self,
            text="",
            fg_color=theme.SURFACE_3,
            corner_radius=10,
            text_color=theme.TEXT,
            font=theme.font(13),
            height=38,
        )
        self.navigate("analyze")

    def _place_window(self) -> None:
        """Ekrana sığan, ortalanmış pencere; küçük ekranda (Windows) tam ekran açılır."""
        screen_w, screen_h = self.winfo_screenwidth(), self.winfo_screenheight()
        width, height = min(WINDOW_SIZE[0], screen_w - 80), min(WINDOW_SIZE[1], screen_h - 120)
        self.minsize(min(1100, width), min(700, height))
        self.geometry(f"{width}x{height}+{(screen_w - width) // 2}+{(screen_h - height) // 3}")
        if sys.platform == "win32" and (screen_w < 1600 or screen_h < 1000):
            self.after(0, lambda: self.state("zoomed"))

    def navigate(self, key: str) -> None:
        self.sidebar.select(key)
        if key == "questions":
            self.questions_view.refresh()
        elif key == "history":
            self.history_view.refresh()
        self.views[key].tkraise()
        self.current_view = key

    def toast(self, text: str) -> None:
        self.toast_label.configure(text=f"   {text}   ")
        self.toast_label.place(relx=0.5, rely=1.0, y=-28, anchor="s")
        self.toast_label.lift()
        self.after(TOAST_MS, self.toast_label.place_forget)

    # --- Analiz -------------------------------------------------------------------------

    def provider_name(self) -> str:
        return config_controller.provider_name(self)

    def base_default(self) -> str:
        return config_controller.base_default(self)

    def current_model(self) -> str:
        return config_controller.current_model(self)

    def apply_settings(self) -> None:
        config_controller.apply_settings(self)

    def analyze(self, *, advance: bool | None = None) -> None:
        view = self.analyze_view
        if self.bridge.is_running("analyze"):
            if not view.busy:  # durdurulan önceki analizin iş parçacığı henüz kapanıyor
                self.toast("Önceki analiz kapanıyor, birazdan yeniden deneyin.")
            return
        code = view.editor.get()
        if not code.strip():
            view.show_error("Analiz edilecek kod yok: editöre kod yaz ya da bir dosya aç.")
            return
        self.navigate("analyze")
        current_qid = view.question.id if view.question else None
        if (
            advance is None
            and code == self._last_code
            and current_qid == self._last_question_id
            and self._last_counted is True
        ):
            advance = False
        request = AnalysisRequest(
            code=code,
            language=view.language,
            engine=view.engine,
            question_id=current_qid,
            session_id=self.prefs.session_id,
            provider=self.prefs.provider,
            options=AnalysisOptions(advance_hint=advance),
        )
        self._last_code = code
        self._last_question_id = current_qid
        self.save_prefs(language=view.language, engine=view.engine)
        self.tracker.reset()
        view.set_busy(True)
        view.show_progress(self.tracker)
        cancellation = Cancellation()
        self.bridge.submit(
            "analyze", analysis_work(self.core, request, cancellation), cancellation=cancellation
        )

    def on_escape(self) -> None:
        if self.current_view == "analyze":
            self.stop_analysis()

    def stop_analysis(self) -> None:
        """Süren analizi durdurur: LLM çağrısı ve CLI süreci iptal edilir, sonuç yazılmaz."""
        view = self.analyze_view
        if not view.busy:
            return
        self.bridge.cancel("analyze")
        self.tracker.reset()
        view.set_busy(False)
        view.reset_results()
        self.toast("Analiz durduruldu.")

    def restart(self) -> None:
        self._last_counted = None
        questions_controller.restart(self)

    def _on_message(self, message: Message) -> None:
        if message.task.partition(":")[0] in CONNECTIONS_TASKS:
            self.connections.handle(message)
            return
        if message.task in history_controller.HISTORY_TASKS:  # F11: geçmiş DB işleri arka planda
            history_controller.handle(self, message)
            return
        handler = getattr(self, f"_on_{message.task}", None)
        if handler is not None:
            handler(message)

    def _on_analyze(self, message: Message) -> None:
        view = self.analyze_view
        if message.kind == "event" and isinstance(message.payload, StageEvent):
            self.tracker.apply(message.payload)
            view.show_progress(self.tracker)
            return
        self.tracker.finish()
        view.set_busy(False)
        view.show_progress(self.tracker)
        if message.kind == "result" and isinstance(message.payload, AnalysisReport):
            report = message.payload
            self._shown_analysis_id = report.analysis_id
            keep = self.core.settings.storage.max_analyses
            runtime.save_source(report.analysis_id, self._last_code, self.prefs_dir, keep=keep)
            self._last_counted = not report.meta.early_exit and not report.meta.degraded
            view.show_report(report)
        else:
            self._shown_analysis_id = None
            self._last_counted = None
            view.show_error(str(message.payload))

    # --- Dosyalar -----------------------------------------------------------------------
    def load_sample(self) -> None:
        questions_controller.load_sample(self)

    def export(self, fmt: str) -> None:
        history_controller.export(self, fmt)

    # --- Sorular ve geçmiş --------------------------------------------------------------
    def questions_for(self, language: Language, engine: Engine) -> list[QuestionPublic]:
        return questions_controller.questions_for(self.core, language, engine)

    def _filtered_questions(
        self, language: Language | None, difficulty: Difficulty | None
    ) -> list[QuestionPublic] | None:
        return questions_controller.filtered(self.core, language, difficulty)

    def start_question(self, question: QuestionPublic) -> None:
        self._last_counted = None
        questions_controller.start(self, question)

    def _request_history_page(
        self, limit: int, before: str | None, search: str | None, append: bool
    ) -> None:
        """Geçmiş listesini arka planda okutur (Faz F, F11)."""
        history_controller.refresh(self, limit=limit, before=before, search=search, append=append)

    def open_history(self, analysis_id: str) -> None:
        history_controller.open_history(self, analysis_id)

    def delete_history(self, analysis_id: str) -> None:
        history_controller.delete(self, analysis_id)

    def clear_history(self) -> None:
        history_controller.clear(self)

    # --- Ayarlar ve ortam ---------------------------------------------------------------
    def check_environment(self) -> None:
        self.connections.refresh_all()

    def open_folder(self, path: str) -> None:
        config_controller.open_folder(path)

    def _locations(self) -> list[tuple[str, str]]:
        return config_controller.locations(self)

    def write_config(self) -> None:
        config_controller.write_config(self)

    def reload_config(self) -> None:
        config_controller.reload_config(self)

    def save_prefs(self, **changes: Any) -> None:
        self.prefs = self.prefs.model_copy(update=changes)
        runtime.save_prefs(self.prefs, self.prefs_dir)

    # --- Döngü ve kapanış ---------------------------------------------------------------
    def _poll(self) -> None:
        if self._closing:
            return
        for message in self.bridge.drain():
            self._on_message(message)
        if self.analyze_view.busy:  # Faz 63: uzun LLM geçişinde "takılmadı" uyarısı
            self.analyze_view.timeline.set_hint(self.tracker.slow_hint())
        self.after(POLL_MS, self._poll)

    def close(self) -> None:
        if not runtime.confirm_close(self):
            return
        self._closing = True
        self.bridge.cancel_all()
        # İptal zinciri (loop → CLI süreç ağacı) yorumlayıcı kapanmadan tamamlansın
        self.bridge.join("analyze", CLOSE_JOIN_S)
        self.core.close()
        self.destroy()

    def report_callback_exception(
        self, exc_type: type[BaseException], exc: BaseException, tb: Any
    ) -> None:
        """Tkinter olay geri çağrılarındaki beklenmeyen hataları yakalar (Faz F, O10)."""
        log.error("Arayüzde beklenmeyen hata", exc_info=(exc_type, exc, tb))
        self.toast("Beklenmeyen bir hata oldu; ayrıntı desktop.log'da.")
