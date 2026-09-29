"""Tier 0 (tree-sitter) ön doğrulama testleri (mimari §5.2.1)."""

from __future__ import annotations

import time

import pytest

from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint, NormalizedCode
from codementor.validation.tier0 import MAX_DIAGNOSTICS, run_tier0
from tests.unit.tier0_fixtures import Tier0Fixture, load_fixtures

VALID = load_fixtures(valid=True)
INVALID = load_fixtures(valid=False)


def _code(text: str, language: Language, engine: Engine = Engine.NONE) -> NormalizedCode:
    return normalize(text, LanguageHint(language=language, engine=engine))


def _fixture_code(fixture: Tier0Fixture) -> NormalizedCode:
    return _code(fixture.text, fixture.language, fixture.engine)


def test_fixture_counts() -> None:
    for language in Language:
        assert len([f for f in VALID if f.language is language]) >= 5
        assert len([f for f in INVALID if f.language is language]) >= 5
    assert all(f.expected_line is not None for f in INVALID)


@pytest.mark.parametrize("fixture", VALID, ids=lambda f: f.id)
def test_valid_fixtures_have_no_errors(fixture: Tier0Fixture) -> None:
    result = run_tier0(_fixture_code(fixture))
    assert result.diagnostics == [], [d.message for d in result.diagnostics]
    assert not result.has_errors


@pytest.mark.parametrize("fixture", INVALID, ids=lambda f: f.id)
def test_invalid_fixtures_error_on_marked_line(fixture: Tier0Fixture) -> None:
    result = run_tier0(_fixture_code(fixture))
    assert result.has_errors
    assert fixture.expected_line is not None
    lines = [d.line for d in result.diagnostics]
    assert any(abs(line - fixture.expected_line) <= 1 for line in lines), lines


@pytest.mark.parametrize("fixture", INVALID, ids=lambda f: f.id)
def test_diagnostic_shape(fixture: Tier0Fixture) -> None:
    code = _fixture_code(fixture)
    for d in run_tier0(code).diagnostics:
        assert d.tool == "tree-sitter"
        assert d.severity == "error"
        assert 1 <= d.line <= len(code.lines)
        assert d.column is not None
        assert 1 <= d.column <= len(code.lines[d.line - 1]) + 1
        assert d.message


def test_unreal_without_neutralization_would_fail() -> None:
    """Unreal makroları nötrleştirilmezse geçerli kod hata üretir (regresyon kalkanı)."""
    fixture = next(f for f in VALID if f.engine is Engine.UNREAL)
    assert run_tier0(_code(fixture.text, Language.CPP, Engine.NONE)).has_errors
    assert not run_tier0(_fixture_code(fixture)).has_errors


# ---------------------------------------------------------------- mesajlar ve konum


def test_missing_semicolon_message() -> None:
    result = run_tier0(_code("int main(void) {\n    int x = 1\n    return x;\n}", Language.C))
    assert result.diagnostics[0].line == 2
    assert "noktalı virgül" in result.diagnostics[0].message


def test_unexpected_token_message() -> None:
    result = run_tier0(_code("int main(void) {\n    int x = 1 @;\n}\n", Language.C))
    assert [(d.line, d.message) for d in result.diagnostics] == [(2, "Beklenmeyen sözdizimi: '@'")]


@pytest.mark.parametrize(
    ("language", "code", "line"),
    [
        (
            Language.C,
            "int main(void) {\n    int x = 1;\n    x = 2\n    // yorum\n    return x;\n}\n",
            3,
        ),
        (
            Language.C,
            "int main(void) {\n    int x = 1\n    /* a */\n    // b\n\n"
            "    // c\n    return x;\n}\n",
            2,
        ),
        (Language.CPP, "struct A {\n    float s = 2.f\n\n    // yorum\n    int t;\n};\n", 2),
    ],
    ids=["line-comment", "many-comments", "cpp-member"],
)
def test_missing_semicolon_reported_before_comments(
    language: Language, code: str, line: int
) -> None:
    """Regresyon: tree-sitter eksik ';'yi araya giren yorumların arkasına yerleştirir."""
    diag = run_tier0(_code(code, language)).diagnostics[0]
    assert diag.line == line
    assert "noktalı virgül" in diag.message


@pytest.mark.parametrize(
    "fixture",
    [f for f in INVALID if "missing_semicolon" in f.path.name],
    ids=lambda f: f.id,
)
def test_missing_semicolon_fixtures_exact(fixture: Tier0Fixture) -> None:
    """Eksik ';' fixture'larında tanı tam işaretli satırda ve mesaj doğru."""
    first = run_tier0(_fixture_code(fixture)).diagnostics[0]
    assert first.line == fixture.expected_line
    assert "noktalı virgül" in first.message


def test_csharp_initializer_confusion_reports_semicolon() -> None:
    code = (
        "class A {\n    void F(int[] a) {\n        foreach (var v in a) {\n"
        "            t += v\n        }\n    }\n}\n"
    )
    diag = run_tier0(_code(code, Language.CSHARP)).diagnostics[0]
    assert (diag.line, diag.column) == (4, len("            t += v") + 1)
    assert "noktalı virgül" in diag.message


@pytest.mark.parametrize(
    ("language", "code", "opened"),
    [
        (Language.CPP, "#include <string>\nclass A {\npublic:\n    int x;\n", "Satır 2 ile"),
        (
            Language.CSHARP,
            "namespace N\n{\n    class A\n    {\n        int x;\n    }\n",
            "Satır 2 ile",
        ),
    ],
)
def test_unclosed_block_reported_at_end(language: Language, code: str, opened: str) -> None:
    normalized = _code(code, language)
    result = run_tier0(normalized)
    last = result.diagnostics[-1]
    assert last.line == len(normalized.lines)
    assert "kapanmamış" in last.message
    assert opened in last.message


@pytest.mark.parametrize(
    ("name", "opened"),
    [
        ("c/invalid/missing_brace.c", 7),
        ("cpp/invalid/missing_brace.cpp", 3),
        ("csharp/invalid/missing_brace.cs", 4),
    ],
)
def test_missing_brace_fixtures_name_opening_line(name: str, opened: int) -> None:
    fixture = next(f for f in INVALID if f.id == name)
    messages = [d.message for d in run_tier0(_fixture_code(fixture)).diagnostics]
    assert any(f"Satır {opened} ile başlayan blok kapanmamış" in m for m in messages), messages


def test_unclosed_summary_survives_diagnostic_cap() -> None:
    body = "\n".join("    int x = @;" for _ in range(30))
    result = run_tier0(_code("int main(void) {\n" + body + "\n", Language.C))
    assert len(result.diagnostics) == MAX_DIAGNOSTICS
    assert result.truncated
    assert "kapanmamış" in result.diagnostics[-1].message


def test_unclosed_block_with_trailing_comment() -> None:
    code = _code(
        "class A {\npublic:\n    int x;\n// son yorum\n/* bir tane daha */\n", Language.CPP
    )
    result = run_tier0(code)
    assert any("kapanmamış" in d.message for d in result.diagnostics)
    assert max(d.line for d in result.diagnostics) == len(code.lines)


def test_braces_inside_strings_and_comments_are_not_counted() -> None:
    code = 'int main(void) {\n    const char *s = "{{{";\n    /* { */\n    return 0;\n}\n'
    assert not run_tier0(_code(code, Language.C)).has_errors


def test_column_counts_characters_not_bytes() -> None:
    line = '    const char *s = "ğüşöçı"; @'
    code = _code("int main(void) {\n" + line + "\n}\n", Language.C)
    diag = next(d for d in run_tier0(code).diagnostics if d.line == 2)
    assert diag.column == line.index("@") + 1


def test_column_correct_after_neutralized_macro_with_unicode() -> None:
    line = '    UPROPERTY(meta = (DisplayName = "Öğe")) int32 X = 1 @;'
    code = _code("UCLASS()\nclass AFoo\n{\n" + line + "\n};\n", Language.CPP, Engine.UNREAL)
    diag = next(d for d in run_tier0(code).diagnostics if d.line == 4)
    assert diag.column == line.index("@") + 1


def test_diagnostics_capped_and_sorted() -> None:
    body = "\n".join("    int x = @;" for _ in range(100))
    result = run_tier0(_code("int main(void) {\n" + body + "\n}\n", Language.C))
    assert 0 < len(result.diagnostics) <= MAX_DIAGNOSTICS
    assert result.truncated
    positions = [(d.line, d.column or 0) for d in result.diagnostics]
    assert positions == sorted(positions)


@pytest.mark.parametrize("fixture", VALID, ids=lambda f: f.id)
def test_repeated_fixture_does_not_crash(fixture: Tier0Fixture) -> None:
    """Regresyon: 600 satıra tekrarlanan dosyalar hata içerir ve eskiden çöküyordu."""
    lines = fixture.text.splitlines()
    text = "\n".join((lines * (600 // len(lines) + 1))[:600])
    result = run_tier0(_code(text, fixture.language, fixture.engine))
    assert len(result.diagnostics) <= MAX_DIAGNOSTICS


# ---------------------------------------------------------------- performans


@pytest.mark.slow
@pytest.mark.parametrize("fixture", [f for f in VALID if f.path.stat().st_size > 1000][:3])
def test_tier0_under_50ms(fixture: Tier0Fixture) -> None:
    lines = fixture.text.splitlines()
    text = "\n".join((lines * (600 // len(lines) + 1))[:600])
    code = _code(text, fixture.language, fixture.engine)
    run_tier0(code)  # ısınma (parser önbelleği)
    timings = []
    for _ in range(5):
        start = time.perf_counter()
        run_tier0(code)
        timings.append(time.perf_counter() - start)
    assert min(timings) < 0.050, f"{min(timings) * 1000:.1f} ms"
