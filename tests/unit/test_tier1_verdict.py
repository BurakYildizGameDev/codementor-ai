"""Tier 1 sonuç sınıflandırma + güvenlik/kolon regresyon testleri (sahte runner ile).

Bölme (Faz J5, denetim Küçük-5): `tests/unit/test_tier1.py`'den (633 satır) taşındı; vaka adları ve
iddialar değişmedi.
- Atlama yolları + çağrı biçimi: `tests/unit/test_tier1.py`
- Ortak düzenek: `tests/unit/tier1_helpers.py`
"""

from __future__ import annotations

import threading
from collections.abc import Callable, Mapping, Sequence
from typing import Any

import pytest

from codementor.models.enums import CompilationStatus, Engine, Language
from codementor.models.validation import CompilerTool, SkipReason, Toolchain
from codementor.validation.runner import ProcessLimits, ProcessResult
from codementor.validation.tier1 import run_tier1
from tests.unit.tier1_helpers import (
    C_CODE,
    CPP_CODE,
    CS_CODE,
    FULL,
    SETTINGS,
    UNREAL_CODE,
    FakeRunner,
    normalize_code,
    read_stderr,
)

# ------------------------------------------------------------------ sonuç sınıflandırma


def test_c_type_error_failed() -> None:
    runner = FakeRunner(ProcessResult(1, "", read_stderr("gcc_c_type_error.txt")))
    result = run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.FAILED
    assert result.tool == "gcc"
    assert [(d.line, d.severity) for d in result.diagnostics][:2] == [(3, "error"), (4, "warning")]
    assert all(d.tool == "gcc" for d in result.diagnostics)


def test_clang_cpp_error_failed() -> None:
    chain = Toolchain(cpp=CompilerTool(name="clang++", kind="clang", command=["/c++"]))
    runner = FakeRunner(ProcessResult(1, "", read_stderr("clang_cpp_type_error.txt")))
    result = run_tier1(
        normalize_code(CPP_CODE, Language.CPP), SETTINGS, toolchain=chain, runner=runner
    )
    assert result.status is CompilationStatus.FAILED
    assert all(d.tool == "clang" for d in result.diagnostics)


def test_warnings_only_warning() -> None:
    stderr = "<stdin>:3:9: warning: unused variable 'x' [-Wunused-variable]\n"
    runner = FakeRunner(ProcessResult(0, "", stderr))
    result = run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.WARNING
    assert result.diagnostics[0].severity == "warning"


def test_clean_passed() -> None:
    runner = FakeRunner(ProcessResult(0, "", ""))
    result = run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.PASSED
    assert result.diagnostics == []
    assert result.skip_reason is None


@pytest.mark.parametrize("sample", ["gcc_missing_header.txt", "clang_missing_header.txt"])
def test_missing_local_header_is_warning(sample: str) -> None:
    runner = FakeRunner(ProcessResult(1, "", read_stderr(sample)))
    code = normalize_code('#include "WaveSpawner.h"\nint main() { return 0; }\n', Language.CPP)
    result = run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.WARNING
    assert [d.severity for d in result.diagnostics] == ["warning"]
    assert result.warnings


def test_unreal_errors_demoted_to_warning() -> None:
    runner = FakeRunner(ProcessResult(1, "", read_stderr("clang_unreal_stub.txt")))
    code = normalize_code(UNREAL_CODE, Language.CPP, Engine.UNREAL)
    result = run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.WARNING
    assert result.diagnostics
    assert all(d.severity != "error" for d in result.diagnostics)
    assert result.warnings


def test_unreal_clean_passed() -> None:
    runner = FakeRunner(ProcessResult(0, "", ""))
    code = normalize_code(UNREAL_CODE, Language.CPP, Engine.UNREAL)
    assert run_tier1(code, SETTINGS, toolchain=FULL, runner=runner).status in (
        CompilationStatus.PASSED,
        CompilationStatus.WARNING,
    )


def test_roslyn_error_failed() -> None:
    runner = FakeRunner(ProcessResult(0, read_stderr("roslyn_errors.json"), ""))
    result = run_tier1(
        normalize_code(CS_CODE, Language.CSHARP), SETTINGS, toolchain=FULL, runner=runner
    )
    assert result.status is CompilationStatus.FAILED
    assert result.diagnostics[0].tool == "roslyn"


@pytest.mark.parametrize(
    "result", [ProcessResult(0, "not json", ""), ProcessResult(2, "[]", "boom")]
)
def test_roslyn_bad_output_skipped(result: ProcessResult) -> None:
    out = run_tier1(
        normalize_code(CS_CODE, Language.CSHARP),
        SETTINGS,
        toolchain=FULL,
        runner=FakeRunner(result),
    )
    assert out.status is CompilationStatus.SKIPPED
    assert out.skip_reason is SkipReason.TOOL_ERROR


def test_roslyn_tool_error_logged_for_operator(
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    """Faz 27: Roslyn aracı düşerse çıkış kodu ve stderr başı log'a (teşhis); gcc'de değil."""
    host_error = "You must install or update .NET to run this application."
    runner = FakeRunner(ProcessResult(150, "", host_error))
    run_tier1(normalize_code(CS_CODE, Language.CSHARP), SETTINGS, toolchain=FULL, runner=runner)
    event = next(e for e in captured_logs() if e["event"] == "tier1_tool_error")
    assert event["returncode"] == 150
    assert host_error in event["stderr"]

    gcc = FakeRunner(ProcessResult(1, "", "int gizli_kod_satiri;"))
    run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=gcc)
    assert sum(e["event"] == "tier1_tool_error" for e in captured_logs()) == 1


def test_truncated_output_flagged() -> None:
    stderr = "<stdin>:3:13: error: bad\n"
    runner = FakeRunner(ProcessResult(1, "", stderr, truncated=True))
    result = run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.truncated
    assert result.status is CompilationStatus.FAILED


def test_never_raises_on_runner_exception(
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    def broken(*_args: object, **_kwargs: object) -> ProcessResult:
        raise OSError("disk dolu")

    result = run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=broken)
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.TOOL_ERROR
    # Faz 48: sessiz geçilmez, istisna türü loglanır
    logs = [e for e in captured_logs() if e["event"] == "tier1_runner_exception"]
    assert [e["error"] for e in logs] == ["OSError"]


# ------------------------------------------------------------------ güvenlik denetimi regresyonları


@pytest.mark.parametrize(
    "prefix",
    [
        "UCLASS()#include </etc/passwd>\n",
        "X_API #import </etc/passwd>\n",
        '#include "a.h" \\\n#include </etc/passwd>\n',
        '#include "a.h" \\\n#pragma GCC dependency "/etc/passwd"\n',
    ],
)
def test_unreal_transform_cannot_create_directive(prefix: str) -> None:
    runner = FakeRunner()
    code = normalize_code(prefix + UNREAL_CODE, Language.CPP, Engine.UNREAL)
    result = run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    assert result.skip_reason is SkipReason.INCLUDE_GUARD
    assert runner.calls == []


def test_unreal_continued_include_line_not_blanked() -> None:
    from codementor.validation.tier1 import _blank_local_includes

    text = '#include "a.h" \\\nint x;\n#include "b.h"\n'
    out = _blank_local_includes(text)
    assert out.startswith('#include "a.h" \\\n')
    assert '"b.h"' not in out
    assert len(out) == len(text)


def test_runner_receives_cancel_event() -> None:
    runner = FakeRunner()
    cancel = threading.Event()
    run_tier1(
        normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner, cancel=cancel
    )
    assert runner.cancels == [cancel]


# ---------------------------------------------------- kolon birimi: bayt (Faz H3)


def test_c_argv_uses_byte_columns() -> None:
    """gcc'nin `display` birimi yerine bayt seçilir: iki derleyici aynı birimi kullanır."""
    runner = FakeRunner()
    run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    ((argv, *_),) = [runner.calls[0]]
    assert "-fdiagnostics-column-unit=byte" in argv
    assert argv[-1] == "-"  # stdin göstergesi sonda kalır


def test_unsupported_column_unit_is_retried_without_flag() -> None:
    """Eski gcc bayrağı tanımazsa ikinci kez bayraksız çalıştırılır (denetim atlanmaz)."""
    results = [
        ProcessResult(
            1, "", "gcc: error: unrecognized command-line option '-fdiagnostics-column-unit=byte'\n"
        ),
        ProcessResult(1, "", "<stdin>:3:5: error: 'x' undeclared\n"),
    ]
    calls: list[list[str]] = []

    def runner(
        argv: Sequence[str],
        stdin: str,
        limits: ProcessLimits,
        *,
        extra_env: Mapping[str, str] | None = None,
        cancel: threading.Event | None = None,
    ) -> ProcessResult:
        calls.append(list(argv))
        return results[len(calls) - 1]

    result = run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert len(calls) == 2
    assert "-fdiagnostics-column-unit=byte" in calls[0]
    assert "-fdiagnostics-column-unit=byte" not in calls[1]
    assert result.status is CompilationStatus.FAILED
    assert [d.line for d in result.diagnostics] == [3]


@pytest.mark.parametrize(
    "outcome",
    [
        ProcessResult(0, "", ""),  # başarılı: yeniden deneme yok
        ProcessResult(1, "", "<stdin>:2:1: error: beklenmeyen\n"),  # bayrak anılmıyor
        ProcessResult(None, "", "", error="runner exception"),
        ProcessResult(1, "", "", timed_out=True),
    ],
)
def test_no_retry_without_flag_complaint(outcome: ProcessResult) -> None:
    runner = FakeRunner(outcome)
    run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert len(runner.calls) == 1


def test_roslyn_env_keeps_fsize_limit_compatible() -> None:
    """Faz 27: Linux'ta RLIMIT_FSIZE altında CoreCLR açılabilsin (W^X kapalı, GC sınırlı)."""
    runner = FakeRunner()
    run_tier1(normalize_code(CS_CODE, Language.CSHARP), SETTINGS, toolchain=FULL, runner=runner)
    _argv, _stdin, limits, env = runner.calls[0]
    assert env["DOTNET_EnableWriteXorExecute"] == "0"
    assert "DOTNET_GCHeapHardLimit" in env
    assert not limits.limit_address_space


def test_zig_argv_reads_stdin_only() -> None:
    """Zig (Faz 29): `zig clang` + sonda bayrakları; kod yalnız stdin'den, diske yazılmaz."""
    zig = CompilerTool(
        name="zig",
        kind="clang",
        command=[
            "/tc/zig/zig",
            "clang",
            "--target=x86_64-linux-gnu",
            "-nostdinc",
            "-isystem",
            "/tc/zig/lib/include",
        ],
        origin="downloaded",
    )
    runner = FakeRunner(ProcessResult(1, "", read_stderr("zig_clang_cpp_crlf.txt")))
    code = normalize_code(CPP_CODE, Language.CPP)
    result = run_tier1(code, SETTINGS, toolchain=Toolchain(cpp=zig), runner=runner)
    ((argv, stdin, _, env),) = runner.calls
    assert argv[:2] == ["/tc/zig/zig", "clang"]
    assert argv[-1] == "-"
    assert "cc" not in argv
    assert "c++" not in argv[:2]
    assert stdin == code.text
    assert "ZIG_GLOBAL_CACHE_DIR" not in env  # zig clang önbellek dizini istemez
    assert result.status is CompilationStatus.FAILED
    assert result.tool == "zig"
