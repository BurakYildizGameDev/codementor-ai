"""`analysis/` + `rules/` + `verify/` desenlerinin en kötü girdide süre bütçesi (mimari §12).

KALAN_ISLER.md iş 4 (Bulgular §10 K2 kalan taraması): desenler kötü niyetli girdiyle
ölçülür. Tarama beş süper-doğrusal desen buldu ve doğrusallaştırıldı:

- `call_costs._LAST_INDEX` / `_END_INDEX` (sınırsız taban sınıfı → sondan çapalı desen),
- `leak_guard._ASSIGNMENT` (sınırsız sol/sağ taraf → sözcük sınırı + sınırlı, sahiplenici sınıflar),
- `leak_guard` yorum/metin taraması (karesel `.*?` → tek geçişli tarayıcı),
- `complexity._TRAILER` (baştaki `\\s*` → `_before_trailer`).

Desenler **otomatik keşfedilir**: yeni bir modül düzeyi desen eklendiğinde de bütçe ve
büyüme kontrolü kapsar. Eşdeğerlik testleri eski desenleri karşılaştırma ölçütü olarak tutar.
"""

from __future__ import annotations

import importlib
import pkgutil
import re
import time
from collections.abc import Callable

import pytest
from hypothesis import example, given
from hypothesis import settings as hyp_settings
from hypothesis import strategies as st

from codementor.analysis.call_costs import _END_INDEX, _LAST_INDEX, _index_base
from codementor.verify.complexity import _before_trailer
from codementor.verify.leak_guard import _ASSIGNMENT, strip_comments_and_strings
from tests.timing import deadline as _deadline

_PACKAGES = ("codementor.analysis", "codementor.rules", "codementor.verify")
_SIZE = 40_960  # kullanıcı kodu sınırı (40 KB, mimari §12)
_BUDGET_S = 0.05  # desen başına en kötü girdi bütçesi (KALAN_ISLER.md iş 4)
_GROWTH = 8.0  # 4x uzunlukta 8x'ten fazla artış süper-doğrusal sayılır
_MIN_PATTERNS = 40  # keşif bozulursa (import hatası vb.) test sessizce boş kalmasın


def _discover() -> list[tuple[str, re.Pattern[str]]]:
    """Paketlerdeki modül düzeyi derlenmiş desenler (ad → desen, sıralı)."""
    found: dict[str, re.Pattern[str]] = {}
    for package in _PACKAGES:
        root = importlib.import_module(package)
        for info in pkgutil.walk_packages(root.__path__, package + "."):
            for attr, value in vars(importlib.import_module(info.name)).items():
                if isinstance(value, re.Pattern):
                    found[f"{info.name}::{attr}"] = value
    return sorted(found.items())


PATTERNS = _discover()
_IDS = [name for name, _ in PATTERNS]


def _payloads(n: int) -> dict[str, str]:
    """En kötü girdi aileleri: sınırsız sınıfın kaotik tekrarı ve kapanmayan son."""
    half = n // 2
    return {
        "letter-run": "a" * n,
        "digit-run": "0" * n,
        "underscore-run": "_" * half + "=;",
        "space-run": " " * n,
        "space-junk": " " * (n - 1) + "!",
        "newline-run": "\n" * n,
        "paren-run": "(" * n,
        "open-block-comment": "/*a" * (n // 3),
        "comment-marks": "/*" * half,
        "unclosed-string": '"a' * half,
        "unclosed-char": "'a" * half,
        "escaped-quotes": '"\\' * half,
        "at-strings": '@"a' * (n // 3),
        "count-chain": "a.Count" * (n // 7),
        "count-tail": "a" * half + ".Count - 1",
        "assign-repeat": "=b" * half,
        "unreal-run": "UPROPERTY(" * (n // 10),
        "include-run": "#include" + " " * (n - 8),
    }


_FAMILIES: dict[str, Callable[[int], str]] = {
    name: (lambda n, name=name: _payloads(n)[name]) for name in _payloads(4)
}


def _measure(pattern: re.Pattern[str], text: str) -> float:
    """Bütçe ölçümü: CPU saati, en iyi dört koşu.

    Windows'ta `process_time` kuantumu ~15,6 ms'dir: hızlı desenler 0 okunur (yanlış kırmızı
    olmaz), bütçeyi aşan desen en az bir kuantum gösterir. Diğer süreçlerin yükü ölçüme
    girmez — bu yüzden bütçe testi duvar saati değil CPU saati kullanır.
    """
    best = float("inf")
    for _ in range(4):
        start = time.process_time()
        pattern.search(text)
        best = min(best, time.process_time() - start)
    return best


def _measure_wall(pattern: re.Pattern[str], text: str) -> float:
    """Büyüme ölçümü: `perf_counter` (yüksek çözünürlük) ve beş koşunun en iyisi.

    Oran karşılaştırması ince değerlere duyarlı olduğundan burada kuantumlu CPU saati
    kullanılamaz; en iyi koşu sıralayıcı gürültüsünü eler.
    """
    best = float("inf")
    for _ in range(5):
        start = time.perf_counter()
        pattern.search(text)
        best = min(best, time.perf_counter() - start)
    return best


def test_discovery_covers_the_packages() -> None:
    """Keşif sessizce boşalırsa bütçe testleri hiçbir şeyi ölçmez (alt sınır)."""
    assert len(PATTERNS) >= _MIN_PATTERNS, _IDS


@pytest.mark.parametrize(("name", "pattern"), PATTERNS, ids=_IDS)
def test_hostile_input_stays_within_budget(name: str, pattern: re.Pattern[str]) -> None:
    """Desen başına < 50 ms: 40 KB kötü niyetli girdide karesel/kübik davranış yok (§12)."""
    limit = _deadline(_BUDGET_S)
    for family, build in _FAMILIES.items():
        elapsed = _measure(pattern, build(_SIZE))
        assert elapsed < limit, f"{name} [{family}] {elapsed * 1000:.1f} ms"


@given(
    index=st.integers(min_value=0, max_value=len(PATTERNS) - 1),
    family=st.sampled_from(sorted(_FAMILIES)),
    size=st.integers(min_value=4_000, max_value=8_000),
)
@hyp_settings(deadline=None, max_examples=125)
def test_growth_is_linear_on_hostile_input(index: int, family: str, size: int) -> None:
    """Uzunluk eğrisi: 4x girdi 8x'ten fazla süre üretmez (doğrusal kalır).

    2 ms taban, sıralayıcı gürültüsüne ve ölçüm tabanına karşı paydır: eski (karesel)
    desenler bu aralıkta bile 16x büyüdüğü için kontrol onları yakalar (bkz. iş 4 kanıtı).
    """
    name, pattern = PATTERNS[index]
    small = _measure_wall(pattern, _FAMILIES[family](size))
    large = _measure_wall(pattern, _FAMILIES[family](size * 4))
    assert large <= _GROWTH * small + 0.002, (
        f"{name} [{family}] {small * 1000:.3f}→{large * 1000:.3f} ms"
    )


def _time_call(call: Callable[[str], object], text: str) -> float:
    """Bir girdi noktasının en iyi koşusu (`perf_counter`); sıralayıcı gürültüsü elenir."""
    best = float("inf")
    for _ in range(5):
        start = time.perf_counter()
        call(text)
        best = min(best, time.perf_counter() - start)
    return best


@pytest.mark.parametrize(
    ("label", "call", "hostile"),
    [
        ("comment-strip-open-block", strip_comments_and_strings, "/*a" * 13_000),
        ("comment-strip-open-string", strip_comments_and_strings, '"a' * 20_000),
        ("comment-strip-escaped-quotes", strip_comments_and_strings, '"\\' * 13_000),
        ("index-base-letter-run", lambda t: _index_base(t, _LAST_INDEX), "a" * 40_000),
        ("index-base-count-chain", lambda t: _index_base(t, _END_INDEX), "a.Count" * 5_000),
        ("assignment-underscore-run", _ASSIGNMENT.search, "_" * 40_000),
        ("assignment-eq-repeat", _ASSIGNMENT.search, "=b" * 13_000),
        ("trailer-space-run", _before_trailer, " " * 40_000),
        ("trailer-open-char", _before_trailer, "'a" * 13_000),
    ],
    ids=[
        "comment-strip-open-block",
        "comment-strip-open-string",
        "comment-strip-escaped-quotes",
        "index-base-letter-run",
        "index-base-count-chain",
        "assignment-underscore-run",
        "assignment-eq-repeat",
        "trailer-space-run",
        "trailer-open-char",
    ],
)
def test_fixed_entry_points_stay_fast(
    label: str, call: Callable[[str], object], hostile: str
) -> None:
    """K2'de düzeltilen desenlerin girdi noktaları 40 KB kötü niyetli girdide bütçe içinde."""
    elapsed = _time_call(call, hostile)
    assert elapsed < _deadline(_BUDGET_S), f"{label} {elapsed * 1000:.1f} ms"


# ------------------------------------------------- eski desenle eşdeğerlik (davranış korunur)

_LEGACY_COMMENTS_STRINGS = re.compile(
    r"//[^\n]*|/\*.*?\*/|@?\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'", re.DOTALL
)
_LEGACY_LAST_INDEX = re.compile(r"(?P<base>[A-Za-z_][\w.]*)\.(?:Count|Length)\s*-\s*1$")
_LEGACY_END_INDEX = re.compile(r"(?P<base>[A-Za-z_][\w.]*)\.(?:Count|Length)$")
_LEGACY_TRAILER = re.compile(
    r"\s*(?:\(|,|;|\bper\b|\bkare\b|\bher\b|\bamorti|\bworst\b|\baverage\b|\bbest\b"
    r"|\ben kötü\b|\bortalama\b|\bin the\b)",
    re.IGNORECASE,
)
_LEGACY_ASSIGNMENT = re.compile(r"[A-Za-z_][\w.\[\]<>]*\s*[+\-*/%|&^]?=\s*([^=\s][^;\n]*);")


def _legacy_base(arg: str, pattern: re.Pattern[str]) -> str | None:
    match = pattern.match(arg)
    return match.group("base") if match is not None else None


@pytest.mark.parametrize(
    "code",
    [
        "int a = 1; // HashSet kullan",
        'var s = "seenTargets";',
        "/* kapanmayan yorum (\nint x = 1;",
        '"kapanmayan metin (\nkod("ek"',
        'x = @"verbatim "" iç\ny = 1;',
        "a = 'c'; b = '\\''; c = // yorum\n\"d\";",
        '// tek satır "tırnak sahte\nint y = 2;',
        "",
        "/*a/*b/*c*/rest",
        'x = "kaçış \\" devam";',
    ],
    ids=[
        "line-comment",
        "string",
        "open-block",
        "open-strings",
        "verbatim",
        "char-escapes",
        "fake-quote-in-comment",
        "empty",
        "nested-open",
        "escaped-quote",
    ],
)
def test_comment_stripping_matches_legacy_pattern(code: str) -> None:
    """Tek geçişli tarayıcı eski desenle aynı metni üretir (yalnızca süre değişti)."""
    assert strip_comments_and_strings(code) == _LEGACY_COMMENTS_STRINGS.sub(" ", code)


@given(st.text(alphabet=st.sampled_from(list("ab(){}/*\"'\\@\n ;1_=.")), max_size=120))
# Kapanmayan `/*`'tan sonraki yorum/metin de silinir (hypothesis'in bulduğu karşı örnek)
@example("/*//")
@example("/*a // b\nc")
@example("/* 'x' /*")
@hyp_settings(deadline=None)
def test_comment_stripping_matches_legacy_pattern_on_random_text(code: str) -> None:
    assert strip_comments_and_strings(code) == _LEGACY_COMMENTS_STRINGS.sub(" ", code)


@pytest.mark.parametrize(
    "arg",
    [
        "xs.Count - 1",
        "xs.Count",
        "this.items.Count - 1",
        "a.b.Length - 1",
        "items.Count ",
        "i + 1",
        "a.Count.Count - 1",
        "a.Count + b.Count - 1",
        "0",
        "",
        "_x.Count-1",
        "xs[0].Count",
        "XS.Count -  1",
    ],
)
def test_index_base_matches_legacy_pattern(arg: str) -> None:
    """İndeks tabanı eski `(?P<base>…)` deseniyle aynı (yalnızca süre değişti)."""
    assert _index_base(arg, _LAST_INDEX) == _legacy_base(arg, _LEGACY_LAST_INDEX)
    assert _index_base(arg, _END_INDEX) == _legacy_base(arg, _LEGACY_END_INDEX)


@given(
    st.text(alphabet=st.sampled_from(list("abXL._-[]i 01\n")), max_size=40).map(
        lambda s: f"{s}Count - 1"
    )
)
@hyp_settings(deadline=None)
def test_index_base_matches_legacy_pattern_on_random_args(arg: str) -> None:
    assert _index_base(arg, _LAST_INDEX) == _legacy_base(arg, _LEGACY_LAST_INDEX)
    assert _index_base(arg, _END_INDEX) == _legacy_base(arg, _LEGACY_END_INDEX)


@pytest.mark.parametrize(
    "text",
    [
        "total = 0;",
        "x = f(y);",
        "  a += b[i];  ",
        "int x = 0; total = x;",
        "prose only",
        "",
    ],
)
def test_assignment_matches_legacy_pattern(text: str) -> None:
    """Atama deseni kod parçalarında eski desenle aynı (sınırlar yalnızca aşırı uzunlukta etkir)."""
    assert _ASSIGNMENT.findall(text) == _LEGACY_ASSIGNMENT.findall(text)


def test_assignment_bound_only_affects_oversized_statements() -> None:
    """Sınırlar bilinçli: tek deyim ölçeğinde cömert, üstünde kod parçası sayılmaz."""
    from codementor.verify.leak_guard import _MAX_ASSIGN_LHS, _MAX_ASSIGN_RHS

    assert _ASSIGNMENT.search(f"{'x' * _MAX_ASSIGN_LHS} = {'y' * _MAX_ASSIGN_RHS};") is not None
    assert _ASSIGNMENT.search(f"{'x' * (_MAX_ASSIGN_LHS + 8)} = 1;") is None
    assert _ASSIGNMENT.search(f"x = {'y' * (_MAX_ASSIGN_RHS + 8)};") is None


@pytest.mark.parametrize(
    "text",
    [
        "n^2 per frame",
        "n (kare başına)",
        "O(n) amortized",
        "en kötü n log n",
        "karesel, duruma göre",
        "n",
        "",
        "   n^2\t\tper frame",
    ],
)
def test_trailer_split_matches_legacy_pattern(text: str) -> None:
    """Açıklama ayıklama eski `\\s*(?:…)` ayırmıyla aynı sonucu verir."""
    assert _before_trailer(text) == _LEGACY_TRAILER.split(text, maxsplit=1)[0]


@given(st.text(alphabet=st.sampled_from(list("nO() ,;\tperköbadien")), max_size=60))
@hyp_settings(deadline=None)
def test_trailer_split_matches_legacy_pattern_on_random_text(text: str) -> None:
    assert _before_trailer(text) == _LEGACY_TRAILER.split(text, maxsplit=1)[0]
