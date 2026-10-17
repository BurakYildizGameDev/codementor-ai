"""Include koruması testleri (mimari §5.2.3): derleyiciden önce, maskelenmiş kodda."""

from __future__ import annotations

import pytest

from codementor.validation.include_guard import check_includes

REJECTED = {
    "abs_posix": '#include "/etc/shadow"\n',
    "abs_angle": "#include </etc/passwd>\n",
    "unc_path": '#include "//server/share/x.h"\n',
    "dotdot": '#include "../../secrets.h"\n',
    "dotdot_angle": "#include <sys/../../../etc/passwd>\n",
    "drive_letter": '#include "C:/Windows/win.ini"\n',
    "drive_relative": '#include "C:win.ini"\n',
    "backslash": '#include "sub\\x.h"\n',
    "macro_include": "#define P </etc/passwd>\n#include P\n",
    "include_next": '#include_next "/etc/passwd"\n',
    "import": '#import "/etc/passwd"\n',
    "import_macro": "#import FOO\n",
    "embed": '#embed "data.bin"\n',
    "has_include": "#if __has_include(<stdio.h>)\n#endif\n",
    "has_include_next": "#if __has_include_next(<x.h>)\n#endif\n",
    "has_embed": '#if __has_embed("x")\n#endif\n',
    "digraph": '%:include "/etc/passwd"\n',
    "line_splice_directive": '#inc\\\nlude "/etc/passwd"\n',
    "line_splice_path": '#include "/etc/\\\npasswd"\n',
    "spaced_hash": '  #   include   "/etc/passwd"\n',
    "trigraph": '??=include "/etc/passwd"\n',
    "pragma_dependency": '#pragma GCC dependency "/etc/passwd"\n',
    "pragma_operator": '_Pragma("GCC dependency \\"/etc/passwd\\"")\n',
    "comment_before_hash": '/* x */ #include "/etc/passwd"\n',
    "multiline_comment_before_hash": '/*\n*/#include "/etc/passwd"\n',
    "comment_before_target": '#include /* c */ "/etc/passwd"\n',
    "empty_target": '#include ""\n',
    "unterminated": '#include "stdio.h\n',
    # --- güvenlik denetimi (Faz 4) regresyonları
    "splice_with_trailing_space": '#inc\\ \nlude "/etc/passwd"\n',
    "splice_with_trailing_tab": '#include "/etc/\\\t\npasswd"\n',
    "form_feed_before_hash": '\f#include "/etc/passwd"\n',
    "vtab_after_hash": '#\vinclude "/etc/passwd"\n',
    "prefixed_char_opens_fake_comment": "int x = L'/*';\n#include \"/etc/passwd\"\n// */\n",
    "u8_char_opens_fake_comment": "auto c = u8'/*';\n#include </etc/passwd>\n// */\n",
    "ident_quote_opens_fake_comment": "int x = b'/*';\n#include </etc/passwd>\n// */\n",
    "raw_string_opens_fake_comment": 'auto s = R"(x"/*)";\n#include "/etc/passwd"\n// */\n',
    "at_quote_verbatim_in_c": 'int a = 1 @"\n#include "/etc/passwd"\n";\n',
    "token_paste_pragma": '#define C(a,b) a##b\nC(_Pra,gma)("GCC dependency \\"/x\\"")\n',
    "token_paste_has_include": "#define C(a,b) a##b\n#if C(__ha,s_include)(<x>)\n#endif\n",
    "partial_has": "#if __has_(x)\n#endif\n",
    "old_gcc_has_include": "#if __has_include__(<x>)\n#endif\n",
    "device_con": '#include "CON"\n',
    "device_com1_ext": '#include "com1.h"\n',
    "device_conin": '#include "CONIN$"\n',
    "unsafe_path_in_comment": '// #include "/etc/shadow"\n',
    "unsafe_path_in_string": 'const char* s = "#include </etc/passwd>";\n',
    # --- Faz A1 (K1): `#` ile yönerge adı arasına giren yorum
    "comment_between_hash_and_keyword": '#/**/include "/etc/passwd"\n',
    "digraph_comment_between": "%:/**/include </etc/passwd>\n",
    "multiline_comment_between": '#/*\n*/include "/etc/passwd"\n',
    "spaced_comment_between": '# /* a */ include "../x.h"\n',
    "two_comments_between": "#/**//**/include <stdio.h>\n",
    "comment_between_embed": '#/**/embed "data.bin"\n',
    # --- Faz H3: `#pragma` izin listesi ve `#line`
    "pragma_unknown": "#pragma bilesen_bilgisi\n",
    "pragma_macro_dependency": '#define X GCC dependency "/etc/passwd"\n#pragma X\n',
    "pragma_macro_dependency_digraph": '%:define X GCC dependency "/etc/x"\n%:pragma X\n',
    "pragma_lowercase_dependency": '#pragma gcc dependency "/etc/passwd"\n',
    "pragma_define_argument": "#pragma bilesen(1)\n",
    "pragma_after_comment": "/* x */ #pragma bilesen(1)\n",
    # `pack`/`warning` izinlidir ama ad eşleşmesi katı kalır: büyük harf, ekli ad ve
    # `dependency` sözcüğü fail-closed tarafında (pragma adları derleyicide de harf duyarlı).
    "pragma_pack_uppercase": "#pragma PACK(1)\n",
    "pragma_packable": "#pragma packable\n",
    "pragma_allowed_name_with_dependency": '#pragma warning(GCC dependency "/etc/passwd")\n',
    "define_once_macro": '#define once GCC dependency "/etc/passwd"\n',
    "define_region_macro": "#define region /* gizli */\n",
    "define_endregion_macro": "#define endregion 1\n",
    # İzin listesine eklenen adlar da makro atlatmasına kapalı olmalı (izin listesi ile
    # `_PRAGMA_RESERVED` birlikte büyür; aksi hâlde `#define pack GCC dependency "…"` +
    # `#pragma pack` host dosyası yoklar — ikinci vaka yalnız `#define` ile de düşer).
    "define_pack_macro_with_pragma": '#define pack GCC dependency "/etc/passwd"\n#pragma pack\n',
    "define_pack_macro": "#define pack 4\n",
    "define_warning_macro": "#define warning 1\n#pragma warning(disable: 1)\n",
    "line_with_filename": '#line 1 "/etc/passwd"\n',
    "line_with_relative_filename": '#line 7 "yol/../x.c"\n',
    "line_with_macro": "#line __LINE__\n",
    "line_comment_split": '#/**/line 1 "/etc/passwd"\n',
    "line_after_comment": '/* x */ #line 1 "a.c"\n',
}

ALLOWED = {
    "stdio": "#include <stdio.h>\nint main(void) { return 0; }\n",
    "local_quote": '#include "my_header.h"\n',
    "nested_angle": "#include <sys/types.h>\n",
    "unreal_generated": '#include "Enemy.generated.h"\n',
    "subdir": '#include "Engine/World.h"\n',
    "no_includes": "int x = 1;\n",
    "division_not_path": "int a = 4 / 2;\n",
    "comment_after_include": "#include <stdio.h> /* g/ç */\n",
    "hash_in_comment_then_word": "/* # */ int include_count = 0;\n",
    # --- Faz H3: izin listesindeki biçimler ve yorum/metindeki geçişler
    "pragma_once": "#pragma once\n",
    "pragma_once_with_comment": "#pragma once // koruma\n",
    "pragma_region": "#pragma region Gizli bölge\nint x = 1;\n#pragma endregion\n",
    "pragma_region_digraph": "%:pragma region\n",
    # --- Faz H denetimi kararı (2026-10-17): `pack`/`warning` izin listesine alındı;
    # bunlar hiçbir dosyayı okumaz, öncesinde bu dosyalar Tier 1'i gereksiz atlıyordu.
    "pragma_pack": "#pragma pack(push, 1)\n",
    "pragma_pack_argument": "#pragma pack(2)\n",
    "pragma_pack_reset": "#pragma pack()\n",
    "pragma_pack_pop": "#pragma pack(pop, bilesen)\n",
    "pragma_pack_digraph": "%:pragma pack(1)\n",
    "pragma_pack_after_comment": "/* x */ #pragma pack(1)\n",
    "pragma_warning": "#pragma warning(disable: 4996)\n",
    "pragma_warning_push": "#pragma warning(push, 0)\n",
    "pragma_warning_in_string": 'const char* s = "#pragma warning(disable: 1)";\n',
    # (yorum/metin içindeki `pack` geçişleri `pragma_in_comment` / `pragma_in_string`
    # vakalarıyla kapsanıyor)
    "pragma_in_comment": "// #pragma pack(1) kullanma\n",
    "pragma_in_string": 'const char* s = "#pragma pack(1)";\n',
    "define_not_reserved": "#define PAKET_BOYU 32\n",
    "line_number": "#line 42\nint x = 1;\n",
    "line_number_spaced": "#   line   42   \n",
    "line_number_digraph": "%:line 42\n",
    "line_in_comment": '// #line 1 "/etc/passwd" ekleme\n',
    "line_in_string": 'const char* s = "#line 1 x.c";\n',
}


@pytest.mark.parametrize("code", REJECTED.values(), ids=REJECTED.keys())
def test_rejects(code: str) -> None:
    reasons = check_includes(code)
    assert reasons, code
    assert all(r.strip() for r in reasons)


@pytest.mark.parametrize("code", ALLOWED.values(), ids=ALLOWED.keys())
def test_allows(code: str) -> None:
    assert check_includes(code) == []


def test_safe_includes_in_comments_and_strings_are_ignored() -> None:
    """Yorum/metindeki güvenli include'lar ve düzyazı engel değildir.

    Güvenli olmayan yollar ise yorum/metinde bile reddedilir (fail-closed): sözcük
    maskeleyicisi derleyiciyle her durumda aynı ayrımı yapamaz (`L'`, `R"`, `b'` ...).
    """
    code = (
        "// #include <vector>\n"
        "/* use #include to add headers */\n"
        'const char* s = "#include \\"my.h\\"";\n'
        "#include <stdio.h>\n"
    )
    assert check_includes(code) == []


def test_directive_after_comment_end_with_macro_rejected() -> None:
    assert check_includes("/* a\n*/ #include P\n")


@pytest.mark.parametrize("code", ["#define CAT(a, b) a##b\n", "int a = 1; // x %:%: y\n"])
def test_token_pasting_rejected(code: str) -> None:
    assert check_includes(code)


@pytest.mark.parametrize(
    "code",
    [
        # denetim: `_Pragma("GCC dependency ...")` ile host dosyası yoklanabiliyordu
        '#define P(a,b) a#\\\n#b\nP(_Pra,gma)("GCC dependency \\"C:/Windows/win.ini\\"")\n',
        "#define P(a,b) a%:\\\n%:b\n",
        "#define P(a,b) a#\\  \n#b\n",  # `\` ile satır sonu arası boşluk (gcc/clang kabul eder)
    ],
)
def test_token_pasting_split_by_line_splice_rejected(code: str) -> None:
    reasons = check_includes(code)
    assert any("token yapıştırma" in r for r in reasons), reasons
    assert any(r.startswith("Satır 1") for r in reasons)


def test_reason_mentions_line_number() -> None:
    code = 'int a;\n\n#include "/etc/shadow"\n'
    (reason,) = check_includes(code)
    assert "3" in reason


def test_line_number_survives_line_splices() -> None:
    code = "#define X 1 \\\n  + 2\n#include </etc/passwd>\n"
    (reason,) = check_includes(code)
    assert "3" in reason


def test_linear_on_adversarial_input() -> None:
    import time

    code = ("#include <a.h>\n" + "\\\n" * 5000 + '"' * 5000 + "/*" * 5000) * 2
    start = time.perf_counter()
    check_includes(code)
    assert time.perf_counter() - start < 1.0


def test_valid_fixtures_have_no_false_positives() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "fixtures" / "tier0"
    for path in [*root.glob("c/valid/*"), *root.glob("cpp/valid/*")]:
        assert check_includes(path.read_text(encoding="utf-8")) == [], path.name


# ------------------------------------------------- C++ ham metin gerilemesi (Faz 55)


def test_raw_string_does_not_hide_absolute_include() -> None:
    """Ham metin maskelemesi doğru olsa da koruma ham (maskesiz) metinde taranır;
    kapanan ham metinden sonraki mutlak yol include'u reddedilmeye devam eder."""
    code = 'const char* s = R"(\n/*\n)";\n#include "/etc/passwd"\n// */\nint main(){return 0;}\n'
    (reason,) = check_includes(code)
    assert "4" in reason
    assert "mutlak yol" in reason


def test_include_inside_raw_string_still_rejected() -> None:
    """Fail-closed: ham metin İÇİNDEKİ `#include` da reddedilir (Tier 1 atlanır).

    Derleyici o satırı string olarak görür; ancak maskeleyicinin ham metin
    ayrımında bir hata olsa bile koruma maskelenmemiş metinde arandığından
    güvenli yönde hata verir.
    """
    code = 'const char* s = R"(\n#include "/etc/passwd"\n)";\nint main(){return 0;}\n'
    (reason,) = check_includes(code)
    assert "2" in reason
    assert "mutlak yol" in reason


def test_safe_include_inside_raw_string_allowed() -> None:
    """Ham metin içindeki güvenli görünümlü include yanlış pozitif üretmez."""
    code = 'const char* s = R"(#include <stdio.h>\n)";\nint main(){return 0;}\n'
    assert check_includes(code) == []
