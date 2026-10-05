"""Tier 1: yerel derleyiciyle opsiyonel sözdizimi/tip denetimi (mimari §5.2.2-5.2.3, ADR-0009).

Akış: ayar kapalı mı → araç var mı → include koruması (C/C++) → stub (Unreal) → güvenli
alt süreç (yalnızca stdin) → tanı ayrıştırma → sınıflandırma. Hiçbir adım istisna
fırlatmaz; sorun olursa `SKIPPED` + kullanıcıya dönük uyarı döner ve sistem Tier 0 ile
devam eder.

Sınıflandırma (§5.2.4): kesin hata → `FAILED`; yalnızca uyarı → `WARNING`; temiz →
`PASSED`. Bulunamayan başlık ve Unreal stub kaynaklı hatalar uyarıya düşürülür.
"""

from __future__ import annotations

import re
import threading

from codementor.analysis.parsers import neutralize_unreal_macros
from codementor.config import ValidationSettings
from codementor.log import get_logger, scrub
from codementor.models.enums import MARKUP_LANGUAGES, CompilationStatus, Engine, Language
from codementor.models.findings import Diagnostic
from codementor.models.request import NormalizedCode
from codementor.models.validation import CompilerTool, SkipReason, Tier1Result, Toolchain
from codementor.validation.diagnostics import (
    is_missing_header,
    parse_compiler_output,
    parse_roslyn_output,
)
from codementor.validation.include_guard import check_includes
from codementor.validation.python_check import check_python
from codementor.validation.runner import ProcessLimits, ProcessResult, Runner, run_process
from codementor.validation.toolchain import get_toolchain

_COMMON_FLAGS = ("-fsyntax-only", "-Wall", "-Wextra", "-fno-diagnostics-color")
_STD = {Language.C: ("c", "-std=c17"), Language.CPP: ("c++", "-std=c++20")}
# `\` ile devam eden satırlar boşaltılmaz: birleştirme kopar, alt satır yönergeye dönüşürdü
_LOCAL_INCLUDE = re.compile(r'^[ \t]*#[ \t]*include[ \t]*"[^\n]*(?<![\\ \t\f\v])$', re.MULTILINE)
log = get_logger("codementor.validation")

_DOTNET_ENV = {
    "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
    "DOTNET_NOLOGO": "1",
    "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
    # Linux'ta W^X çift eşlemesi memfd'yi büyütür; POSIX RLIMIT_FSIZE (1 MB) bunu engeller ve
    # CoreCLR açılışta "Out Of Memory" ile düşer (Faz 27, CI'da görüldü). Roslyn kod çalıştırmaz,
    # yalnızca ayrıştırır; dosya boyutu sınırı korunur, W^X bu süreçte kapatılır
    "DOTNET_EnableWriteXorExecute": "0",
}
_TARGET_NAMES = {
    (Language.C, Engine.NONE): "C",
    (Language.CPP, Engine.NONE): "C++",
    (Language.CPP, Engine.UNREAL): "Unreal C++",
    (Language.CSHARP, Engine.NONE): "C#",
    (Language.CSHARP, Engine.UNITY): "Unity C#",
}
_MAX_REASONS_SHOWN = 3


def _skipped(reason: SkipReason, message: str, tool: str | None = None) -> Tier1Result:
    return Tier1Result(
        status=CompilationStatus.SKIPPED, tool=tool, skip_reason=reason, warnings=[message]
    )


def _blank_local_includes(text: str) -> str:
    """Unreal: `#include "..."` satırlarını aynı uzunlukta boşlukla değiştirir.

    Motor başlıkları (`CoreMinimal.h`, `*.generated.h`) yerel olarak yoktur; yerlerini stub tutar.
    """
    return _LOCAL_INCLUDE.sub(lambda m: " " * len(m.group()), text)


def _roslyn_env(memory_mb: int) -> dict[str, str]:
    # GC yığınını Job Object / bellek sınırının altında tut (onaltılık bayt)
    return {**_DOTNET_ENV, "DOTNET_GCHeapHardLimit": format(memory_mb * 1024 * 1024 * 3 // 4, "x")}


def _classify(
    diagnostics: list[Diagnostic], *, advisory: bool
) -> tuple[list[Diagnostic], list[str]]:
    """Eksik başlık ve (Unreal'da) tüm hataları uyarıya düşürür; kullanıcı notlarını üretir."""
    notes: list[str] = []
    result: list[Diagnostic] = []
    for diag in diagnostics:
        if diag.severity == "error" and is_missing_header(diag.message):
            notes.append(
                f"Satır {diag.line}: başlık dosyası bulunamadı; "
                "derleyici denetimi bu noktada durdu."
            )
            diag = diag.model_copy(update={"severity": "warning"})
        elif diag.severity == "error" and advisory:
            diag = diag.model_copy(update={"severity": "warning"})
        result.append(diag)
    if advisory and diagnostics:
        notes.append(
            "Unreal kodu gerçek motor başlıkları olmadan (stub ile) denetlendi; "
            "derleyici mesajları tavsiye niteliğindedir."
        )
    return result, notes


def _status(diagnostics: list[Diagnostic]) -> CompilationStatus:
    severities = {d.severity for d in diagnostics}
    if "error" in severities:
        return CompilationStatus.FAILED
    if "warning" in severities:
        return CompilationStatus.WARNING
    return CompilationStatus.PASSED


def _guard(text: str, tool: CompilerTool) -> Tier1Result | None:
    """Include koruması; bulgu varsa `SKIPPED` sonucu."""
    reasons = check_includes(text)
    if not reasons:
        return None
    shown = "; ".join(reasons[:_MAX_REASONS_SHOWN])
    return _skipped(
        SkipReason.INCLUDE_GUARD,
        f"Güvenlik nedeniyle derleyici denetimi atlandı ({shown}).",
        tool.name,
    )


def _command(
    tool: CompilerTool, code: NormalizedCode, settings: ValidationSettings
) -> tuple[list[str], str, ProcessLimits, dict[str, str]] | Tier1Result:
    """Çağrı bileşenleri; hazırlık başarısızsa `SKIPPED` sonucu."""
    limits = ProcessLimits(
        timeout_s=settings.compile_timeout_s,
        memory_mb=settings.compile_memory_mb,
        limit_address_space=tool.kind != "roslyn",
    )
    if tool.kind == "roslyn":
        return list(tool.command), code.text, limits, _roslyn_env(settings.compile_memory_mb)

    guarded = _guard(code.text, tool)
    if guarded is not None:
        return guarded
    x_lang, std = _STD[code.language]
    argv = [*tool.command, "-x", x_lang, std, *_COMMON_FLAGS]
    stdin = code.text
    if code.engine is Engine.UNREAL:
        stub = settings.stub_header
        if not stub.is_file():
            return _skipped(
                SkipReason.STUB_MISSING,
                "Unreal stub başlığı bulunamadı; derleyici denetimi atlandı.",
                tool.name,
            )
        argv += ["-include", str(stub.resolve())]
        # Tier 0 ile aynı ön işlem (`*_API`, yansıma makroları) + yerel include'lar;
        # hepsi aynı uzunlukta boşlukla: satır/kolon kaymaz
        stdin = _blank_local_includes(neutralize_unreal_macros(stdin))
        # derleyiciye giden son metin de denetlenir: dönüşüm yeni yönerge üretmemeli
        guarded = _guard(stdin, tool)
        if guarded is not None:
            return guarded
    return [*argv, "-"], stdin, limits, {}


def _interpret(
    tool: CompilerTool, outcome: ProcessResult, *, advisory: bool, timeout_s: int
) -> Tier1Result:
    if outcome.error is not None:
        return _skipped(
            SkipReason.TOOL_ERROR, "Derleyici başlatılamadı; denetim atlandı.", tool.name
        )
    if outcome.timed_out:
        return _skipped(
            SkipReason.TIMEOUT,
            f"Derleyici denetimi {timeout_s} saniyede bitmedi; atlandı.",
            tool.name,
        )
    try:
        if tool.kind == "roslyn":
            if outcome.returncode != 0:
                raise ValueError("Roslyn aracı hata koduyla çıktı")
            diagnostics, capped = parse_roslyn_output(outcome.stdout)
        else:
            diagnostics, capped = parse_compiler_output(outcome.stderr, tool.kind)
            if outcome.returncode != 0 and not any(d.severity == "error" for d in diagnostics):
                raise ValueError("derleyici tanısız hata koduyla çıktı")
    except ValueError:
        if tool.kind == "roslyn":
            # Operatör için teşhis (Faz 27): Roslyn hatası .NET çalışma zamanı mesajıdır, kaynak
            # kodu yankılamaz; gcc/clang stderr'i kod parçası içerebildiği için loglanmaz (§12)
            log.warning(
                "tier1_tool_error",
                tool=tool.name,
                returncode=outcome.returncode,
                stderr=scrub(outcome.stderr[:300]),
            )
        return _skipped(
            SkipReason.TOOL_ERROR,
            "Derleyici beklenmedik bir çıktı üretti; denetim atlandı.",
            tool.name,
        )
    diagnostics, notes = _classify(diagnostics, advisory=advisory)
    return Tier1Result(
        status=_status(diagnostics),
        tool=tool.name,
        diagnostics=diagnostics,
        warnings=notes,
        truncated=capped or outcome.truncated,
    )


def run_tier1(
    code: NormalizedCode,
    settings: ValidationSettings,
    *,
    toolchain: Toolchain | None = None,
    runner: Runner = run_process,
    cancel: threading.Event | None = None,
) -> Tier1Result:
    """Kodu uygun yerel derleyiciyle denetler; araç yoksa veya güvenli değilse `SKIPPED`.

    `cancel` set edilince derleyici süreci zaman aşımını beklemeden öldürülür (Faz 24).
    """
    if code.language in MARKUP_LANGUAGES:  # derleyici kavramı yok; uyarı da yok (ADR-0015)
        return Tier1Result(status=CompilationStatus.SKIPPED, skip_reason=SkipReason.NOT_APPLICABLE)
    if not settings.tier1_enabled:
        return _skipped(SkipReason.DISABLED, "Derleyici denetimi yapılandırmada kapalı.")
    if code.language is Language.PYTHON:
        return check_python(code)
    chain = toolchain if toolchain is not None else get_toolchain(settings)
    tool = chain.for_code(code.language, code.engine)
    if tool is None:
        target = _TARGET_NAMES.get((code.language, code.engine), code.language.value)
        return _skipped(
            SkipReason.TOOL_MISSING,
            f"{target} için yerel derleyici bulunamadı; yalnızca sözdizimi ağacı denetlendi.",
        )
    prepared = _command(tool, code, settings)
    if isinstance(prepared, Tier1Result):
        return prepared
    argv, stdin, limits, env = prepared
    try:
        outcome = runner(argv, stdin, limits, extra_env=env, cancel=cancel)
    except Exception as exc:  # runner sözleşmesi istisna fırlatmamak; yine de sistemi düşürme
        log.warning("tier1_runner_exception", tool=tool.kind, error=type(exc).__name__)
        outcome = ProcessResult(None, "", "", error="runner exception")
    return _interpret(
        tool,
        outcome,
        advisory=code.engine is Engine.UNREAL,
        timeout_s=settings.compile_timeout_s,
    )
