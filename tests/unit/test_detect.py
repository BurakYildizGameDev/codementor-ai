"""Dil/motor tespiti testleri (mimari §5.1)."""

from __future__ import annotations

import pytest

from codementor.ingest.detect import detect
from codementor.ingest.errors import LanguageDetectionError
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint
from tests.unit.tier0_fixtures import Tier0Fixture, load_fixtures

VALID = load_fixtures(valid=True)


def test_fixture_count() -> None:
    assert len(VALID) == 15
    engines = {f.engine for f in VALID}
    assert {Engine.UNITY, Engine.UNREAL, Engine.NONE} <= engines


@pytest.mark.parametrize("fixture", VALID, ids=lambda f: f.id)
def test_detects_all_valid_fixtures(fixture: Tier0Fixture) -> None:
    result = detect(fixture.text)
    assert (result.language, result.engine) == (fixture.language, fixture.engine)
    assert 0 < result.confidence <= 1
    assert result.reasons


@pytest.mark.parametrize(
    ("code", "language", "engine"),
    [
        ('#include <stdio.h>\nint main(void) { printf("x"); }', Language.C, Engine.NONE),
        ("#include <stdlib.h>\nvoid f(void) { free(malloc(4)); }", Language.C, Engine.NONE),
        ("#include <iostream>\nint main() { std::cout << 1; }", Language.CPP, Engine.NONE),
        ("#include <stdio.h>\n#include <vector>\nstd::vector<int> v;", Language.CPP, Engine.NONE),
        ("auto p = std::make_unique<int>(3);", Language.CPP, Engine.NONE),
        (
            "class A {\npublic:\n  A() = default;\n};\ntemplate <typename T> T id(T x);",
            Language.CPP,
            Engine.NONE,
        ),
        (
            "using System;\nclass P { static void Main() { Console.WriteLine(1); } }",
            Language.CSHARP,
            Engine.NONE,
        ),
        (
            "namespace X;\npublic class A { public int B { get; set; } }",
            Language.CSHARP,
            Engine.NONE,
        ),
        ("using UnityEngine;\npublic class A : MonoBehaviour { }", Language.CSHARP, Engine.UNITY),
        (
            "public class A : MonoBehaviour {\n  [SerializeField] float s;\n}",
            Language.CSHARP,
            Engine.UNITY,
        ),
        ("UCLASS()\nclass AFoo : public AActor { GENERATED_BODY() };", Language.CPP, Engine.UNREAL),
        ('#include "CoreMinimal.h"\nstruct FData { int32 X; };', Language.CPP, Engine.UNREAL),
    ],
)
def test_detects_snippets(code: str, language: Language, engine: Engine) -> None:
    result = detect(code)
    assert (result.language, result.engine) == (language, engine)


@pytest.mark.parametrize(
    "code",
    [
        "int main(void) { return 0; }",
        "x = 1;",
        "// sadece yorum\n",
        "int add(int a, int b) { return a + b; }",
    ],
)
def test_ambiguous_code_raises(code: str) -> None:
    with pytest.raises(LanguageDetectionError, match="belirlenemedi") as exc:
        detect(code)
    assert exc.value.status_code == 422


def test_signals_in_comments_are_ignored() -> None:
    code = "// using UnityEngine; UCLASS()\n/* std::vector */\n#include <stdio.h>\nint x;"
    result = detect(code)
    assert (result.language, result.engine) == (Language.C, Engine.NONE)


@pytest.mark.parametrize(
    "code",
    [
        '#include <stdio.h>\nint main(void) { printf("sonuc => %d\\n", 3); return 0; }',
        '#include <stdio.h>\nint main(void) { printf("Hata::bellek std::x\\n"); return 0; }',
        '#include <stdio.h>\nint main(void) { puts("using UnityEngine; UCLASS()"); }',
    ],
)
def test_signals_inside_strings_are_ignored(code: str) -> None:
    result = detect(code)
    assert (result.language, result.engine) == (Language.C, Engine.NONE)


@pytest.mark.parametrize(
    "code",
    [
        "#include <stdio.h>\nclass A { int x; };\nint main() { A* a = new A; delete a; "
        'printf("%d", 1); return 0; }',
        "#include <stdio.h>\nstruct V { int x; };\nvoid inc(V& v) { v.x++; }\n"
        'int main(void) { V v = {0}; inc(v); printf("%d", v.x); }',
    ],
    ids=["class-new-delete", "reference-param"],
)
def test_c_style_cpp_detected_via_grammar(code: str) -> None:
    result = detect(code)
    assert result.language is Language.CPP
    assert any("C++ dilbilgisi" in r for r in result.reasons)


def test_valid_c_stays_c_after_grammar_check() -> None:
    code = "#include <stdlib.h>\ntypedef struct { int *p; } Box;\nvoid f(Box *b) { free(b->p); }"
    assert detect(code).language is Language.C


def test_unity_detected_without_using_directive() -> None:
    code = "public class Mover : MonoBehaviour\n{\n    void Update() { }\n}\n"
    result = detect(code)
    assert (result.language, result.engine) == (Language.CSHARP, Engine.UNITY)


@pytest.mark.parametrize(
    "code",
    [
        "public class Main {\n  public static void main(String[] args) {\n"
        '    System.out.println("x");\n  }\n}',
        "import java.util.List;\npublic class A { private int x; }",
    ],
)
def test_java_is_rejected(code: str) -> None:
    with pytest.raises(LanguageDetectionError, match="Java"):
        detect(code)


def test_confidence_higher_for_stronger_evidence() -> None:
    weak = detect("#include <vector>\nint x;")
    strong = detect("#include <vector>\n#include <memory>\nstd::vector<int> v; auto p = nullptr;")
    assert strong.confidence > weak.confidence


# ---------------------------------------------------------------- ipucu önceliği


def test_full_hint_wins() -> None:
    code = "using UnityEngine;\npublic class A : MonoBehaviour { }"
    result = detect(code, LanguageHint(language=Language.CSHARP, engine=Engine.NONE))
    assert (result.language, result.engine) == (Language.CSHARP, Engine.NONE)
    assert result.confidence == 1.0


def test_engine_hint_implies_language() -> None:
    result = detect("x = 1;", LanguageHint(engine=Engine.UNREAL))
    assert (result.language, result.engine) == (Language.CPP, Engine.UNREAL)


def test_language_hint_detects_compatible_engine() -> None:
    code = "using UnityEngine;\npublic class A : MonoBehaviour { }"
    result = detect(code, LanguageHint(language=Language.CSHARP))
    assert result.engine is Engine.UNITY


def test_language_hint_ignores_incompatible_engine() -> None:
    code = "using UnityEngine;\npublic class A : MonoBehaviour { }"
    result = detect(code, LanguageHint(language=Language.C))
    assert (result.language, result.engine) == (Language.C, Engine.NONE)


def test_language_hint_on_ambiguous_code() -> None:
    result = detect("int main(void) { return 0; }", LanguageHint(language=Language.C))
    assert (result.language, result.engine) == (Language.C, Engine.NONE)


def test_engine_none_hint_still_detects_language() -> None:
    result = detect("#include <iostream>\nint main() {}", LanguageHint(engine=Engine.NONE))
    assert (result.language, result.engine) == (Language.CPP, Engine.NONE)


@pytest.mark.parametrize(
    ("language", "engine"),
    [(Language.C, Engine.UNITY), (Language.CPP, Engine.UNITY), (Language.CSHARP, Engine.UNREAL)],
)
def test_inconsistent_hint_rejected(language: Language, engine: Engine) -> None:
    with pytest.raises(ValueError, match="motoru"):
        LanguageHint(language=language, engine=engine)
