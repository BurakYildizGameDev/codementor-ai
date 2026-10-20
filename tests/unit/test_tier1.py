"""Tier 1 orkestrasyon testleri: atlama yolları ve çağrı biçimi (sahte runner/araç zinciri).

Bölme (Faz J5, denetim Küçük-5): dosya 633 satırdı (AGENTS.md 400 satır önerisi); vaka adları ve
iddialar değişmedi, yalnız taşındı.
- Sonuç sınıflandırma + güvenlik/kolon regresyonları: `tests/unit/test_tier1_verdict.py`
- Ortak düzenek (sahte runner, örnek kod, araç zinciri): `tests/unit/tier1_helpers.py`
"""

from __future__ import annotations

import threading
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

from codementor.config import ValidationSettings
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
    STUB,
    UNREAL_CODE,
    FakeRunner,
    normalize_code,
)

# ------------------------------------------------------------------ atlama yolları


def test_disabled_skips_with_zero_calls() -> None:
    runner = FakeRunner()
    result = run_tier1(
        normalize_code(C_CODE, Language.C),
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
        normalize_code(text, language, engine), SETTINGS, toolchain=Toolchain(), runner=runner
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
        # Faz H (Önemli-3): izin listesindeki adı tanımlayan `#define` + `#pragma` makro atlatması
        (
            '#define pack GCC dependency "/etc/passwd"\n#pragma pack\nint main() { return 0; }\n',
            Language.CPP,
            Engine.NONE,
        ),
        (
            "#define warning 1\n#pragma warning(disable: 4996)\nint main() { return 0; }\n",
            Language.CPP,
            Engine.NONE,
        ),
        ("#pragma PACK(1)\nint main() { return 0; }\n", Language.CPP, Engine.NONE),
    ],
)
def test_include_guard_skips_with_zero_calls(text: str, language: Language, engine: Engine) -> None:
    runner = FakeRunner()
    result = run_tier1(
        normalize_code(text, language, engine), SETTINGS, toolchain=FULL, runner=runner
    )
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.INCLUDE_GUARD
    assert result.warnings
    assert runner.calls == []


def test_pragma_pack_and_warning_reach_compiler() -> None:
    """Faz H (Önemli-3): `#pragma pack`/`#pragma warning` Tier 1'i artık atlatmaz.

    Öncesinde bu pragmaları içeren dosya `include_guard` ile `SKIPPED` oluyordu.
    """
    runner = FakeRunner()
    text = (
        "#pragma once\n"
        "#pragma pack(push, 1)\n"
        "struct Packed { char c; int i; };\n"
        "#pragma pack(pop)\n"
        "#pragma warning(disable: 4996)\n"
        "int main() { return 0; }\n"
    )
    code = normalize_code(text, Language.CPP)
    result = run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.PASSED
    assert result.skip_reason is None
    ((argv, stdin, _, _),) = runner.calls
    assert argv[0] == "/usr/bin/g++"
    assert stdin == code.text


def test_unreal_pragma_pack_passes_both_guard_calls() -> None:
    """Faz H (Önemli-3): Unreal yolunda guard iki kez koşar (ham ve nötrleştirilmiş metin).

    `#pragma pack` ikisinden de geçmeli; aksi hâlde geçerli Unreal kodu gereksiz atlanırdı.
    """
    runner = FakeRunner()
    code = normalize_code("#pragma pack(push, 1)\n" + UNREAL_CODE, Language.CPP, Engine.UNREAL)
    result = run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    assert result.skip_reason is None
    assert len(runner.calls) == 1
    assert "#pragma pack" in runner.calls[0][1]


def test_pragma_pack_file_reaches_real_process() -> None:
    """Uçtan uca (Önemli-3): gerçek alt süreç başlar; makro atlatması fail-closed kalır."""
    import sys

    from codementor.validation.runner import run_process

    probe = "import sys; sys.stdin.read(); sys.stderr.write('<stdin>:2:1: error: sentetik\\n')"
    tool = CompilerTool(name="gcc", kind="gcc", command=[sys.executable, "-c", probe])
    launched: list[ProcessResult] = []

    def spy(
        argv: Sequence[str],
        stdin: str,
        limits: ProcessLimits,
        *,
        extra_env: Mapping[str, str] | None = None,
        cancel: threading.Event | None = None,
    ) -> ProcessResult:
        result = run_process(argv, stdin, limits, extra_env=extra_env, cancel=cancel)
        launched.append(result)
        return result

    text = "#pragma pack(push, 1)\n#pragma warning(disable: 4996)\nint main() { return 0; }\n"
    result = run_tier1(
        normalize_code(text, Language.CPP), SETTINGS, toolchain=Toolchain(cpp=tool), runner=spy
    )
    assert len(launched) == 1
    assert result.status is CompilationStatus.FAILED
    assert "sentetik" in result.diagnostics[0].message

    launched.clear()
    bypass = normalize_code(
        '#define pack GCC dependency "/etc/passwd"\n#pragma pack\n', Language.CPP
    )
    blocked = run_tier1(bypass, SETTINGS, toolchain=Toolchain(cpp=tool), runner=spy)
    assert launched == []
    assert blocked.skip_reason is SkipReason.INCLUDE_GUARD


def test_missing_stub_skipped(tmp_path: Path) -> None:
    runner = FakeRunner()
    settings = ValidationSettings(stub_header=tmp_path / "yok.h")
    result = run_tier1(
        normalize_code(UNREAL_CODE, Language.CPP, Engine.UNREAL),
        settings,
        toolchain=FULL,
        runner=runner,
    )
    assert result.skip_reason is SkipReason.STUB_MISSING
    assert runner.calls == []


def test_timeout_skipped() -> None:
    runner = FakeRunner(ProcessResult(None, "", "", timed_out=True))
    result = run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.TIMEOUT
    assert result.warnings


def test_launch_error_skipped() -> None:
    runner = FakeRunner(ProcessResult(None, "", "", error="FileNotFoundError"))
    result = run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.skip_reason is SkipReason.TOOL_ERROR


def test_crash_without_diagnostics_skipped() -> None:
    runner = FakeRunner(ProcessResult(-11, "", "Segmentation fault\n"))
    result = run_tier1(normalize_code(C_CODE, Language.C), SETTINGS, toolchain=FULL, runner=runner)
    assert result.status is CompilationStatus.SKIPPED
    assert result.skip_reason is SkipReason.TOOL_ERROR


# ------------------------------------------------------------------ çağrı biçimi


def test_argv_stdin_only_no_include_paths() -> None:
    runner = FakeRunner()
    code = normalize_code(C_CODE, Language.C)
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
    run_tier1(normalize_code(CPP_CODE, Language.CPP), SETTINGS, toolchain=FULL, runner=runner)
    argv = runner.calls[0][0]
    assert argv[0] == "/usr/bin/g++"
    assert argv[argv.index("-x") + 1] == "c++"
    assert "-std=c++20" in argv


def test_unreal_argv_has_stub_and_local_includes_blanked() -> None:
    runner = FakeRunner()
    code = normalize_code(UNREAL_CODE, Language.CPP, Engine.UNREAL)
    run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    ((argv, stdin, _, _),) = runner.calls
    assert argv[0] == "/usr/bin/clang++"
    assert argv[argv.index("-include") + 1] == str(STUB.resolve())
    assert argv[-1] == "-"
    assert not any(a.startswith("-I") for a in argv)
    # satırlar kaymaz; yalnızca yerel include satırları boşaltılır. Tek ek: UHT'nin `Super`
    # typedef'i sınıfın `{` satırına, satır sonu olmadan (Sonraya #9)
    assert stdin.count("\n") == code.text.count("\n")
    assert "#include" not in stdin
    # Tier 0 ile aynı makro nötrleştirme: yansıma makroları gider, kod yerinde kalır
    lines = stdin.split("\n")
    assert "UCLASS" not in stdin
    assert "GENERATED_BODY" not in stdin
    assert lines[3] == "class AEnemy : public AActor { typedef AActor Super;"
    original = code.text.split("\n")
    assert [len(line) for i, line in enumerate(lines) if i != 3] == [
        len(line) for i, line in enumerate(original) if i != 3
    ]
    assert lines[5].strip() == "int32 Health = 100;"
    assert lines[5].index("int32") == code.text.split("\n")[5].index("int32")


def test_unreal_api_macro_neutralized() -> None:
    runner = FakeRunner()
    text = "class MYGAME_API AFoo : public AActor {\n};\n"
    run_tier1(
        normalize_code(text, Language.CPP, Engine.UNREAL), SETTINGS, toolchain=FULL, runner=runner
    )
    stdin = runner.calls[0][1]
    assert "MYGAME_API" not in stdin
    assert stdin.index("AFoo") == text.index("AFoo")


def test_unreal_delegate_macro_reaches_compiler() -> None:
    """Faz H3: delege makroları Tier 1'de boşaltılmaz; açılımı stub başlığı yapar.

    Boşaltılsaydı delege tipi (`FOnReady`) tanımsız kalır, geçerli kod uyarı üretirdi.
    """
    runner = FakeRunner()
    text = (
        "DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnReady, int32, Index, bool, bDone);\n"
        "\nUCLASS()\nclass AGadget : public AActor\n{\n    GENERATED_BODY()\n"
        "public:\n    UPROPERTY(BlueprintAssignable)\n    FOnReady OnReady;\n};\n"
    )
    run_tier1(
        normalize_code(text, Language.CPP, Engine.UNREAL), SETTINGS, toolchain=FULL, runner=runner
    )
    argv, stdin, _, _ = runner.calls[0]
    assert "DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnReady" in stdin
    assert "UCLASS" not in stdin  # yansıma makroları yine boşaltılır
    assert str(STUB.resolve()) in argv  # tipi stub tanımlar


def test_unreal_keeps_system_includes() -> None:
    runner = FakeRunner()
    code = normalize_code("#include <vector>\n" + UNREAL_CODE, Language.CPP, Engine.UNREAL)
    run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    assert runner.calls[0][1].startswith("#include <vector>\n")


def test_roslyn_argv_and_env() -> None:
    runner = FakeRunner(ProcessResult(0, "[]", ""))
    code = normalize_code(CS_CODE, Language.CSHARP, Engine.UNITY)
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

    code = normalize_code(f"int main(void) {{ /* {marker} */ return 0; }}\n", Language.C)
    run_tier1(code, SETTINGS, toolchain=Toolchain(c=fake), runner=spy)
    import json

    listing, _ = json.loads(captured[0].stdout)
    assert listing == []
