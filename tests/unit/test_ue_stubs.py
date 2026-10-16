"""`data/stubs/ue_stubs.h` testleri: §5.2.2 listesi eksiksiz ve dosya sözdizimsel olarak geçerli."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from codementor.analysis.parsers import get_parser
from codementor.models.enums import Language

STUB = Path(__file__).resolve().parents[2] / "data" / "stubs" / "ue_stubs.h"

# mimari §5.2.2
MACROS = [
    "UCLASS",
    "USTRUCT",
    "UENUM",
    "UPROPERTY",
    "UFUNCTION",
    "GENERATED_BODY",
    "GENERATED_UCLASS_BODY",
]
TYPES = [
    "int32",
    "uint8",
    "FString",
    "FName",
    "FVector",
    "UObject",
    "AActor",
    "UActorComponent",
    "TArray",
    "TMap",
    "TSet",
    "TObjectPtr",
    "TSharedPtr",
    "TWeakObjectPtr",
]

# Faz H3: analiz sırasında en sık karşılaşılan ek tipler ve makrolar
EXTRA_TYPES = ["FMath", "FHitResult", "FTimerHandle", "FTimerManager", "FRotator", "FTransform"]
DELEGATE_MACROS = [
    "DECLARE_DYNAMIC_MULTICAST_DELEGATE",
    "DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam",
    "DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams",
    "DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams",
    "DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams",
    "DECLARE_DYNAMIC_MULTICAST_DELEGATE_FiveParams",
]
FMATH_METHODS = ["Clamp", "Abs", "Max", "Min", "Sqrt"]


@pytest.fixture(scope="module")
def stub() -> str:
    return STUB.read_text(encoding="utf-8")


@pytest.mark.parametrize("name", MACROS)
def test_macro_defined_empty(stub: str, name: str) -> None:
    assert re.search(rf"^#define {name}\(\.\.\.\)[ \t]*$", stub, re.MULTILINE), name


@pytest.mark.parametrize("name", TYPES)
def test_type_declared(stub: str, name: str) -> None:
    pattern = rf"^(?:using {name} =|(?:class|struct) {name}\b)"
    assert re.search(pattern, stub, re.MULTILINE), name


@pytest.mark.parametrize("name", EXTRA_TYPES)
def test_extra_analysis_types_declared(stub: str, name: str) -> None:
    """Faz H3: `FMath`, `FHitResult`, `FTimerHandle`/`FTimerManager` stub'da bulunur."""
    assert re.search(rf"^(?:using {name} =|(?:class|struct) {name}\b)", stub, re.MULTILINE), name


@pytest.mark.parametrize("name", FMATH_METHODS)
def test_fmath_has_static_method(stub: str, name: str) -> None:
    assert re.search(rf"static T {name}\(", stub), name


@pytest.mark.parametrize("name", DELEGATE_MACROS)
def test_delegate_macro_declares_struct(stub: str, name: str) -> None:
    """`DECLARE_DYNAMIC_MULTICAST_DELEGATE*` makroları delege adıyla bir struct tanımlar."""
    match = re.search(
        rf"^#define {name}\(Name, \.\.\.\) \\\n\s+struct Name : public (\w+)", stub, re.MULTILINE
    )
    assert match, name
    base = match.group(1)
    assert re.search(rf"^struct {base} \{{", stub, re.MULTILINE)
    for method in ("Broadcast", "AddDynamic", "RemoveDynamic", "Clear"):
        assert method in stub, method


def test_timer_manager_api_present(stub: str) -> None:
    assert re.search(r"FTimerManager& GetWorldTimerManager\(\)", stub)
    for method in ("SetTimer(", "SetTimerForNextTick(", "ClearTimer("):
        assert method in stub, method


def test_stub_matches_tier0_unreal_fixtures(stub: str) -> None:
    """Tier 0 Unreal fixture'larının kullandığı adlar stub'da tanımlı olmalı (Faz H3)."""
    names = {
        "UCLASS",
        "GENERATED_BODY",
        "FMath",
        "FTimerHandle",
        "GetWorldTimerManager",
    }
    for name in names:
        assert name in stub, name


@pytest.mark.parametrize(
    "name", ["TArray", "TMap", "TSet", "TObjectPtr", "TSharedPtr", "TWeakObjectPtr"]
)
def test_containers_are_templates(stub: str, name: str) -> None:
    assert re.search(rf"template <[^>]*>\s*class {name}\b", stub), name


def test_stub_parses_without_errors(stub: str) -> None:
    tree = get_parser(Language.CPP).parse(stub.encode("utf-8"))
    assert not tree.root_node.has_error


def test_stub_has_no_includes_outside_standard_library(stub: str) -> None:
    includes = re.findall(r"^#include\s+(\S+)", stub, re.MULTILINE)
    assert includes
    assert all(inc.startswith("<") and "/" not in inc for inc in includes)
