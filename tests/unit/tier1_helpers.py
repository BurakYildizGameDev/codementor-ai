"""Tier 1 testlerinin ortak düzeneği: sahte runner, örnek kod ve araç zinciri.

Bölme (Faz J5, denetim Küçük-5): `tests/unit/test_tier1.py` 633 satırdı (AGENTS.md 400 satır
önerisi); düzenek iki test dosyası arasında paylaşılır:
`test_tier1.py` (atlama yolları + çağrı biçimi) ve `test_tier1_verdict.py` (sonuç sınıflandırma +
güvenlik/kolon regresyonları). Vaka adları ve iddialar değişmedi, yalnız taşındı.
"""

from __future__ import annotations

import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from codementor.config import ValidationSettings
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint, NormalizedCode
from codementor.models.validation import CompilerTool, Toolchain
from codementor.validation.runner import ProcessLimits, ProcessResult

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


def normalize_code(text: str, language: Language, engine: Engine = Engine.NONE) -> NormalizedCode:
    """Kullanıcı kodunu Tier 1'in gördüğü biçime normalleştirir.

    Ad `code` değil: testlerde yerel `code = ...` değişkeni yaygın (gölgeleme olmasın).
    """
    return normalize(text, LanguageHint(language=language, engine=engine))


def read_stderr(name: str) -> str:
    """`tests/fixtures/tier1` altındaki derleyici çıktısı örneğini okur."""
    return (SAMPLES / name).read_text(encoding="utf-8")


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
