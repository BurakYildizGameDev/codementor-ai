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
