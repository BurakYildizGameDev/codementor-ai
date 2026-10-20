"""tree-sitter ayrıştırıcı ve Unreal makro nötrleştirme testleri."""

from __future__ import annotations

import subprocess
import sys
import threading
import time

import pytest
from tree_sitter import Parser

from codementor.analysis.parsers import (
    get_parser,
    iter_nodes,
    neutralize_unreal_macros,
    parse_source,
)
from codementor.models.enums import Engine, Language


@pytest.mark.parametrize(
    ("language", "code"),
    [
        (Language.C, "int main(void) { return 0; }"),
        (Language.CPP, "#include <vector>\nstd::vector<int> v;"),
        (Language.CSHARP, "class A { void F() { var x = 1; } }"),
    ],
)
def test_parse_valid_code(language: Language, code: str) -> None:
    parsed = parse_source(code, language, Engine.NONE)
    assert not parsed.tree.root_node.has_error
    assert parsed.text == code


def test_parser_cached_per_thread() -> None:
    assert get_parser(Language.C) is get_parser(Language.C)
    assert get_parser(Language.C) is not get_parser(Language.CPP)
    other: list[Parser] = []
    thread = threading.Thread(target=lambda: other.append(get_parser(Language.C)))
    thread.start()
    thread.join()
    assert other[0] is not get_parser(Language.C)


# ---------------------------------------------------------------- Unreal makroları


def _check_shape(original: str, neutral: str) -> None:
    assert len(neutral) == len(original)
    assert [i for i, c in enumerate(neutral) if c == "\n"] == [
        i for i, c in enumerate(original) if c == "\n"
    ]


@pytest.mark.parametrize(
    "code",
    [
        "UCLASS()\nclass A {};",
        'UPROPERTY(EditAnywhere, meta = (ClampMin = "0", Nested = (A = (1))))\nfloat X;',
        'UFUNCTION(BlueprintCallable,\n          Category = "Çok satırlı")\nvoid F();',
        'UPROPERTY(meta = (ToolTip = "a) b"))\nint32 Y;',
        'UENUM()\nenum class E : uint8 { A UMETA(DisplayName = "Öğe"), B };',
        "class MYGAME_API AFoo {};",
    ],
)
def test_neutralize_preserves_shape_and_removes_macros(code: str) -> None:
    neutral = neutralize_unreal_macros(code)
    _check_shape(code, neutral)
    for macro in ("UCLASS", "UPROPERTY", "UFUNCTION", "UENUM", "UMETA", "MYGAME_API"):
        assert macro not in neutral


@pytest.mark.parametrize(
    "member",
    [
        'UPROPERTY(EditAnywhere, // (eski ayar\n              Category = "X")\n    int32 X;',
        "UPROPERTY(meta = (ClampMax = 1'000))\n    int32 Y;",
        'UPROPERTY(meta = (ToolTip = "a) b /* c"))\n    int32 Z;',
        "UFUNCTION(/* (yorum) */ BlueprintCallable)\n    void F();",
    ],
    ids=["line-comment", "digit-separator", "string-with-comment", "block-comment"],
)
def test_macro_arguments_with_comments_and_literals(member: str) -> None:
    code = f"UCLASS()\nclass AFoo : public AActor\n{{\n    GENERATED_BODY()\n    {member}\n}};\n"
    neutral = neutralize_unreal_macros(code)
    _check_shape(code, neutral)
    assert "UPROPERTY" not in neutral
    assert "UFUNCTION" not in neutral
    assert not parse_source(code, Language.CPP, Engine.UNREAL).tree.root_node.has_error


def test_macro_names_inside_strings_and_comments_are_ignored() -> None:
    code = 'const char* s = "UCLASS(";\n// UPROPERTY(\nint f(int x) { return (x); }\n'
    assert neutralize_unreal_macros(code) == code


@pytest.mark.parametrize(
    "hostile",
    ["UPROPERTY(" * 4000, "UMETA(" * 6826, "UCLASS(" * 5851, "X_API " * 6000],
    ids=["uproperty", "umeta", "uclass", "api"],
)
def test_neutralize_is_linear_on_hostile_input(hostile: str) -> None:
    """Regresyon (DoS, mimari §12): eski sürüm 40 KB girdide 4-7 saniye harcıyordu."""
    start = time.perf_counter()
    neutral = neutralize_unreal_macros(hostile)
    assert time.perf_counter() - start < 0.5
    assert len(neutral) == len(hostile)


def test_neutralize_keeps_similar_identifiers() -> None:
    code = "int MY_UCLASS_HELPER(int); int UCLASSIFY(); int x = GENERATED_BODY_COUNT;"
    assert neutralize_unreal_macros(code) == code


def test_neutralize_leaves_unterminated_macro() -> None:
    code = "UPROPERTY(EditAnywhere\nfloat X;"
    assert neutralize_unreal_macros(code) == code


# ------------------------------------------------- delege bildirimleri (Faz H3)

_DELEGATE_LINE = (
    "DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnReady, int32, Index, bool, bDone);\n"
)
_DELEGATE_SOURCE = (
    _DELEGATE_LINE
    + "\nUCLASS()\nclass AGadget : public AActor\n{\n    GENERATED_BODY()\n"
    + "public:\n    UPROPERTY(BlueprintAssignable)\n    FOnReady OnReady;\n};\n"
)


@pytest.mark.parametrize(
    "line",
    [
        "DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnReady);",
        "DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnReady, int32, Index);",
        "DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams("
        "FOnReady, int32, I, bool, B, float, F, FName, N);",
        "DECLARE_DYNAMIC_MULTICAST_DELEGATE_RetVal_OneParam(bool, FOnReady, int32, Index);",
    ],
)
def test_delegate_declaration_is_neutralized_for_parsing(line: str) -> None:
    """Tree-sitter çıplak delege bildirimini ayrıştıramaz: ayrıştırma yolunda boşaltılır."""
    code = line + "\n"
    assert neutralize_unreal_macros(code) == code  # derleyici yolu: makro stub'a bırakılır
    neutral = neutralize_unreal_macros(code, delegates=True)
    _check_shape(code, neutral)
    assert "DECLARE_DYNAMIC_MULTICAST_DELEGATE" not in neutral
    assert neutral.count(";") == code.count(";")


def test_delegate_source_parses_without_errors_when_unreal() -> None:
    """Geçerli Unreal kodu: delege bildirimi yüzünden 'sözdizimi hatası' verilmez."""
    assert parse_source(_DELEGATE_SOURCE, Language.CPP, Engine.NONE).tree.root_node.has_error
    parsed = parse_source(_DELEGATE_SOURCE, Language.CPP, Engine.UNREAL)
    assert not parsed.tree.root_node.has_error
    assert "OnReady" in parsed.text  # alan yerinde kalır (yalnızca makro çağrısı boşalır)


def test_delegate_neutralization_keeps_unterminated_call() -> None:
    code = "DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnReady, int32, Index\n"
    assert neutralize_unreal_macros(code, delegates=True) == code


def test_delegate_neutralization_is_linear_on_hostile_input() -> None:
    """40 KB kötü niyetli girdi (kapanmayan delege makroları) doğrusal kalmalı."""
    hostile = ("DECLARE_DYNAMIC_MULTICAST_DELEGATE_" + "A" * 6_000 + "\n") * 2
    start = time.perf_counter()
    neutral = neutralize_unreal_macros(hostile, delegates=True)
    assert time.perf_counter() - start < 0.5
    assert len(neutral) == len(hostile)


def test_neutralized_unreal_parses_without_errors() -> None:
    code = (
        '#include "CoreMinimal.h"\n'
        "UCLASS(Blueprintable)\n"
        "class MYGAME_API AFoo : public AActor\n"
        "{\n"
        "    GENERATED_BODY()\n"
        "    UPROPERTY(EditAnywhere)\n"
        "    TArray<TObjectPtr<AActor>> Items;\n"
        "};\n"
    )
    assert parse_source(code, Language.CPP, Engine.NONE).tree.root_node.has_error
    assert not parse_source(code, Language.CPP, Engine.UNREAL).tree.root_node.has_error


def test_real_error_after_macro_keeps_line_number() -> None:
    code = "UCLASS()\nclass AFoo\n{\n    GENERATED_BODY()\n    float X = 1.f\n    void F();\n};\n"
    root = parse_source(code, Language.CPP, Engine.UNREAL).tree.root_node
    assert root.has_error
    rows = [n.start_point.row + 1 for n in iter_nodes(root) if n.is_error or n.is_missing]
    assert min(rows) in {5, 6}


# ---------------------------------------------------------------- güvenli gezinti


def test_iter_nodes_preorder() -> None:
    root = parse_source("int a; int b;", Language.C, Engine.NONE).tree.root_node
    types = [n.type for n in iter_nodes(root)]
    assert types[0] == "translation_unit"
    assert types.count("declaration") == 2
    assert types.index("declaration") < types.index("identifier")
    assert len(types) == root.descendant_count


def test_iter_nodes_prunes_subtrees() -> None:
    root = parse_source("int a; int b;", Language.C, Engine.NONE).tree.root_node
    shallow = list(iter_nodes(root, descend=lambda n: n.type == "translation_unit"))
    assert [n.type for n in shallow] == ["translation_unit", "declaration", "declaration"]


_BINDING_PROBE = """
import tree_sitter as ts, tree_sitter_c
parser = ts.Parser(ts.Language(tree_sitter_c.language()))
unit = "struct n { int v; };\\nstatic int f(void) {\\n    return 0;\\n}\\nint x = @;\\n"
root = parser.parse((unit * 150).encode()).root_node
found, stack = [], [root]
while stack:
    node = stack.pop()
    if node.is_error or node.is_missing:
        found.append(node)
    elif node.has_error:
        stack.extend(reversed(node.children))
stack, rows = [root], []
while stack:
    node = stack.pop()
    if node.child_count:
        stack.extend(reversed(node.children))
    elif node.type == "{":
        rows.append(node.start_point.row)
print(len(found), len(rows))
"""


@pytest.mark.slow
def test_tree_sitter_binding_is_memory_safe() -> None:
    """tree-sitter 0.26.0 bu kalıpta erişim ihlaliyle çöküyor (`Point` refcount hatası,
    py-tree-sitter#472; düzeltme 0.26.1'i bekliyor); sürüm `<0.26` sabitlendi.

    Sürüm yükseltilirse bu test yeni sürümün güvenli olup olmadığını söyler.
    """
    result = subprocess.run(
        [sys.executable, "-c", _BINDING_PROBE], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, f"tree-sitter bağlaması çöktü: {result.stderr[-500:]}"


def test_large_tree_with_errors_does_not_crash() -> None:
    """Regresyon: `Node.children` ile gezinti tree-sitter 0.26'da erişim ihlaliyle çöküyordu."""
    unit = "struct n { int v; };\nstatic int f(void) {\n    return 0;\n}\nint x = @;\n"
    code = unit * 150
    root = parse_source(code, Language.C, Engine.NONE).tree.root_node
    errors = [n for n in iter_nodes(root) if n.is_error]
    assert errors
    points = [e.start_point for e in errors]
    braces = [n.start_point.row for n in iter_nodes(root) if n.type == "{"]
    assert points
    assert len(braces) >= 300
