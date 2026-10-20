"""Pencere duman testi: gerçek Tk penceresi + FakeProvider. Ekran yoksa (Linux CI) atlanır.

Bölüm 3/5.
"""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from pathlib import Path

import pytest

from codementor.desktop import connections_controller as controller_module
from codementor.desktop import runtime
from codementor.desktop.app import App
from codementor.desktop.login import LoginUnavailableError, manual_login_hint
from codementor.desktop.services import PullOutcome
from codementor.models.enums import Difficulty, Language
from codementor.storage.db import AnalysisRow
from codementor.validation.toolchain_install import InstallCancelledError, ToolchainInstallError
from tests.desktop.app_support import (
    _compilers_message,
    _toast,
    open_and_wait,
    pump,
)


def test_compiler_download_error_shown(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    def failing(settings: object, **_kwargs: object) -> Path:
        raise ToolchainInstallError("İndirilen dosya doğrulanamadı (sha256 uyuşmuyor).")

    monkeypatch.setattr(controller_module, "install_zig", failing)
    view = app.settings_view
    view.download_button.invoke()
    pump(app, lambda: not view.downloading)
    assert "sha256 uyuşmuyor" in str(view.download_text.cget("text"))
    assert view.download_button.grid_info()  # yeniden denenebilir


def test_compiler_download_cancel(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    started = threading.Event()
    stopped = threading.Event()

    release = threading.Event()

    def waiting(settings: object, *, progress: object, cancel: threading.Event) -> Path:
        started.set()
        assert cancel.wait(10), "iptal gelmedi"
        stopped.set()
        assert release.wait(10)  # yarım dosyaların silinmesi sürüyor
        raise InstallCancelledError

    monkeypatch.setattr(controller_module, "install_zig", waiting)
    view = app.settings_view
    view.download_button.invoke()
    assert started.wait(5)
    view.download_cancel.invoke()
    assert stopped.wait(5)  # arka plandaki indirme gerçekten durdu
    # işçi bitmeden "iptal edildi / silindi" denmez; yeniden başlatma da reddedilir (denetim O2)
    assert "İptal ediliyor" in str(view.download_text.cget("text"))
    assert view.downloading
    view.download_button.invoke()
    assert "kapanıyor" in _toast(app)
    release.set()
    app.bridge.join("toolchain", 5)
    pump(app, lambda: not view.downloading)
    assert "iptal edildi" in str(view.download_text.cget("text"))
    assert view.download_button.grid_info()


def test_compiler_update_button_when_installed_zig_is_old(
    app: App, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz F (F9): kurulu zig eskiyken kart "Derleyiciyi güncelle" düğmesi gösterir."""
    monkeypatch.setattr(controller_module, "compiler_update_available", lambda _settings: False)
    view = app.settings_view
    app.connections.handle(_compilers_message("zig (indirilen)"))
    assert not view.download_box.grid_info()  # güncel: kutu (ve düğme) görünmez

    monkeypatch.setattr(controller_module, "compiler_update_available", lambda _settings: True)
    app.connections.handle(_compilers_message("zig (indirilen)"))
    assert view.download_button.grid_info()
    assert "güncelle" in str(view.download_button.cget("text")).lower()
    assert "Güncelleme var" in str(view.download_text.cget("text"))


def test_compiler_update_button_downloads_through_same_flow(
    app: App, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz F (F9): güncelleme düğmesi mevcut indirme akışını (install_zig) kullanır."""
    monkeypatch.setattr(controller_module, "compiler_update_available", lambda _settings: True)
    done = threading.Event()

    def fake_install(settings: object, **_kwargs: object) -> Path:
        done.set()
        return Path("/tc/zig/zig")

    monkeypatch.setattr(controller_module, "install_zig", fake_install)
    view = app.settings_view
    app.connections.handle(_compilers_message("zig (indirilen)"))
    view.download_button.invoke()
    assert done.wait(5)
    pump(app, lambda: not view.downloading)
    assert "kuruldu" in _toast(app)


# --- Faz F (F10): `ollama pull` düğmesi --------------------------------------------------------


def test_ollama_pull_button_runs_through_background_task(
    app: App, monkeypatch: pytest.MonkeyPatch
) -> None:
    """F10: kart düğmesi argv ile arka plan görevini başlatır; sonuç kartta ve toast'ta."""
    app.connections.check = lambda _name: None  # type: ignore[method-assign]
    app.connections.set_model("ollama", "qwen2.5-coder:7b")
    card = app.settings_view.cards["ollama"]
    model = card.model.get()
    assert model == "qwen2.5-coder:7b"
    seen: list[tuple[str, list[str]]] = []
    proceed = threading.Event()
    off_main: list[bool] = []

    def fake_pull(model_name: str, argv: list[str]) -> PullOutcome:
        seen.append((model_name, argv))
        off_main.append(threading.current_thread() is not threading.main_thread())
        assert proceed.wait(10)
        return PullOutcome(True, f"{model_name} indirildi.")

    monkeypatch.setattr(controller_module, "run_ollama_pull", fake_pull)
    monkeypatch.setattr(
        controller_module, "ollama_pull_argv", lambda m, _path: ["/opt/ollama", "pull", m]
    )
    card.pull_button.invoke()
    assert app.bridge.is_running("pull:ollama")  # iş arka planda (arayüz kilitlenmez)
    assert "indiriliyor" in str(card.detail.cget("text"))
    proceed.set()
    pump(app, lambda: "indirildi" in _toast(app))
    assert off_main == [True]  # DB/ağ işi ana iş parçacığında değil
    assert seen == [(model, ["/opt/ollama", "pull", model])]
    assert "indirildi" in str(card.detail.cget("text"))


def test_ollama_pull_without_binary_warns_and_starts_nothing(
    app: App, monkeypatch: pytest.MonkeyPatch
) -> None:
    """F10: ollama PATH'te yoksa düğme Türkçe uyarır; hiçbir süreç/görev başlamaz."""
    app.connections.check = lambda _name: None  # type: ignore[method-assign]
    app.connections.set_model("ollama", "qwen2.5-coder:7b")
    card = app.settings_view.cards["ollama"]
    monkeypatch.setenv("PATH", "")
    card.pull_button.invoke()
    assert "Ollama bulunamadı" in _toast(app)
    assert "Ollama bulunamadı" in str(card.detail.cget("text"))
    assert not app.bridge.is_running("pull:ollama")


# --- Faz F (F12): Linux/macOS'ta "oturum aç" ------------------------------------------------


def test_login_starts_console_and_points_to_check(
    app: App, monkeypatch: pytest.MonkeyPatch
) -> None:
    """F12: kart eylemi oturum açma penceresini açar; kart kullanıcıyı Denetle'ye yönlendirir."""
    seen: list[str] = []

    def fake_open(name: str, _providers: object) -> None:
        seen.append(name)

    monkeypatch.setattr(controller_module, "open_login_console", fake_open)
    app.connections.login("claude_cli")
    card = app.settings_view.cards["claude_cli"]
    assert seen == ["claude_cli"]
    assert "Açılan pencerede oturum aç" in str(card.detail.cget("text"))


def test_login_without_terminal_shows_command_toast(
    app: App, monkeypatch: pytest.MonkeyPatch
) -> None:
    """F12: terminal yoksa hiçbir süreç başlamaz; bildirim elle çalıştırılacak komutu söyler."""
    hint = manual_login_hint(["claude", "auth", "login"])

    def unavailable(name: str, _providers: object) -> None:
        raise LoginUnavailableError(name, hint)

    monkeypatch.setattr(controller_module, "open_login_console", unavailable)
    app.connections.login("claude_cli")
    text = _toast(app)
    assert "Terminalde şu komutu çalıştırın: claude auth login" in text
    assert not text.strip().startswith("claude_cli:")  # sağlayıcı ön eki kullanıcıya gösterilmez


def test_question_difficulty_filter(app: App) -> None:
    """Faz 30: dil ve zorluk filtreleri birlikte uygulanır; sayı etiketi güncellenir."""
    app.navigate("questions")
    view = app.questions_view
    expected = app.core.questions().filter(Language.C, None, Difficulty.HARD)
    assert len(expected) >= 1
    view.filter.set("C")
    view.difficulty_filter.set("Zor")
    view.refresh()
    assert view.count_label.cget("text") == f"{len(expected)} soru"
    assert len(view.grid_area.winfo_children()) == len(expected)
    view.filter.set("Tümü")
    view.difficulty_filter.set("Tümü")
    view.refresh()
    assert view.count_label.cget("text") == f"{len(app.core.questions())} soru"


def test_question_view_messages(app: App, monkeypatch: pytest.MonkeyPatch) -> None:
    """Boş filtre sonucu ile okunamayan banka farklı mesaj verir (denetim D1)."""
    app.navigate("questions")
    view = app.questions_view

    def label_texts() -> list[str]:
        return [str(w.cget("text")) for w in view.grid_area.winfo_children()]

    monkeypatch.setattr(view, "_load", lambda _l, _d: [])
    view.difficulty_filter.set("Zor")
    view.refresh()
    assert label_texts() == ["Bu filtrelerle eşleşen soru yok."]

    monkeypatch.setattr(view, "_load", lambda _l, _d: None)
    view.refresh()
    assert label_texts() == ["Soru bankası boş ya da okunamadı."]


def test_finding_list_groups_suggestions(app: App) -> None:
    """Faz 36: hatalar açık, öneriler "Öneriler (n)" düğmesinin altında katlı."""
    from codementor.models.enums import AuditCategory, FindingSource, Severity
    from codementor.models.findings import Finding

    def make(line: int, kind: str) -> Finding:
        return Finding(
            id=f"F-00{line}",
            rule_id=None,
            category=AuditCategory.DESIGN,
            severity=Severity.LOW,
            line_start=line,
            line_end=None,
            evidence="x",
            description=f"{kind} açıklaması",
            source=FindingSource.LLM,
            confidence=0.7,
            kind=kind,  # type: ignore[arg-type]
        )

    findings = app.analyze_view.findings
    findings.show([make(1, "issue"), make(2, "suggestion")], [])
    app.update()
    assert findings.count.cget("text") == "1"
    toggle = findings.suggestion_toggle
    assert toggle is not None
    assert toggle.cget("text") == "Öneriler (1) ▸"
    assert not findings.suggestion_body.grid_info()
    toggle.invoke()
    app.update()
    assert toggle.cget("text") == "Öneriler (1) ▾"
    assert findings.suggestion_body.grid_info()
    findings.show([make(1, "issue")], [])
    assert findings.suggestion_toggle is None


# --- Faz 60: geçmişte uyumsuz rapor --------------------------------------------------------


def test_open_history_missing_record_shows_not_found_toast(app: App) -> None:
    """Faz 60: Kayıt hiç yoksa 'Bu analiz artık bulunamıyor.' mesajı gösterilir."""
    open_and_wait(app, "01JNONEXISTENT9999999999999")
    assert "Bu analiz artık bulunamıyor." in _toast(app)


def test_open_history_incompatible_report_loads_code_and_clears_results(app: App) -> None:
    """Faz 60: Rapor şeması uyumsuzsa kod açılır, sonuçlar temizlenir ve uyarı toast'ı verilir."""
    analysis_id = "01J60TESTINCOMPATIBLE000001"
    row = AnalysisRow(
        id=analysis_id,
        created_at=datetime.now(UTC),
        cache_key="key_incompat_1",
        language="c",
        engine="standalone",
        question_id=None,
        session_id=None,
        provider="fake",
        model="fake",
        early_exit=False,
        degraded=False,
        tokens_in=10,
        tokens_out=20,
        latency_ms=100,
        report_json='{"bilinmeyen_veya_eski": "format"}',
    )
    db = app.core.database()
    with db.session() as session:
        session.add(row)
        session.commit()

    test_code = "int x = 42;\n"
    runtime.save_source(analysis_id, test_code, app.prefs_dir)

    open_and_wait(app, analysis_id)
    assert app.current_view == "analyze"
    assert app.analyze_view.editor.get() == test_code
    assert app.analyze_view.language == Language.C
    assert app.analyze_view.report is None
    assert "farklı bir CodeMentor sürümüyle" in _toast(app)


def test_open_history_incompatible_report_missing_source_falls_back(app: App) -> None:
    """Faz 60 Olumsuz test: Uyumsuz kaydın kodu saklanmamışsa 'kod saklanmamış' yazılır, çökmez."""
    analysis_id = "01J60TESTINCOMPATIBLE000002"
    row = AnalysisRow(
        id=analysis_id,
        created_at=datetime.now(UTC),
        cache_key="key_incompat_2",
        language="cpp",
        engine="standalone",
        question_id=None,
        session_id=None,
        provider="fake",
        model="fake",
        early_exit=False,
        degraded=False,
        tokens_in=10,
        tokens_out=20,
        latency_ms=100,
        report_json='{"eski": "sema"}',
    )
    db = app.core.database()
    with db.session() as session:
        session.add(row)
        session.commit()

    # Kaynak dosya kasıtlı olarak oluşturulmadı
    open_and_wait(app, analysis_id)
    assert app.current_view == "analyze"
    assert "saklanmamış" in app.analyze_view.editor.get()
    assert app.analyze_view.language == Language.CPP
    assert "farklı bir CodeMentor sürümüyle" in _toast(app)
