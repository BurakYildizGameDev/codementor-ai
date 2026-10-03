"""İndirilen zig ve self-contained Roslyn ile Tier 1 (Faz 29, `@pytest.mark.compiler`).

Zig `~/.codementor/toolchain` (ya da `CODEMENTOR_TOOLCHAIN_DIR`) altında kurulu değilse
(`codementor toolchain install zig`) testler atlanır; CI `CODEMENTOR_REQUIRE_ZIG=1` verir.
Sistem gcc/clang'ı bilerek kullanılmaz (`PATH` boş): derleyicisiz kullanıcının yolu sınanır.
"""

from __future__ import annotations

import functools
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
TOOLCHAIN_DIR = Path(
    os.environ.get("CODEMENTOR_TOOLCHAIN_DIR") or Path.home() / ".codementor" / "toolchain"
)
_EXE = ".exe" if os.name == "nt" else ""
ROSLYN_SC = ROOT / "tools" / "roslyn-check" / "sc" / f"RoslynCheck{_EXE}"
SETTINGS = ValidationSettings(
    stub_header=ROOT / "data" / "stubs" / "ue_stubs.h",
    compile_timeout_s=60,  # soğuk başlangıç (CI) — süre değil tanı doğruluğu ölçülür
)


@functools.cache
def _chain() -> Toolchain:
    """Keşif ilk testte yapılır (toplama anında değil: `-m "not live"` zig'i sondalamasın)."""
    return discover(
        "", ROOT / "yok.dll", roslyn_exe=ROSLYN_SC, toolchain_dir=TOOLCHAIN_DIR, probe_timeout_s=60
    )


@pytest.fixture
def chain() -> Toolchain:
    found = _chain()
    if found.c is None:
        pytest.skip("zig kurulu değil (codementor toolchain install zig)")
    return found


@pytest.fixture
def roslyn_chain() -> Toolchain:
    found = _chain()
    if found.csharp is None:
        pytest.skip("self-contained Roslyn yok (make roslyn-check-sc)")
    return found


def _code(text: str, language: Language, engine: Engine = Engine.NONE) -> NormalizedCode:
    return normalize(text, LanguageHint(language=language, engine=engine))


def _run(code: NormalizedCode, chain: Toolchain) -> Tier1Result:
    result = run_tier1(code, SETTINGS, toolchain=chain)
    assert result.skip_reason is None, result
    return result


def _errors(result: Tier1Result) -> list[int]:
    return [d.line for d in result.diagnostics if d.severity == "error"]


def test_zig_tools_are_clang_passthrough(chain: Toolchain) -> None:
    for tool in (chain.c, chain.cpp, chain.unreal):
        assert tool is not None
        assert (tool.name, tool.kind, tool.origin) == ("zig", "clang", "downloaded")
        assert tool.command[1] == "clang"


def test_zig_c_syntax_error_line(chain: Toolchain) -> None:
    result = _run(_code("int main(void) {\n    int x = 1\n    return x;\n}\n", Language.C), chain)
    assert result.status is CompilationStatus.FAILED
    assert _errors(result) == [2]
    assert result.tool == "zig"


def test_zig_c_type_error_tree_sitter_misses(chain: Toolchain) -> None:
    code = _code(
        "struct P { int a; };\nint main(void) {\n    struct P p = {1};\n    return p.b;\n}\n",
        Language.C,
    )
    assert not run_tier0(code).has_errors
    assert 4 in _errors(_run(code, chain))


def test_zig_c_stdlib_passes(chain: Toolchain) -> None:
    code = _code(
        "#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n"
        'int main(void) {\n    puts("hi");\n    return 0;\n}\n',
        Language.C,
    )
    assert _run(code, chain).status is CompilationStatus.PASSED


def test_zig_cpp_stdlib_warning(chain: Toolchain) -> None:
    code = _code(
        "#include <vector>\n#include <string>\n#include <map>\n#include <iostream>\n"
        "int main() {\n    std::vector<std::string> v;\n    int unused;\n"
        '    std::cout << v.size() << "\\n";\n    return 0;\n}\n',
        Language.CPP,
    )
    result = _run(code, chain)
    assert result.status is CompilationStatus.WARNING
    assert [d.line for d in result.diagnostics] == [7]


def test_zig_valid_cpp_fixture_not_failed(chain: Toolchain) -> None:
    text = (FIXTURES / "cpp" / "valid" / "lru_cache.cpp").read_text(encoding="utf-8")
    assert _run(_code(text, Language.CPP), chain).status in (
        CompilationStatus.PASSED,
        CompilationStatus.WARNING,
    )


def test_zig_missing_header_warning(chain: Toolchain) -> None:
    result = _run(
        _code('#include "WaveSpawner.h"\nint main() { return 0; }\n', Language.CPP), chain
    )
    assert result.status is CompilationStatus.WARNING
    assert result.diagnostics[0].line == 1


@pytest.mark.parametrize("name", ["unreal_wave_spawner.cpp", "unreal_health_regen.h"])
def test_zig_unreal_stub(name: str, chain: Toolchain) -> None:
    text = (FIXTURES / "cpp" / "valid" / name).read_text(encoding="utf-8")
    result = _run(_code(text, Language.CPP, Engine.UNREAL), chain)
    assert result.status in (CompilationStatus.PASSED, CompilationStatus.WARNING)


def test_self_contained_roslyn_syntax_error(roslyn_chain: Toolchain) -> None:
    assert roslyn_chain.csharp is not None
    assert roslyn_chain.csharp.origin == "bundled"
    result = _run(
        _code("class A\n{\n    void F() { int x = 1 }\n}\n", Language.CSHARP), roslyn_chain
    )
    assert result.status is CompilationStatus.FAILED
    assert _errors(result) == [3]


def test_zig_available_when_required() -> None:
    """CI `CODEMENTOR_REQUIRE_ZIG=1` verir: zig testleri sessizce atlanmasın."""
    if os.environ.get("CODEMENTOR_REQUIRE_ZIG") != "1":
        pytest.skip("yalnızca CI'da zorunlu")
    assert _chain().c is not None, f"zig {TOOLCHAIN_DIR} altında kurulu değil ya da çalışmıyor"
