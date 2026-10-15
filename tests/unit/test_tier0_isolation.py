"""Tier 0 ayrıştırmasının alt süreçte yalıtılması (Faz 59, ADR-0025).

Gerçek alt süreç açan testler yavaştır (Windows'ta süreç başına ~1 sn); sayıları az tutulur.
Hata yolları sahte çalıştırıcıyla denenir.
"""

from __future__ import annotations

import io
import sys
import time

import pytest
from pydantic import ValidationError

from codementor.config import ValidationSettings
from codementor.ingest.normalize import normalize
from codementor.models.enums import Language
from codementor.models.findings import Diagnostic
from codementor.models.request import LanguageHint, NormalizedCode
from codementor.models.validation import Tier0Result
from codementor.validation import tier0_isolation, tier0_worker
from codementor.validation.runner import ProcessLimits, ProcessResult
from codementor.validation.tier0 import run_tier0
from codementor.validation.tier0_isolation import (
    FAILURE_MESSAGE,
    INFRA_MESSAGE,
    TIMEOUT_MESSAGE,
    check_syntax,
    stopped,
)


def _code(text: str, language: Language = Language.C) -> NormalizedCode:
    return normalize(text, LanguageHint(language=language))


def _isolated(**overrides: object) -> ValidationSettings:
    return ValidationSettings.model_validate({"tier0_isolation": True, **overrides})


def _fake(result: ProcessResult, seen: list[ProcessLimits] | None = None) -> object:
    def run(argv: list[str], stdin: str, limits: ProcessLimits) -> ProcessResult:
        if seen is not None:
            seen.append(limits)
        return result

    return run


# ---------------------------------------------------------------- gerçek alt süreç


@pytest.mark.parametrize(
    ("text", "language"),
    [
        ("int main(void) {\n    int x = 1\n    return x;\n}\n", Language.C),
        ("int main(void) { return 0; }\n", Language.C),
        ("def f(:\n    pass\n", Language.PYTHON),
        ("<div>\n<p>Merhaba</p>\n", Language.HTML),
        # Türkçe karakter (kolon karakter cinsinden) ve tanı üst sınırı (`truncated`)
        ('const char *s = "çğışöü"; int ğ = 1\nint y = 2;\n', Language.C),
        ("int main(void) {\n" + "    int x = 1\n" * 40 + "    return 0;\n}\n", Language.C),
    ],
    ids=["c-missing-semicolon", "c-valid", "python-error", "html", "turkish", "truncated"],
)
def test_isolated_result_matches_in_process(text: str, language: Language) -> None:
    code = _code(text, language)
    assert check_syntax(code, _isolated()) == run_tier0(code)


_CSHARP_BOMB = "a<" * 20000  # ADR-0024: süreç içinde ~10-12 sn ve ~4,2 GB bellek


def test_pathological_csharp_hits_memory_cap() -> None:
    """Varsayılan 1024 MB sınırında işçi süre dolmadan ölür; analiz güvenle durur."""
    code = _code(_CSHARP_BOMB, Language.CSHARP)
    start = time.perf_counter()
    result = check_syntax(code, _isolated(tier0_timeout_s=5))
    assert time.perf_counter() - start < 5 + 3  # bellek ya da süre sınırı + süreç payı
    (diagnostic,) = result.diagnostics
    assert diagnostic.severity == "error"  # erken çıkış: statik aşama yeniden ayrıştırmaz
    assert diagnostic.message in (FAILURE_MESSAGE, TIMEOUT_MESSAGE.format(seconds=5))
    assert stopped(result)


def test_pathological_csharp_is_cut_at_timeout() -> None:
    """Bellek bol olsa da süre sınırında süreç ağacı öldürülür."""
    code = _code(_CSHARP_BOMB, Language.CSHARP)
    start = time.perf_counter()
    result = check_syntax(code, _isolated(tier0_timeout_s=1, tier0_memory_mb=8192))
    assert time.perf_counter() - start < 6  # süreç açma + 1 sn sınır + öldürme payı
    (diagnostic,) = result.diagnostics
    assert (diagnostic.severity, diagnostic.message) == ("error", TIMEOUT_MESSAGE.format(seconds=1))


# ---------------------------------------------------------------- yönlendirme ve hata yolları


def test_disabled_by_default_runs_in_process(monkeypatch: pytest.MonkeyPatch) -> None:
    assert ValidationSettings().tier0_isolation is False

    def boom(*_args: object, **_kwargs: object) -> ProcessResult:
        raise AssertionError("alt süreç açılmamalı")

    monkeypatch.setattr(tier0_isolation, "run_process", boom)
    code = _code("int main(void) { return 0 }\n")
    assert check_syntax(code, ValidationSettings()) == run_tier0(code)


def test_frozen_exe_falls_back_to_in_process(monkeypatch: pytest.MonkeyPatch) -> None:
    """Exe'de `python -m` yok; yalıtım açık olsa da süreç içinde koşulur (ADR-0025)."""
    monkeypatch.setattr(tier0_isolation, "is_frozen", lambda: True)
    monkeypatch.setattr(
        tier0_isolation, "run_process", _fake(ProcessResult(None, "", "", error="olmamalı"))
    )
    code = _code("int main(void) { return 0 }\n")
    assert check_syntax(code, _isolated()) == run_tier0(code)


def test_limits_come_from_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[ProcessLimits] = []
    ok = Tier0Result(diagnostics=[]).model_dump_json()
    monkeypatch.setattr(tier0_isolation, "run_process", _fake(ProcessResult(0, ok, ""), seen))
    check_syntax(_code("int x;\n"), _isolated(tier0_timeout_s=2.5, tier0_memory_mb=256))
    (limits,) = seen
    assert (limits.timeout_s, limits.memory_mb) == (2.5, 256)


@pytest.mark.parametrize(
    "result",
    [
        ProcessResult(3, "", "Segmentation fault"),
        ProcessResult(0, "{bozuk json", ""),
        ProcessResult(0, '{"diagnostics": []}', "", truncated=True),
        ProcessResult(None, "", "", cancelled=True),
    ],
    ids=["crash", "bad-json", "truncated", "cancelled"],
)
def test_worker_failure_fails_closed(
    monkeypatch: pytest.MonkeyPatch, result: ProcessResult
) -> None:
    """Alt süreç çökse ya da bozuk çıktı verse de ana süreç çökmez, analiz güvenle durur."""
    monkeypatch.setattr(tier0_isolation, "run_process", _fake(result))
    result = check_syntax(_code("int x;\n"), _isolated())
    (diagnostic,) = result.diagnostics
    assert (diagnostic.severity, diagnostic.message) == ("error", FAILURE_MESSAGE)
    assert stopped(result)


def test_timeout_result_uses_timeout_message(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        tier0_isolation, "run_process", _fake(ProcessResult(None, "", "", timed_out=True))
    )
    (diagnostic,) = check_syntax(_code("int x;\n"), _isolated(tier0_timeout_s=3)).diagnostics
    assert diagnostic.message == TIMEOUT_MESSAGE.format(seconds=3)


def test_worker_argv_is_absolute_python_module() -> None:
    argv = tier0_isolation.worker_argv()
    assert argv[0] == sys.executable
    assert argv[-2:] == ["-m", "codementor.validation.tier0_worker"]


def test_worker_main_round_trip(monkeypatch: pytest.MonkeyPatch) -> None:
    """İşçi stdin'den `NormalizedCode` okur, stdout'a `Tier0Result` yazar (süreç içinde)."""
    code = _code("int main(void) {\n    int x = 1\n")
    # Windows borusu gibi yerel kod sayfalı metin katmanı: işçi baytları UTF-8 kullanmalı
    stdin = io.TextIOWrapper(io.BytesIO(code.model_dump_json().encode("utf-8")), "cp1252")
    raw = io.BytesIO()
    stdout = io.TextIOWrapper(raw, "cp1252")
    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "stdout", stdout)
    assert tier0_worker.main() == 0
    result = Tier0Result.model_validate_json(raw.getvalue().decode("utf-8"))
    assert result == run_tier0(code)
    assert any("ı" in d.message for d in result.diagnostics)  # Türkçe karakter bozulmadı


# ---------------------------------------------------------------- denetim düzeltmeleri


def test_launch_error_does_not_blame_student_code(monkeypatch: pytest.MonkeyPatch) -> None:
    """Denetim Ö2: alt süreç hiç başlamadıysa mesaj kodu değil yapılandırmayı işaret eder."""
    failed = ProcessResult(None, "", "", error="çalıştırılabilir bulunamadı")
    monkeypatch.setattr(tier0_isolation, "run_process", _fake(failed))
    result = check_syntax(_code("int x;\n"), _isolated())
    (diagnostic,) = result.diagnostics
    assert (diagnostic.severity, diagnostic.message) == ("error", INFRA_MESSAGE)
    assert "kodunla ilgili değil" in diagnostic.message
    assert stopped(result)


def test_memory_floor_rejects_unusable_limit() -> None:
    """Denetim Ö2: Linux'ta `RLIMIT_AS` 64 MB'ta Python bile açılmaz; alt sınır 256."""
    with pytest.raises(ValidationError):
        ValidationSettings.model_validate({"tier0_memory_mb": 128})


def test_regular_tier0_errors_are_not_stops() -> None:
    assert not stopped(run_tier0(_code("int main(void) { return 0 }\n")))


def test_stopped_flag_is_structural_not_textual() -> None:
    """D18: durdurma kararı bayraktan gelir; tanı metni değişse de `durduruldu` kalır."""
    changed = Tier0Result(
        diagnostics=[_syntax_error("Kodun sözdizimi denetimi başka bir metinle anlatıldı")],
        stopped=True,
    )
    assert stopped(changed)
    assert not stopped(Tier0Result(diagnostics=[_syntax_error("beklenmeyen '}' simgesi")]))
    # işçi süreci sınırından geçerken (JSON) bayrak korunur
    assert stopped(Tier0Result.model_validate_json(changed.model_dump_json()))
    # `_stopped` tek durdurma üreticisi: bayrağı kendisi koyar
    assert tier0_isolation._stopped("herhangi bir metin").stopped


def _syntax_error(message: str) -> Diagnostic:
    return Diagnostic(tool="tree-sitter", severity="error", line=1, column=None, message=message)


def test_failure_log_omits_user_code(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Denetim küçük 3: stderr/stdout kullanıcı kodundan parça taşıyabilir; loga girmez."""
    leak = "input_value={'text': 'GIZLI_KULLANICI_KODU " + "x" * 300 + "'}\nValidationError"
    for result in (ProcessResult(1, "", leak), ProcessResult(0, "GIZLI_KULLANICI_KODU{", "")):
        monkeypatch.setattr(tier0_isolation, "run_process", _fake(result))
        check_syntax(_code("int x;\n"), _isolated())
    assert "GIZLI_KULLANICI_KODU" not in capsys.readouterr().err
