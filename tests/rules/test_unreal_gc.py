"""Faz 32: UE-GC-001 kapsayıcı alanlar ve yansıtılmayan (UCLASS/USTRUCT olmayan) sınıflar."""

from __future__ import annotations

from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint
from codementor.rules import run_rules

PLAIN = """#pragma once
#include "CoreMinimal.h"

class FEnemyCache
{
    UEnemyData* Data;
};

UCLASS()
class AHolder : public AActor
{
    GENERATED_BODY()
    AActor* Target;
};
"""


def _gc_findings(text: str) -> dict[int, str]:
    code = normalize(text, LanguageHint(language=Language.CPP, engine=Engine.UNREAL))
    result = run_rules(code, extract_facts(code), disabled=[])
    return {f.line_start: f.description for f in result.findings if f.rule_id == "UE-GC-001"}


def test_plain_class_gets_non_uproperty_question() -> None:
    """UCLASS olmayan sınıfta UPROPERTY işe yaramaz; soru başka yolu düşündürür."""
    found = _gc_findings(PLAIN)
    assert set(found) == {6, 13}
    assert "UCLASS" in found[6]
    assert "FGCObject" in found[6] or "TStrongObjectPtr" in found[6]
    assert "UPROPERTY" in found[13]
    assert "FGCObject" not in found[13]


def test_symbols_record_unreflected_fields() -> None:
    code = normalize(PLAIN, LanguageHint(language=Language.CPP, engine=Engine.UNREAL))
    symbols = extract_facts(code).engine_symbols
    assert [s.line for s in symbols.uobject_fields] == [6, 13]
    assert [s.line for s in symbols.unreflected_fields] == [6]


NESTED = """#pragma once
#include "CoreMinimal.h"

UCLASS()
class AHolder : public AActor
{
    GENERATED_BODY()
    TMap<FName, TArray<UObject*>> Nested;
    TArray<TSet<AActor*>> Deep;
    UPROPERTY()
    TMap<FName, TArray<UObject*>> Tracked;
    TMap<FName, TArray<TArray<UObject*>>> TooDeep;
};
"""


def test_nested_container_field_is_recorded_as_uobject_field() -> None:
    """Kapsayıcı içindeki kapsayıcı da UObject tutar (`TMap<FName, TArray<UObject*>>`)."""
    code = normalize(NESTED, LanguageHint(language=Language.CPP, engine=Engine.UNREAL))
    symbols = extract_facts(code).engine_symbols
    assert [(s.name, s.line) for s in symbols.uobject_fields] == [
        ("Nested", 8),
        ("Deep", 9),
        ("Tracked", 11),
    ]


def test_container_nesting_beyond_limit_is_not_claimed() -> None:
    """İkiden derin iç içe kapsayıcı bilinçli olarak kapsam dışı (katman sınırı)."""
    found = _gc_findings(NESTED)
    assert set(found) == {8, 9}
    assert "UPROPERTY" in found[8]  # UCLASS tipi: soru UPROPERTY'ye yönlendirir
