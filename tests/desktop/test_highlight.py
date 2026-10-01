"""Editör sözdizimi renklendirmesi."""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from codementor.desktop.highlight import tokenize
from codementor.models.enums import Language


def kinds(code: str, language: Language) -> dict[str, str]:
    return {code[s:e]: kind for kind, s, e in tokenize(code, language)}


def test_basic_c_tokens() -> None:
    found = kinds("#include <stdio.h>\nint main(void) { return 42; } // for\n", Language.C)
    assert found["#include <stdio.h>"] == "preproc"
    assert found["int"] == "type"
    assert found["main"] == "function"
    assert found["return"] == "keyword"
    assert found["42"] == "number"
    assert found["// for"] == "comment"


def test_keywords_inside_strings_and_comments_are_not_split() -> None:
    code = 'char *s = "while if";\n/* return\n for */ int x;'
    spans = tokenize(code, Language.C)
    words = [code[s:e] for kind, s, e in spans if kind == "keyword"]
    assert words == []
    assert '"while if"' in [code[s:e] for kind, s, e in spans if kind == "string"]


def test_language_specific_words() -> None:
    assert kinds("nullptr;", Language.CPP)["nullptr"] == "keyword"
    assert "nullptr" not in kinds("nullptr;", Language.C)
    assert kinds("foreach (var s in xs)", Language.CSHARP)["foreach"] == "keyword"


def test_unterminated_block_comment_runs_to_end() -> None:
    code = "int a; /* açık"
    assert tokenize(code, Language.C)[-1] == ("comment", 7, len(code))


@given(st.text(max_size=300), st.sampled_from(list(Language)))
def test_spans_are_sorted_non_overlapping_and_in_bounds(code: str, language: Language) -> None:
    previous_end = 0
    for _kind, start, end in tokenize(code, language):
        assert previous_end <= start < end <= len(code)
        previous_end = end
