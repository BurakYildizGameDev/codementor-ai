"""Yorum/metin maskeleme ve parantez eşleme testleri."""

from __future__ import annotations

import time

import pytest
from hypothesis import given
from hypothesis import strategies as st

from codementor.analysis.lexical import mask_non_code, matching_parens
from codementor.models.enums import Language


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


# ---------------------------------------------------------- C++ ham metin (Faz 55)


@pytest.mark.parametrize(
    ("code", "kept", "dropped"),
    [
        # tek satır: içerikteki `"(` string'i bitirmez, `b)"` kod sayılmaz
        ('const char* s = R"(a"b)";', ['const char* s = R"(', ')";'], ['a"b']),
        # özel delimiter: `)"b` içerikte kalır, yalnız `)x"` kapatır
        ('const char* s = R"x(a)"b)x";', ['R"x(', ')x";'], [')"b']),
        # önekli biçimler
        ('const char* s = u8R"(a"b)";', ['u8R"(', ')";'], ['a"b']),
        ('const char* s = UR"(a"b)";', ['UR"(', ')";'], ['a"b']),
        ('const char* s = LR"x(a)"b)x";', ['LR"x(', ')x";'], [')"b']),
        # çok satırlı: yorum, tırnak, ayraç ve include görünümlü içerik
        (
            'const char* s = R"(multi\n/* yorum\n// satır\n{ } #include "e.h"\n)";\nint x;',
            ['R"(', ')";', "\nint x;"],
            ["yorum", "e.h", "{ }"],
        ),
        # kapanmamış ham metin: dosya sonuna kadar maskele
        ('const char* s = R"(open\n/* x', ['R"(', "\n"], ["open", "/* x"]),
        # önek tanımlayıcının parçasıysa ham metin değildir (normal string)
        ('int FOO_R"(x)";', ['FOO_R"', '";'], ["(x)"]),
        # `R` adlı değişken ham metin açmaz
        ("int R = 1; R + 1;", ["int R = 1; R + 1;"], []),
    ],
)
def test_raw_string_masking(code: str, kept: list[str], dropped: list[str]) -> None:
    masked = mask_non_code(code)
    assert len(masked) == len(code)
    for part in kept:
        assert part in masked, part
    for part in dropped:
        assert part not in masked, part


def test_raw_string_delimiter_length_boundary() -> None:
    """`delim` en fazla 16 karakter (C++ standardı): 16'sı ham metin, 17'si değil."""
    ok, bad = "d" * 16, "d" * 17
    raw = f'const char* s = R"{ok}(a"b){ok}";'
    masked = mask_non_code(raw)
    assert f'R"{ok}(' in masked  # açılış görünür kalır
    assert f'){ok}"' in masked  # kapanış görünür kalır
    assert 'a"b' not in masked  # içerik maskelendi

    not_raw = f'const char* s = R"{bad}(a"b){bad}";'
    masked = mask_non_code(not_raw)
    assert f'R"{bad}(' not in masked  # ham metin değil: normal string olarak maskelendi


def test_raw_string_inner_parens_not_matched() -> None:
    """Ham metin içeriğindeki parantezler eşlenmez; açılış/kapanış kendi aralarında eşleşir."""
    masked = mask_non_code('f(R"x((1))x");')
    assert matching_parens(masked) == {1: 12, 5: 9}


def test_raw_string_content_after_include_is_masked() -> None:
    """`#include "..."` istisnası ham metnin içeriğini maskellemekten alıkoymaz."""
    code = '#include "CoreMinimal.h"\nconst char* s = R"(UCLASS() GENERATED_BODY())";\n'
    masked = mask_non_code(code)
    assert masked.startswith('#include "CoreMinimal.h"\n')
    assert "UCLASS" not in masked
    assert "GENERATED_BODY" not in masked


@given(st.text(alphabet=st.sampled_from(list("ab(){}/*\"'\\@\n ;1_Ru8Lx#<>=")), max_size=300))
def test_mask_preserves_length_and_newlines_with_raw_strings(code: str) -> None:
    masked = mask_non_code(code)
    assert len(masked) == len(code)
    assert [i for i, c in enumerate(masked) if c == "\n"] == [
        i for i, c in enumerate(code) if c == "\n"
    ]


@pytest.mark.parametrize(
    "hostile",
    ['R"x(' * 10_000 + ')x"', 'R"x()x"' * 5_000, 'u8R"(' * 8_000],
    ids=["one-huge-raw", "many-closed-raws", "prefixed-unclosed"],
)
def test_linear_time_on_hostile_raw_strings(hostile: str) -> None:
    start = time.perf_counter()
    masked = mask_non_code(hostile)
    matching_parens(masked)
    assert time.perf_counter() - start < 0.5


# ---------------------------------------------------------- C# 11 ham metin (Faz H3)


def test_csharp_raw_string_content_is_masked() -> None:
    """Ham metin içindeki `//`, `/*` ve tırnak, yorum/metin sanılmaz (dil verilince)."""
    code = (
        "class A\n"
        "{\n"
        '    string s = """\n'
        "    // yorum değil (\n"
        "    /* blok değil */\n"
        '    " tırnak\n'
        '    """;\n'
        "    int x = 1;\n"
        "}\n"
    )
    masked = mask_non_code(code, Language.CSHARP)
    assert len(masked) == len(code)
    assert masked.startswith('class A\n{\n    string s = """\n')
    assert masked.endswith('""";\n    int x = 1;\n}\n')
    for dropped in ("yorum değil", "blok değil", '" tırnak'):
        assert dropped not in masked, dropped
    # açılış/kapanış dizileri yerinde: parantez eşleme şaşmaz
    assert matching_parens(masked) == matching_parens(code)


@pytest.mark.parametrize("dollars", ["", "$", "$$"])
def test_csharp_interpolated_raw_string_is_masked(dollars: str) -> None:
    code = f'string s = {dollars}"""\n{{ değer }} // yorum\nsondaki tırnak: "\n""";\n'
    masked = mask_non_code(code, Language.CSHARP)
    assert len(masked) == len(code)
    assert f'{dollars}"""' in masked
    for dropped in ("değer", "yorum", 'tırnak: "'):
        assert dropped not in masked, dropped


def test_csharp_raw_string_does_not_hide_following_code() -> None:
    """Ham metinden sonraki gerçek yorumlar maskelenmeye devam eder."""
    code = 'string a = """x // y""";\nstring b = "gerçek"; // maskelenmeli\n'
    masked = mask_non_code(code, Language.CSHARP)
    assert "x // y" not in masked
    assert "gerçek" not in masked
    assert "maskelenmeli" not in masked


@pytest.mark.parametrize(
    ("code", "kept", "dropped"),
    [
        # uzun kapanış dizisi: 4 tırnakla açılan ham metni 3 tırnak kapatmaz
        ('string s = """"iç "" x"""";', '""""', ["iç ", '"" x']),
        # kapanmış ve dosya sonunda biten ham metin: kapanış tırnakları yerinde kalır
        ('string s = """x//y"""', '"""', ["x//y"]),
        # kapanmamış ham metin: dosya sonuna kadar maskele (satırlar korunur)
        ('string s = """\nkapanmadı // x\n" tırnak\n', '"""', ["kapanmadı", "tırnak"]),
    ],
)
def test_csharp_raw_string_edge_cases(code: str, kept: str, dropped: list[str]) -> None:
    masked = mask_non_code(code, Language.CSHARP)
    assert len(masked) == len(code)
    assert kept in masked
    assert [i for i, c in enumerate(masked) if c == "\n"] == [
        i for i, c in enumerate(code) if c == "\n"
    ]
    for part in dropped:
        assert part not in masked, part


def test_csharp_verbatim_string_still_wins_over_raw() -> None:
    """`@\"...\"` C# verbatim metindir: ham metin sayılmaz, `\"\"` kaçışı korunur."""
    code = 'string s = @"satır "" ve // yorum";\nint x = 1;\n'
    masked = mask_non_code(code, Language.CSHARP)
    assert "satır" not in masked
    assert "yorum" not in masked
    assert masked.endswith(";\nint x = 1;\n")


def test_raw_string_masking_only_with_csharp_language() -> None:
    """Dil verilmezse (ya da C/C++ ise) üç tırnak özel değildir: davranış değişmez."""
    code = 'string s = """\n// bu satır gerçek yorum\n""";\nint x = 1;\n'
    assert "bu satır gerçek yorum" not in mask_non_code(code)
    assert "bu satır gerçek yorum" not in mask_non_code(code, Language.CPP)


def test_csharp_raw_string_keeps_line_and_length_on_hostile_input() -> None:
    hostile = ('string s = """' + "x" * 10 + '"""\n') * 1_000
    start = time.perf_counter()
    masked = mask_non_code(hostile, Language.CSHARP)
    assert len(masked) == len(hostile)
    assert masked.count("\n") == hostile.count("\n")
    assert time.perf_counter() - start < 0.5


@pytest.mark.parametrize(
    "hostile",
    ['"""' * 13_000, 'x = "' * 20_000, ('string s = """' + "a" * 40 + "\n") * 900],
    ids=["many-quotes", "open-quotes", "many-open-raws"],
)
def test_csharp_hostile_input_is_linear(hostile: str) -> None:
    start = time.perf_counter()
    masked = mask_non_code(hostile, Language.CSHARP)
    matching_parens(masked)
    assert len(masked) == len(hostile)
    assert time.perf_counter() - start < 0.5


@given(st.text(alphabet=st.sampled_from(list("ab(){}/*\"'\\@\n ;1_$")), max_size=300))
def test_csharp_mask_preserves_length_and_newlines(code: str) -> None:
    masked = mask_non_code(code, Language.CSHARP)
    assert len(masked) == len(code)
    assert [i for i, c in enumerate(masked) if c == "\n"] == [
        i for i, c in enumerate(code) if c == "\n"
    ]
