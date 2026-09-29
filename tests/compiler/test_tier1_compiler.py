"""Gerçek derleyicilerle Tier 1 testleri (`@pytest.mark.compiler`).

Araç `PATH`'te yoksa (veya Roslyn aracı derlenmemişse: `make roslyn-check`) test atlanır.
Tanı metinleri sürüme göre değiştiği için yalnızca durum/satır/önem düzeyine bakılır.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from codementor.config import ValidationSettings
from codementor.ingest.normalize import normalize
from codementor.models.enums import CompilationStatus, Engine, Language
from codementor.models.request import LanguageHint, NormalizedCode
from codementor.models.validation import Tier1Result, Toolchain
from codementor.validation.tier0 import run_tier0
from codementor.validation.tier1 import run_tier1
from codementor.validation.toolchain import discover

pytestmark = pytest.mark.compiler

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures" / "tier0"
SETTINGS = ValidationSettings(
    stub_header=ROOT / "data" / "stubs" / "ue_stubs.h",
    roslyn_check_dll=ROOT / "tools" / "roslyn-check" / "out" / "RoslynCheck.dll",
)
CHAIN: Toolchain = discover(os.environ.get("PATH", ""), SETTINGS.roslyn_check_dll)

needs_c = pytest.mark.skipif(CHAIN.c is None, reason="gcc/clang yok")
needs_cpp = pytest.mark.skipif(CHAIN.cpp is None, reason="g++/clang++ yok")
needs_unreal = pytest.mark.skipif(CHAIN.unreal is None, reason="clang++/g++ yok")
needs_roslyn = pytest.mark.skipif(
    CHAIN.csharp is None, reason="dotnet veya derlenmiş roslyn-check yok (make roslyn-check)"
)


def _code(text: str, language: Language, engine: Engine = Engine.NONE) -> NormalizedCode:
    return normalize(text, LanguageHint(language=language, engine=engine))


def _run(code: NormalizedCode) -> Tier1Result:
    return run_tier1(code, SETTINGS, toolchain=CHAIN)


def _errors(result: Tier1Result) -> list[int]:
    return [d.line for d in result.diagnostics if d.severity == "error"]


@needs_c
def test_c_type_error_tree_sitter_misses() -> None:
    code = _code(
        "struct P { int a; };\nint main(void) {\n    struct P p = {1};\n    return p.b;\n}\n",
        Language.C,
    )
    assert not run_tier0(code).has_errors  # tree-sitter görmüyor
    result = _run(code)
    assert result.status is CompilationStatus.FAILED
    assert 4 in _errors(result)


@needs_c
def test_valid_c_passes() -> None:
    code = _code(
        '#include <stdio.h>\nint main(void) {\n    puts("hi");\n    return 0;\n}\n', Language.C
    )
    assert _run(code).status is CompilationStatus.PASSED


@needs_cpp
def test_cpp_type_error_failed() -> None:
    code = _code('int main() {\n    int x = "a";\n    return x;\n}\n', Language.CPP)
    assert not run_tier0(code).has_errors
    result = _run(code)
    assert result.status is CompilationStatus.FAILED
    assert 2 in _errors(result)


@needs_cpp
def test_valid_cpp_fixture_not_failed() -> None:
    code = _code(
        (FIXTURES / "cpp" / "valid" / "lru_cache.cpp").read_text(encoding="utf-8"), Language.CPP
    )
    assert _run(code).status in (CompilationStatus.PASSED, CompilationStatus.WARNING)


@needs_cpp
def test_missing_local_header_is_warning() -> None:
    code = _code('#include "WaveSpawner.h"\nint main() { return 0; }\n', Language.CPP)
    result = _run(code)
    assert result.status is CompilationStatus.WARNING
    assert result.diagnostics[0].line == 1


@needs_unreal
@pytest.mark.parametrize("name", ["unreal_wave_spawner.cpp", "unreal_health_regen.h"])
def test_unreal_fixture_never_failed(name: str) -> None:
    text = (FIXTURES / "cpp" / "valid" / name).read_text(encoding="utf-8")
    result = _run(_code(text, Language.CPP, Engine.UNREAL))
    assert result.status in (CompilationStatus.PASSED, CompilationStatus.WARNING)
    assert result.skip_reason is None


@needs_roslyn
@pytest.mark.parametrize(
    ("name", "engine"),
    [
        ("fizzbuzz.cs", Engine.NONE),
        ("async_repository.cs", Engine.NONE),
        ("span_parser.cs", Engine.NONE),
        ("unity_door.cs", Engine.UNITY),
        ("unity_inventory.cs", Engine.UNITY),
    ],
)
def test_roslyn_valid_fixtures_pass(name: str, engine: Engine) -> None:
    text = (FIXTURES / "csharp" / "valid" / name).read_text(encoding="utf-8")
    result = _run(_code(text, Language.CSHARP, engine))
    assert result.status is CompilationStatus.PASSED, result
    assert result.tool == "roslyn-check"


@needs_roslyn
def test_roslyn_syntax_error_failed() -> None:
    code = _code("class A\n{\n    void F() { int x = 1 }\n}\n", Language.CSHARP)
    result = _run(code)
    assert result.status is CompilationStatus.FAILED
    assert _errors(result) == [3]
    assert result.diagnostics[0].tool == "roslyn"


@needs_roslyn
def test_roslyn_handles_unicode_and_preprocessor() -> None:
    code = _code(
        '#if UNITY_EDITOR\nusing UnityEditor;\n#endif\nclass Ö {\n    string s = "çğü — ✓";\n}\n',
        Language.CSHARP,
        Engine.UNITY,
    )
    assert _run(code).status is CompilationStatus.PASSED
