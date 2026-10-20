"""Unreal `Super` typedef'i (Sonraya #9): UHT'nin `GENERATED_BODY()` ile eklediği bildirim.

Stub gerçek UHT çıktısını bilemez; derleyici yolu türetilmiş sınıfın gövdesine aynı satırda
`typedef <Taban> Super;` ekler. Ayrıştırma (Tier 0) yolu bundan etkilenmez.
"""

from __future__ import annotations

import pytest

from codementor.analysis.parsers import neutralize_unreal_macros, unreal_super_typedefs
from codementor.models.enums import Engine, Language
from codementor.validation.tier1 import run_tier1
from tests.timing import best_pair
from tests.unit.tier1_helpers import FULL, SETTINGS, FakeRunner, normalize_code

ACTOR = (
    "UCLASS()\nclass AFoo : public AActor\n{\n    GENERATED_BODY()\n"
    "public:\n    void Tick(float D);\n};\n"
)


def _apply(text: str) -> str:
    out = text
    for position, declaration in reversed(unreal_super_typedefs(text)):
        out = out[:position] + declaration + out[position:]
    return out


def test_typedef_inserted_after_class_brace_without_newline() -> None:
    result = _apply(ACTOR)
    assert result.count("\n") == ACTOR.count("\n")
    assert result.split("\n")[2] == "{ typedef AActor Super;"


@pytest.mark.parametrize(
    ("text", "base"),
    [
        ("class MYGAME_API AFoo : public AActor { GENERATED_BODY() };", "AActor"),
        ("class AFoo final : public ACharacter { GENERATED_BODY() };", "ACharacter"),
        ("struct FRow : public FTableRowBase { GENERATED_USTRUCT_BODY() };", "FTableRowBase"),
        (
            "class UHp : public UActorComponent, public IFace { GENERATED_BODY() };",
            "UActorComponent",
        ),
        ("class AFoo : AActor { GENERATED_UCLASS_BODY() };", "AActor"),
        ("class AFoo : public Game::ABase { GENERATED_BODY() };", "Game::ABase"),
    ],
)
def test_base_name_captured(text: str, base: str) -> None:
    assert [declaration for _, declaration in unreal_super_typedefs(text)] == [
        f" typedef {base} Super;"
    ]


@pytest.mark.parametrize(
    "text",
    [
        "class AFoo : public AActor { void Tick(); };",  # GENERATED_BODY yok: UHT typedef eklemez
        "class AFoo { GENERATED_BODY() };",  # taban yok
        "class AFoo : public TBase<int> { GENERATED_BODY() };",  # şablon taban: typedef geçersiz
        "// class AFoo : public AActor { GENERATED_BODY() };\n",  # yorum
        'const char* s = "class AFoo : public AActor { GENERATED_BODY() };";',  # dize
    ],
)
def test_no_typedef(text: str) -> None:
    assert unreal_super_typedefs(text) == []


def test_each_class_uses_its_own_body() -> None:
    """İkinci sınıfın `GENERATED_BODY`'si birinciye yazılmaz."""
    text = (
        "class APlain : public AActor { void F(); };\n"
        "class AReal : public APawn { GENERATED_BODY() };\n"
    )
    assert [d for _, d in unreal_super_typedefs(text)] == [" typedef APawn Super;"]


def test_positions_valid_after_neutralization() -> None:
    """Konumlar orijinal metinde hesaplanır; nötrleştirme aynı uzunlukta boşalttığından geçerli."""
    text = "class MYGAME_API AFoo : public AActor\n{\n    GENERATED_BODY()\n};\n"
    neutral = neutralize_unreal_macros(text)
    ((position, _),) = unreal_super_typedefs(text)
    assert neutral[position - 1] == "{"


def test_tier1_stdin_gets_typedef_and_keeps_lines() -> None:
    runner = FakeRunner()
    code = normalize_code(ACTOR, Language.CPP, Engine.UNREAL)
    run_tier1(code, SETTINGS, toolchain=FULL, runner=runner)
    stdin = runner.calls[0][1]
    assert stdin.count("\n") == code.text.count("\n")
    assert stdin.split("\n")[2] == "{ typedef AActor Super;"
    assert "GENERATED_BODY" not in stdin


def test_plain_cpp_gets_no_typedef() -> None:
    """Yalnız Unreal motoru: düz C++'ta `GENERATED_BODY` geçse de metin değişmez."""
    runner = FakeRunner()
    text = "class AFoo : public ABase { int GENERATED_BODY; };\n"
    run_tier1(normalize_code(text, Language.CPP), SETTINGS, toolchain=FULL, runner=runner)
    assert "Super" not in runner.calls[0][1]


@pytest.mark.parametrize(
    "unit",
    [
        "class A : public B ",  # gövdesiz tekrar
        "class A : public B, ",  # açık kalan taban listesi
        "class " + "A" * 50 + " : ",
    ],
)
def test_scan_grows_linearly(unit: str) -> None:
    """Kötü niyetli tekrarda tarama doğrusal kalır (mimari §12): 2× girdi ≤ 3× süre."""
    small, large = (unit * (16_000 // len(unit)), unit * (32_000 // len(unit)))
    small_time, large_time = best_pair(
        lambda: unreal_super_typedefs(small), lambda: unreal_super_typedefs(large)
    )
    assert large_time <= 3.0 * max(small_time, 0.005), (small_time, large_time)
