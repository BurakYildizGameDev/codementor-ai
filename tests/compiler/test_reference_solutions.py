"""Referans çözümler derleyiciden temiz geçer (Faz 30, `@pytest.mark.compiler`).

Çözümler `private/solutions/` altındadır ve depoda yoktur; dosyası olmayan sorular atlanır.
Araç olarak PATH'teki derleyiciler, indirilmiş zig ve Roslyn kullanılır (bkz. ADR-0018).
Unreal çözümleri stub başlıkla denetlenir; stub'ın tanımadığı motor türleri yalnızca uyarıdır
(ADR-0007), bu yüzden orada yalnızca Tier 0 ve 'derleme başarısız değil' aranır.
"""

from __future__ import annotations

import functools
import os
from pathlib import Path

import pytest

from codementor.config import ValidationSettings
from codementor.ingest.normalize import normalize
from codementor.models.enums import CompilationStatus, Engine
from codementor.models.questions import Question
from codementor.models.request import LanguageHint
from codementor.models.validation import Toolchain
from codementor.questions.bank import QuestionBank
from codementor.validation.tier0 import run_tier0
from codementor.validation.tier1 import run_tier1
from codementor.validation.toolchain import discover

pytestmark = pytest.mark.compiler

ROOT = Path(__file__).resolve().parents[2]
_EXE = ".exe" if os.name == "nt" else ""
SETTINGS = ValidationSettings(
    stub_header=ROOT / "data" / "stubs" / "ue_stubs.h",
    compile_timeout_s=60,
)
BANK = QuestionBank.load(ROOT / "data" / "questions")


@functools.cache
def _chain() -> Toolchain:
    return discover(
        os.environ.get("PATH", ""),
        ROOT / "tools" / "roslyn-check" / "out" / "RoslynCheck.dll",
        roslyn_exe=ROOT / "tools" / "roslyn-check" / "sc" / f"RoslynCheck{_EXE}",
        toolchain_dir=Path(
            os.environ.get("CODEMENTOR_TOOLCHAIN_DIR") or Path.home() / ".codementor" / "toolchain"
        ),
        probe_timeout_s=60,
    )


def _solution(question: Question) -> str:
    assert question.reference_solution_path is not None
    path = ROOT / question.reference_solution_path
    if not path.is_file():
        pytest.skip("referans çözüm yok (private/ depoda değil)")
    return path.read_text(encoding="utf-8")


@pytest.mark.parametrize("question", list(BANK), ids=lambda q: q.id)
def test_reference_solution_compiles_cleanly(question: Question) -> None:
    code = normalize(
        _solution(question), LanguageHint(language=question.language, engine=question.engine)
    )
    tier0 = run_tier0(code)
    assert not tier0.has_errors, [(d.line, d.message) for d in tier0.diagnostics]
    result = run_tier1(code, SETTINGS, toolchain=_chain())
    if result.skip_reason is not None:
        return  # derleyici yok ya da HTML/CSS: Tier 0 yeterli
    assert result.status is not CompilationStatus.FAILED, result.diagnostics
    if question.engine is not Engine.UNREAL:
        noisy = [d for d in result.diagnostics if d.severity in ("error", "warning")]
        assert not noisy, [(d.line, d.message) for d in noisy]
