"""Tier 1 orkestrasyon testleri: sahte runner ve sahte araç zinciriyle (derleyicisiz)."""

from __future__ import annotations

import threading
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from codementor.config import ValidationSettings
from codementor.ingest.normalize import normalize
from codementor.models.enums import CompilationStatus, Engine, Language
from codementor.models.request import LanguageHint, NormalizedCode
from codementor.models.validation import CompilerTool, SkipReason, Toolchain
from codementor.validation.runner import ProcessLimits, ProcessResult
from codementor.validation.tier1 import run_tier1

SAMPLES = Path(__file__).resolve().parents[1] / "fixtures" / "tier1"
STUB = Path(__file__).resolve().parents[2] / "data" / "stubs" / "ue_stubs.h"

GCC = CompilerTool(name="gcc", kind="gcc", command=["/usr/bin/gcc"])
GXX = CompilerTool(name="g++", kind="gcc", command=["/usr/bin/g++"])
CLANGXX = CompilerTool(name="clang++", kind="clang", command=["/usr/bin/clang++"])
ROSLYN = CompilerTool(name="roslyn-check", kind="roslyn", command=["/usr/bin/dotnet", "/x.dll"])
FULL = Toolchain(c=GCC, cpp=GXX, unreal=CLANGXX, csharp=ROSLYN)


@dataclass
class FakeRunner:
    """`run_process` yerine geçer; çağrıları kaydeder, hazır sonuç döndürür."""

    result: ProcessResult = field(default_factory=lambda: ProcessResult(0, "", ""))
    calls: list[tuple[list[str], str, ProcessLimits, dict[str, str]]] = field(default_factory=list)
    cancels: list[threading.Event | None] = field(default_factory=list)

    def __call__(
        self,
        argv: Sequence[str],
        stdin: str,
        limits: ProcessLimits,
        *,
        extra_env: Mapping[str, str] | None = None,
        cancel: threading.Event | None = None,
    ) -> ProcessResult:
        self.cancels.append(cancel)
        self.calls.append((list(argv), stdin, limits, dict(extra_env or {})))
        return self.result


def _code(text: str, language: Language, engine: Engine = Engine.NONE) -> NormalizedCode:
    return normalize(text, LanguageHint(language=language, engine=engine))


C_CODE = "#include <stdio.h>\nint main(void) {\n    int x = 1;\n    return x;\n}\n"
CPP_CODE = "#include <vector>\nint main() {\n    std::vector<int> v;\n    return 0;\n}\n"
CS_CODE = "class A {\n    void F() { int x = 1; }\n}\n"
UNREAL_CODE = (
    '#include "Enemy.h"\n'
    '#include "Enemy.generated.h"\n'
    "UCLASS()\n"
    "class AEnemy : public AActor {\n"
    "    GENERATED_BODY()\n"
    "    UPROPERTY() int32 Health = 100;\n"
    "};\n"
)
SETTINGS = ValidationSettings(stub_header=STUB)


def _stderr(name: str) -> str:
    return (SAMPLES / name).read_text(encoding="utf-8")


# ------------------------------------------------------------------ atlama yolları


def test_disabled_skips_with_zero_calls() -> None:
    runner = FakeRunner()
    result = run_tier1(
        _code(C_CODE, Language.C),
        ValidationSettings(tier1_enabled=False),
        toolchain=FULL,
        runner=runner,
    )
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.DISABLED
    assert runner.calls == []


@pytest.mark.parametrize(
    ("text", "language", "engine"),
    [
        (C_CODE, Language.C, Engine.NONE),
        (CPP_CODE, Language.CPP, Engine.NONE),
        (UNREAL_CODE, Language.CPP, Engine.UNREAL),
        (CS_CODE, Language.CSHARP, Engine.NONE),
        (CS_CODE, Language.CSHARP, Engine.UNITY),
    ],
)
def test_missing_tool_skipped_with_warning(text: str, language: Language, engine: Engine) -> None:
    runner = FakeRunner()
    result = run_tier1(
        _code(text, language, engine), SETTINGS, toolchain=Toolchain(), runner=runner
    )
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.TOOL_MISSING
    assert result.warnings
    assert runner.calls == []


@pytest.mark.parametrize(
    ("text", "language", "engine"),
    [
        ('#include "/etc/shadow"\nint main(void) { return 0; }\n', Language.C, Engine.NONE),
        ("#include <../../etc/passwd>\nint main() {}\n", Language.CPP, Engine.NONE),
        ('#embed "x.bin"\nint main(void) { return 0; }\n', Language.C, Engine.NONE),
        ("#if __has_include(<x>)\n#endif\nint main() {}\n", Language.CPP, Engine.NONE),
        ("#define H </etc/passwd>\n#include H\nint main() {}\n", Language.CPP, Engine.NONE),
        ('#include "C:\\\\x.h"\n' + UNREAL_CODE, Language.CPP, Engine.UNREAL),
    ],
)
def test_include_guard_skips_with_zero_calls(text: str, language: Language, engine: Engine) -> None:
    runner = FakeRunner()
    result = run_tier1(_code(text, language, engine), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.INCLUDE_GUARD
    assert result.warnings
    assert runner.calls == []


def test_missing_stub_skipped(tmp_path: Path) -> None:
    runner = FakeRunner()
    settings = ValidationSettings(stub_header=tmp_path / "yok.h")
    result = run_tier1(
        _code(UNREAL_CODE, Language.CPP, Engine.UNREAL), settings, toolchain=FULL, runner=runner
    )
    assert result.skip_reason is SkipReason.STUB_MISSING
    assert runner.calls == []


def test_timeout_skipped() -> None:
    runner = FakeRunner(ProcessResult(None, "", "", timed_out=True))
    result = run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.TIMEOUT
    assert result.warnings


def test_launch_error_skipped() -> None:
    runner = FakeRunner(ProcessResult(None, "", "", error="FileNotFoundError"))
    result = run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.skip_reason is SkipReason.TOOL_ERROR


def test_crash_without_diagnostics_skipped() -> None:
    runner = FakeRunner(ProcessResult(-11, "", "Segmentation fault\n"))
    result = run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.TOOL_ERROR


# ------------------------------------------------------------------ çağrı biçimi


def test_argv_stdin_only_no_include_paths() -> None:
    runner = FakeRunner()
    code = _code(C_CODE, Language.C)
    run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    ((argv, stdin, limits, _),) = runner.calls
    assert argv[0] == "/usr/bin/gcc"
    assert argv[-1] == "-"
    assert argv[argv.index("-x") + 1] == "c"
    assert "-fsyntax-only" in argv
    assert "-std=c17" in argv
    assert not any(a.startswith(("-I", "-iquote", "-isystem", "-idirafter", "-o")) for a in argv)
    assert "-include" not in argv
    assert stdin == code.text
    assert limits.timeout_s == SETTINGS.compile_timeout_s
    assert limits.memory_mb == SETTINGS.compile_memory_mb


def test_cpp_argv() -> None:
    runner = FakeRunner()
    run_tier1(_code(CPP_CODE, Language.CPP), SETTINGS, toolchain=FULL, runner=runner)
    argv = runner.calls[0][0]
    assert argv[0] == "/usr/bin/g++"
    assert argv[argv.index("-x") + 1] == "c++"
    assert "-std=c++20" in argv


def test_unreal_argv_has_stub_and_local_includes_blanked() -> None:
    runner = FakeRunner()
    code = _code(UNREAL_CODE, Language.CPP, Engine.UNREAL)
    run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    ((argv, stdin, _, _),) = runner.calls
    assert argv[0] == "/usr/bin/clang++"
    assert argv[argv.index("-include") + 1] == str(STUB.resolve())
    assert argv[-1] == "-"
    assert not any(a.startswith("-I") for a in argv)
    # satır ve kolonlar kaymaz; yalnızca yerel include satırları boşaltılır
    assert len(stdin) == len(code.text)
    assert stdin.count("\n") == code.text.count("\n")
    assert "#include" not in stdin
    # Tier 0 ile aynı makro nötrleştirme: yansıma makroları gider, kod yerinde kalır
    lines = stdin.split("\n")
    assert "UCLASS" not in stdin
    assert "GENERATED_BODY" not in stdin
    assert lines[3] == "class AEnemy : public AActor {"
    assert lines[5].strip() == "int32 Health = 100;"
    assert lines[5].index("int32") == code.text.split("\n")[5].index("int32")


def test_unreal_api_macro_neutralized() -> None:
    runner = FakeRunner()
    text = "class MYGAME_API AFoo : public AActor {\n};\n"
    run_tier1(_code(text, Language.CPP, Engine.UNREAL), SETTINGS, toolchain=FULL, runner=runner)
    stdin = runner.calls[0][1]
    assert "MYGAME_API" not in stdin
    assert stdin.index("AFoo") == text.index("AFoo")


def test_unreal_keeps_system_includes() -> None:
    runner = FakeRunner()
    code = _code("#include <vector>\n" + UNREAL_CODE, Language.CPP, Engine.UNREAL)
    run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    assert runner.calls[0][1].startswith("#include <vector>\n")


def test_roslyn_argv_and_env() -> None:
    runner = FakeRunner(ProcessResult(0, "[]", ""))
    code = _code(CS_CODE, Language.CSHARP, Engine.UNITY)
    result = run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    ((argv, stdin, limits, env),) = runner.calls
    assert argv == ["/usr/bin/dotnet", "/x.dll"]
    assert stdin == code.text
    assert not limits.limit_address_space
    assert env["DOTNET_CLI_TELEMETRY_OPTOUT"] == "1"
    assert "DOTNET_GCHeapHardLimit" in env
    assert result.status is CompilationStatus.PASSED
    assert result.tool == "roslyn-check"


def test_user_code_never_written_to_disk() -> None:
    """Gerçek runner ile: argv'de kod yok, geçici dizin boş kalıyor."""
    import sys

    from codementor.validation.runner import run_process

    marker = "USER_CODE_MARKER_91a7"
    probe = (
        "import os, sys, json; data = sys.stdin.read();"
        "print(json.dumps([os.listdir('.'), sys.argv]))"
    )
    fake = CompilerTool(name="gcc", kind="gcc", command=[sys.executable, "-c", probe])
    captured: list[ProcessResult] = []

    def spy(
        argv: Sequence[str],
        stdin: str,
        limits: ProcessLimits,
        *,
        extra_env: Mapping[str, str] | None = None,
        cancel: threading.Event | None = None,
    ) -> ProcessResult:
        assert all(marker not in a for a in argv)
        result = run_process(argv, stdin, limits, extra_env=extra_env, cancel=cancel)
        captured.append(result)
        return result

    code = _code(f"int main(void) {{ /* {marker} */ return 0; }}\n", Language.C)
    run_tier1(code, SETTINGS, toolchain=Toolchain(c=fake), runner=spy)
    import json

    listing, _ = json.loads(captured[0].stdout)
    assert listing == []


# ------------------------------------------------------------------ sonuç sınıflandırma


def test_c_type_error_failed() -> None:
    runner = FakeRunner(ProcessResult(1, "", _stderr("gcc_c_type_error.txt")))
    result = run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.FAILED
    assert result.tool == "gcc"
    assert [(d.line, d.severity) for d in result.diagnostics][:2] == [(3, "error"), (4, "warning")]
    assert all(d.tool == "gcc" for d in result.diagnostics)


def test_clang_cpp_error_failed() -> None:
    chain = Toolchain(cpp=CompilerTool(name="clang++", kind="clang", command=["/c++"]))
    runner = FakeRunner(ProcessResult(1, "", _stderr("clang_cpp_type_error.txt")))
    result = run_tier1(_code(CPP_CODE, Language.CPP), SETTINGS, toolchain=chain, runner=runner)
    assert result.status is CompilationStatus.FAILED
    assert all(d.tool == "clang" for d in result.diagnostics)


def test_warnings_only_warning() -> None:
    stderr = "<stdin>:3:9: warning: unused variable 'x' [-Wunused-variable]\n"
    runner = FakeRunner(ProcessResult(0, "", stderr))
    result = run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.WARNING
    assert result.diagnostics[0].severity == "warning"


def test_clean_passed() -> None:
    runner = FakeRunner(ProcessResult(0, "", ""))
    result = run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.PASSED
    assert result.diagnostics == []
    assert result.skip_reason is None


@pytest.mark.parametrize("sample", ["gcc_missing_header.txt", "clang_missing_header.txt"])
def test_missing_local_header_is_warning(sample: str) -> None:
    runner = FakeRunner(ProcessResult(1, "", _stderr(sample)))
    code = _code('#include "WaveSpawner.h"\nint main() { return 0; }\n', Language.CPP)
    result = run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.WARNING
    assert [d.severity for d in result.diagnostics] == ["warning"]
    assert result.warnings


def test_unreal_errors_demoted_to_warning() -> None:
    runner = FakeRunner(ProcessResult(1, "", _stderr("clang_unreal_stub.txt")))
    code = _code(UNREAL_CODE, Language.CPP, Engine.UNREAL)
    result = run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.WARNING
    assert result.diagnostics
    assert all(d.severity != "error" for d in result.diagnostics)
    assert result.warnings


def test_unreal_clean_passed() -> None:
    runner = FakeRunner(ProcessResult(0, "", ""))
    code = _code(UNREAL_CODE, Language.CPP, Engine.UNREAL)
    assert run_tier1(code, SETTINGS, toolchain=FULL, runner=runner).status in (
        CompilationStatus.PASSED,
        CompilationStatus.WARNING,
    )


def test_roslyn_error_failed() -> None:
    runner = FakeRunner(ProcessResult(0, _stderr("roslyn_errors.json"), ""))
    result = run_tier1(_code(CS_CODE, Language.CSHARP), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.FAILED
    assert result.diagnostics[0].tool == "roslyn"


@pytest.mark.parametrize(
    "result", [ProcessResult(0, "not json", ""), ProcessResult(2, "[]", "boom")]
)
def test_roslyn_bad_output_skipped(result: ProcessResult) -> None:
    out = run_tier1(
        _code(CS_CODE, Language.CSHARP), SETTINGS, toolchain=FULL, runner=FakeRunner(result)
    )
    assert out.status is CompilationStatus.SKIPPED
    assert out.skip_reason is SkipReason.TOOL_ERROR


def test_roslyn_tool_error_logged_for_operator(
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    """Faz 27: Roslyn aracı düşerse çıkış kodu ve stderr başı log'a (teşhis); gcc'de değil."""
    host_error = "You must install or update .NET to run this application."
    runner = FakeRunner(ProcessResult(150, "", host_error))
    run_tier1(_code(CS_CODE, Language.CSHARP), SETTINGS, toolchain=FULL, runner=runner)
    event = next(e for e in captured_logs() if e["event"] == "tier1_tool_error")
    assert event["returncode"] == 150
    assert host_error in event["stderr"]

    gcc = FakeRunner(ProcessResult(1, "", "int gizli_kod_satiri;"))
    run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=gcc)
    assert sum(e["event"] == "tier1_tool_error" for e in captured_logs()) == 1


def test_truncated_output_flagged() -> None:
    stderr = "<stdin>:3:13: error: bad\n"
    runner = FakeRunner(ProcessResult(1, "", stderr, truncated=True))
    result = run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.truncated
    assert result.status is CompilationStatus.FAILED


def test_never_raises_on_runner_exception() -> None:
    def broken(*_args: object, **_kwargs: object) -> ProcessResult:
        raise OSError("disk dolu")

    result = run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=broken)
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.TOOL_ERROR


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
    code = _code(prefix + UNREAL_CODE, Language.CPP, Engine.UNREAL)
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
    run_tier1(_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner, cancel=cancel)
    assert runner.cancels == [cancel]


def test_roslyn_env_keeps_fsize_limit_compatible() -> None:
    """Faz 27: Linux'ta RLIMIT_FSIZE altında CoreCLR açılabilsin (W^X kapalı, GC sınırlı)."""
    runner = FakeRunner()
    run_tier1(_code(CS_CODE, Language.CSHARP), SETTINGS, toolchain=FULL, runner=runner)
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
    runner = FakeRunner(ProcessResult(1, "", _stderr("zig_clang_cpp_crlf.txt")))
    code = _code(CPP_CODE, Language.CPP)
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
