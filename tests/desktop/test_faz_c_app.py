"""Faz C: masaüstünde kavram adı kuralı (Y6) ve yapılandırma konumu zinciri (Y8)."""

from __future__ import annotations

import contextlib
from collections.abc import Iterator
from pathlib import Path

import pytest

from codementor.api.state import ApiState
from codementor.config import CONFIG_FILE_ENV
from codementor.desktop import runtime
from codementor.desktop.app import App
from codementor.desktop.connections import KeyStore
from codementor.models.report import SocraticResult
from tests.desktop.test_app import _open


@pytest.fixture
def app(core: ApiState, prefs_dir: Path, store: KeyStore) -> Iterator[App]:
    yield from _open(core, prefs_dir, store)


def _card_texts(app: App) -> list[str]:
    texts: list[str] = []

    def walk(widget: object) -> None:
        for child in widget.winfo_children():  # type: ignore[attr-defined]
            with contextlib.suppress(Exception):  # çerçevelerin metni yok
                texts.append(str(child.cget("text")))
            walk(child)

    walk(app.analyze_view.socratic.body)
    return texts


def _socratic(revealed: bool) -> SocraticResult:
    return SocraticResult(
        key_flaw_concept="Serbest bırakılmış belleğe erişim" if revealed else "",
        hint_level=2 if revealed else 1,
        guiding_questions=["free'den sonra hangi alanı okuyorsun?"],
        next_step_hint=None,
        leak_check="passed",
        concept_revealed=revealed,
    )


def test_socratic_card_hides_concept_until_revealed(app: App) -> None:
    app.analyze_view.socratic.show(_socratic(revealed=False))
    texts = _card_texts(app)
    assert "Mentor soruları" in texts
    assert not any("Serbest bırakılmış" in t for t in texts)
    app.analyze_view.socratic.show(_socratic(revealed=True))
    assert "Serbest bırakılmış belleğe erişim" in _card_texts(app)


def test_old_report_concept_hidden_without_flag(app: App) -> None:
    """Bayraksız eski rapor (geçmiş/önbellek) kavramı göstermez: varsayılan güvenli taraf."""
    old = SocraticResult.model_validate(
        {
            "key_flaw_concept": "Gizli kavram",
            "hint_level": 1,
            "guiding_questions": ["?"],
            "next_step_hint": None,
            "leak_check": "passed",
        }
    )
    app.analyze_view.socratic.show(old)
    assert "Gizli kavram" not in _card_texts(app)


def test_write_reload_and_location_use_same_file(
    app: App, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Y8: toml'suz kurulumda yazılan dosya etkinleşir; yeniden yükleme ve gösterilen konum o."""
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)
    bundle = tmp_path / "meipass"
    bundle.mkdir()
    (bundle / "codementor.toml").write_text('[providers]\ndefault = "ollama"\n', "utf-8")
    exe_dir = tmp_path / "uygulama"
    exe_dir.mkdir()
    monkeypatch.setattr(runtime, "is_frozen", lambda: True)
    monkeypatch.setattr(runtime, "resource_root", lambda: bundle)
    monkeypatch.setattr("sys.executable", str(exe_dir / "CodeMentor.exe"))
    app.connections.check = lambda _name: None  # type: ignore[method-assign]
    app.connections.make_default("gemini")
    app.write_config()
    written = exe_dir / "codementor.toml"
    assert 'default = "gemini"' in written.read_text(encoding="utf-8")
    app.reload_config()
    assert app.base_settings.providers.default == "gemini"
    locations = dict(app._locations())
    assert Path(locations["Yapılandırma"]) == written.resolve()
