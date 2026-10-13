"""Paket duman testi (Faz D, O17): `CodeMentor.exe --self-check sonuc.json`.

Pencere açmadan exe'nin içindeki kaynakları ve çekirdeğin çalıştığını denetler; release iş akışı
derlenen exe'yi bununla sınar. Eksik `data/`, `prompts/` ya da tree-sitter sorguları (`.scm`)
uygulamayı sessizce bozar (Faz 50'de exe'de olgu çıkarımı boş kalmıştı): burada yakalanır.
LLM çağrılmaz, ağa çıkılmaz, veritabanı açılmaz.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import codementor.analysis.queries as queries_package
from codementor import __version__
from codementor.analysis.call_costs import load_call_costs
from codementor.analysis.extractor import extract_facts
from codementor.config import DEFAULT_CONFIG_FILE, Settings, load_settings
from codementor.ingest.normalize import normalize
from codementor.models.enums import Language
from codementor.models.request import LanguageHint
from codementor.paths import resource_root
from codementor.questions.bank import QuestionBank

SAMPLE_C = (
    "#include <stdlib.h>\n"
    "int sum(const int *v, int n) {\n"
    "    int s = 0;\n"
    "    for (int i = 0; i < n; i++) { s += v[i]; }\n"
    "    return s;\n"
    "}\n"
)
MIN_QUESTIONS = 64  # yerleşik banka (Faz 30)


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str
    required: bool = True


def _run(name: str, probe: Callable[[], tuple[bool, str]], required: bool = True) -> Check:
    try:
        ok, detail = probe()
    except Exception as exc:  # duman testi her denetimi raporlar, ilk hatada durmaz
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    return Check(name, ok, detail, required)


def _exists(path: Path) -> tuple[bool, str]:
    return path.exists(), str(path)


def _bank(settings: Settings) -> tuple[bool, str]:
    count = len(QuestionBank.load(settings.data.questions_dir))
    return count >= MIN_QUESTIONS, f"{count} soru"


def _queries() -> tuple[bool, str]:
    root = Path(queries_package.__file__).parent
    count = len(list(root.rglob("*.scm")))
    return count > 0, f"{count} sorgu dosyası ({root})"


def _facts(settings: Settings) -> tuple[bool, str]:
    code = normalize(SAMPLE_C, LanguageHint(language=Language.C))
    facts = extract_facts(code, costs=load_call_costs(settings.data.call_costs_file))
    return bool(facts.functions and facts.loops), (
        f"{len(facts.functions)} fonksiyon, {len(facts.loops)} döngü"
    )


def run_checks() -> list[Check]:
    """Tüm denetimler; yapılandırma okunamazsa yalnız o hata döner."""
    try:
        settings = load_settings()
    except Exception as exc:
        return [Check("yapılandırma", False, f"{type(exc).__name__}: {exc}")]
    root = resource_root()
    return [
        _run("kaynak kökü", lambda: _exists(root)),
        _run("varsayılan codementor.toml", lambda: _exists(root / DEFAULT_CONFIG_FILE)),
        _run("prompt şablonları", lambda: _exists(settings.prompts.dir)),
        _run("kontrol listeleri", lambda: _exists(settings.data.checklists_dir)),
        _run("soru bankası", lambda: _bank(settings)),
        _run("tree-sitter sorguları", _queries),
        _run("olgu çıkarımı (C)", lambda: _facts(settings)),
        # Roslyn denetleyicisi isteğe bağlı derlenir (make roslyn-check-sc); release'te zorunlu
        _run(
            "Roslyn denetleyicisi",
            lambda: _exists(settings.validation.roslyn_check_exe),
            required=False,
        ),
    ]


def self_check(out: Path) -> int:
    """Denetimleri koşar, JSON'u `out`'a yazar; zorunlu biri başarısızsa 1, değilse 0."""
    checks = run_checks()
    ok = all(c.ok for c in checks if c.required)
    payload = {
        "ok": ok,
        "version": __version__,
        "checks": [c.__dict__ for c in checks],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if ok else 1
