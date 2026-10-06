"""CodeMentor masaüstü uygulaması (ADR-0013): ana pencere ve denetleyici.

Çekirdek doğrudan çağrılır (sunucu yok): `ApiState` orkestratörü, veritabanını ve soru bankasını
sağlar; uzun işler `Bridge` üzerinden arka planda koşar, sonuçlar `after()` ile ana thread'de
işlenir.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Any

import customtkinter as ctk

from codementor.api.state import ApiState
from codementor.config import CONFIG_FILE_ENV, DEFAULT_CONFIG_FILE, Settings, load_settings
from codementor.desktop import questions_controller, runtime, theme
from codementor.desktop.bridge import Bridge, Cancellation, Message, analysis_work
from codementor.desktop.config_writer import write_provider_prefs
from codementor.desktop.connections import KeyStore, apply_overrides
from codementor.desktop.connections_controller import ConnectionsController
from codementor.desktop.files import FileController
from codementor.desktop.services import render_export
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
from codementor.storage.cache import (
    clear_analyses,
    delete_analysis,
    get_analysis,
    get_row,
    list_analyses,
)
from codementor.storage.db import AnalysisRow, resolve_db_path

ASSETS = Path(__file__).resolve().parent / "assets"
POLL_MS = 60
WINDOW_SIZE = (1480, 940)
TOAST_MS = 2600
CLOSE_JOIN_S = 2.0  # kapanışta süren analizin iptalini bekleme süresi
_EXPORT_SUFFIX = {"md": ".md", "sarif": ".sarif", "json": ".json"}
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
        self.apply_settings()
        if not self.prefs.session_id:
            self._new_session()
        self.bridge = Bridge()
        self.connections = ConnectionsController(self, key_store or KeyStore())
        self.files = FileController(self)
        self.tracker = StageTracker()
        self._closing = False
        self._last_code = ""
        self._last_question_id: str | None = None
        self._last_counted: bool | None = None

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
            ),
            self.prefs.language,
        )
        self.analyze_view.select(self.prefs.language, self.prefs.engine, None)
        self.analyze_view.editor.set(SAMPLES[self.prefs.language], self.prefs.language)
        self.files.enable_drop(self.analyze_view.editor.text)
        self.questions_view = QuestionsView(stage, self._filtered_questions, self.start_question)
        self.history_view = HistoryView(
            stage,
            self._history_rows,
            self.open_history,
            on_delete=self.delete_history,
            on_clear=self.clear_history,
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
        return self.prefs.provider or self.settings.providers.default

    def base_default(self) -> str:
        """`codementor.toml`'daki varsayılan sağlayıcı."""
        return self.base_settings.providers.default

    def current_model(self) -> str:
        config = getattr(self.settings.providers, self.provider_name(), None)
        return str(config.model) if config is not None else ""

    def apply_settings(self) -> None:
        """Arayüz seçimlerini (model, adres) ayarlara uygular; sonraki analizler bunu kullanır."""
        self.settings = apply_overrides(self.base_settings, self.prefs)
        self.core.settings = self.settings

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
        """Esc yalnız analiz sayfasında durdurur (başka sayfada açılır liste kapatmak gibi)."""
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
        """İpucu merdivenini sıfırlar (`questions_controller`, Faz 54)."""
        self._last_counted = None
        questions_controller.restart(self)

    def _new_session(self) -> None:
        questions_controller.new_session(self)

    def _on_message(self, message: Message) -> None:
        if message.task.partition(":")[0] in ("probe", "test", "compilers", "toolchain"):
            self.connections.handle(message)
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
            keep = self.core.settings.storage.max_analyses
            runtime.save_source(report.analysis_id, self._last_code, self.prefs_dir, keep=keep)
            self._last_counted = not report.meta.early_exit and not report.meta.degraded
            view.show_report(report)
        else:
            self._last_counted = None
            view.show_error(str(message.payload))

    # --- Dosyalar -----------------------------------------------------------------------

    def load_sample(self) -> None:
        questions_controller.load_sample(self)

    def export(self, fmt: str) -> None:
        report = self.analyze_view.report
        if report is None:
            return
        suffix = _EXPORT_SUFFIX[fmt]
        path = filedialog.asksaveasfilename(
            title="Raporu dışa aktar",
            defaultextension=suffix,
            initialfile=f"codementor-{report.analysis_id}{suffix}",
        )
        if not path:
            return
        Path(path).write_text(render_export(report, fmt), encoding="utf-8")
        self.toast(f"Rapor kaydedildi: {Path(path).name}")

    # --- Sorular ve geçmiş --------------------------------------------------------------

    def questions_for(self, language: Language, engine: Engine) -> list[QuestionPublic]:
        return questions_controller.questions_for(self.core, language, engine)

    def _filtered_questions(
        self, language: Language | None, difficulty: Difficulty | None
    ) -> list[QuestionPublic] | None:
        """Filtrelenmiş sorular; banka okunamazsa None (görünüm 'okunamadı' der)."""
        return questions_controller.filtered(self.core, language, difficulty)

    def start_question(self, question: QuestionPublic) -> None:
        self._last_counted = None
        questions_controller.start(self, question)

    def _history_rows(self) -> list[AnalysisRow]:
        return list_analyses(self.core.database())

    def open_history(self, analysis_id: str) -> None:
        report = get_analysis(self.core.database(), analysis_id)
        if report is not None:
            view = self.analyze_view
            view.select(report.language, report.engine, report.question_id)
            code = runtime.load_source(analysis_id, self.prefs_dir)
            view.editor.set(code or "// Bu analizin kodu saklanmamış.\n", report.language)
            self.tracker.reset()
            self.tracker.finish()
            view.reset_results()
            view.show_report(report)
            self.navigate("analyze")
            return

        row = get_row(self.core.database(), analysis_id)
        if row is None:
            self.toast("Bu analiz artık bulunamıyor.")
            return

        view = self.analyze_view
        try:
            lang = Language(row.language)
        except ValueError:
            lang = view.language
        try:
            eng = Engine(row.engine)
        except ValueError:
            eng = view.engine

        view.select(lang, eng, row.question_id)
        code = runtime.load_source(analysis_id, self.prefs_dir)
        view.editor.set(code or "// Bu analizin kodu saklanmamış.\n", lang)
        self.tracker.reset()
        self.tracker.finish()
        view.reset_results()
        self.toast(
            "Bu rapor farklı bir CodeMentor sürümüyle oluşturulduğu için gösterilemiyor. "
            "Kodu editöre açtım; yeniden denetleyebilirsin."
        )
        self.navigate("analyze")

    def delete_history(self, analysis_id: str) -> None:
        """Kayıtlı bir analizi ve saklanan kodunu siler (Faz 62)."""
        deleted_db = delete_analysis(self.core.database(), analysis_id)
        deleted_file = runtime.delete_source(analysis_id, self.prefs_dir)
        if not deleted_db and not deleted_file:
            self.toast("Analiz bulunamadı.")
            return
        if (
            self.analyze_view.report is not None
            and self.analyze_view.report.analysis_id == analysis_id
        ):
            self.analyze_view.report = None
            self.analyze_view.reset_results()
        self.history_view.refresh()
        self.toast("Analiz geçmişten silindi.")

    def clear_history(self) -> None:
        """Tüm analiz geçmişini ve saklanan kodları temizler (Faz 62)."""
        if not messagebox.askyesno(
            "Geçmişi Temizle",
            "Tüm analiz geçmişi ve saklanan kodlar silinsin mi?\nBu işlem geri alınamaz.",
            parent=self,
        ):
            return
        clear_analyses(self.core.database())
        runtime.clear_sources(self.prefs_dir)
        self.analyze_view.report = None
        self.analyze_view.reset_results()
        self.history_view.refresh()
        self.toast("Tüm analiz geçmişi temizlendi.")

    # --- Ayarlar ve ortam ---------------------------------------------------------------

    def check_environment(self) -> None:
        """Tüm sağlayıcıları ve derleyicileri yoklar (açılışta ve Bağlantılar ekranında)."""
        self.connections.refresh_all()

    def open_folder(self, path: str) -> None:
        target = Path(path)
        folder = target if target.is_dir() else target.parent
        if sys.platform == "win32" and folder.is_dir():
            os.startfile(folder)

    def _locations(self) -> list[tuple[str, str]]:
        config = os.environ.get(CONFIG_FILE_ENV, DEFAULT_CONFIG_FILE)
        return [
            ("Yapılandırma", str(Path(config).resolve())),
            ("Veritabanı", str(resolve_db_path(self.settings))),
            ("Kullanıcı verisi", str(runtime.user_dir())),
        ]

    def write_config(self) -> None:
        """Model ve varsayılan sağlayıcı seçimlerini `codementor.toml`'a işler (anahtar hariç)."""
        try:
            path = write_provider_prefs(runtime.writable_config_file(), self.prefs)
        except (OSError, ValueError) as exc:  # salt okunur konum, bozuk toml
            self.toast(f"codementor.toml yazılamadı: {exc}")
            return
        self.toast(f"Seçimler yazıldı: {path}")

    def reload_config(self) -> None:
        """`codementor.toml`'u (ve ortamı) yeniden okur; arayüz seçimleri yine üstüne uygulanır.
        Bozuk dosya uygulanmaz. Veritabanı yolu gibi açılışta kurulanlar yeniden başlatma ister."""
        try:
            base = load_settings()
        except Exception as exc:  # bozuk toml, geçersiz değer, okunamayan dosya
            self.toast(f"codementor.toml okunamadı: {exc}")
            return
        self.base_settings = base
        self.apply_settings()
        self.connections.refresh_all()
        self.toast("codementor.toml yeniden yüklendi")

    def save_prefs(self, **changes: Any) -> None:
        self.prefs = self.prefs.model_copy(update=changes)
        runtime.save_prefs(self.prefs, self.prefs_dir)

    # --- Döngü ve kapanış ---------------------------------------------------------------

    def _poll(self) -> None:
        if self._closing:
            return
        for message in self.bridge.drain():
            self._on_message(message)
        self.after(POLL_MS, self._poll)

    def close(self) -> None:
        self._closing = True
        self.bridge.cancel_all()
        # İptal zinciri (loop → CLI süreç ağacı) yorumlayıcı kapanmadan tamamlansın
        self.bridge.join("analyze", CLOSE_JOIN_S)
        self.core.close()
        self.destroy()
