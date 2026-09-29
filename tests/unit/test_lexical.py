"""Yorum/metin maskeleme ve parantez eşleme testleri."""

from __future__ import annotations

import time

import pytest
from hypothesis import given
from hypothesis import strategies as st

from codementor.analysis.lexical import mask_non_code, matching_parens


@pytest.mark.parametrize(
    ("code", "kept", "dropped"),
    [
        ("a // yorum (\nb", ["a ", "\nb"], ["yorum", "("]),
        ("a /* çok\nsatır ( */ b", ["a ", " b"], ["çok", "satır", "(", "*/"]),
        ('printf("=> :: (");', ['printf("', '");'], ["=>", "::", " ("]),
        ("char c = '(';", ["char c = '", "';"], ["'('"]),
        ('s = "kaçış \\" ( devam";', ['s = "', '";'], ["kaçış", "devam", "("]),
        ('v = @"satır ""(""\nikinci";', ['v = @"', '";'], ["satır", "ikinci", "("]),
        ('u = "http://x.com"; // gerçek yorum', ['u = "', '";'], ["http", "gerçek"]),
        ("/* kapanmayan yorum (", [], ["kapanmayan", "("]),
        ('"kapanmayan metin (\nkod(', ['"', "\nkod("], ["metin"]),
    ],
)
def test_mask_non_code(code: str, kept: list[str], dropped: list[str]) -> None:
    masked = mask_non_code(code)
    assert len(masked) == len(code)
    for part in kept:
        assert part in masked, part
    for part in dropped:
        assert part not in masked, part


def test_include_paths_are_kept_but_following_strings_masked() -> None:
    code = '#include "CoreMinimal.h"\n#  include "a(b).h"\nconst char* s = "UCLASS(";'
    masked = mask_non_code(code)
    assert masked.startswith('#include "CoreMinimal.h"\n#  include "a(b).h"\n')
    assert "UCLASS" not in masked


def test_digit_separator_is_not_a_char_literal() -> None:
    code = "int n = 1'000'000; f(a);"
    assert mask_non_code(code) == code


@given(st.text(alphabet=st.sampled_from(list("ab(){}/*\"'\\@\n ;1_")), max_size=200))
def test_mask_preserves_length_and_newlines(code: str) -> None:
    masked = mask_non_code(code)
    assert len(masked) == len(code)
    assert [i for i, c in enumerate(masked) if c == "\n"] == [
        i for i, c in enumerate(code) if c == "\n"
    ]


def test_matching_parens() -> None:
    assert matching_parens("f(a(b), c)") == {1: 9, 3: 5}
    assert matching_parens("(()") == {1: 2}
    assert matching_parens(")(") == {}


@pytest.mark.parametrize(
    "hostile",
    ["/*a" * 13_000, '"a' * 20_000, "'(" * 20_000, "(" * 40_000, '@"' * 20_000],
    ids=["open-comments", "open-strings", "char-parens", "parens", "verbatim"],
)
def test_linear_time_on_hostile_input(hostile: str) -> None:
    start = time.perf_counter()
    mask_non_code(hostile)
    matching_parens(hostile)
    assert time.perf_counter() - start < 0.5
