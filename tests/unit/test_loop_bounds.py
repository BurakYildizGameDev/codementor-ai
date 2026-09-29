"""Döngü sınır sınıfı testleri (mimari §5.3.1 desen tablosu).

Her vaka tek bir döngü içeren küçük bir fonksiyondur; emin olunamayan desenler `UNKNOWN`.
"""

from __future__ import annotations

import pytest

from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language, LoopBound
from codementor.models.request import LanguageHint

C, CPP, CS = Language.C, Language.CPP, Language.CSHARP


def _bounds(body: str, language: Language) -> list[LoopBound]:
    if language is CS:
        text = f"class A {{\n  void F(int n, int[] arr, List<int> list) {{\n{body}\n  }}\n}}\n"
    else:
        text = f"void f(int n, int *arr) {{\n{body}\n}}\n"
    code = normalize(text, LanguageHint(language=language, engine=Engine.NONE))
    facts = extract_facts(code)
    assert not facts.warnings, facts.warnings
    return [loop.bound for loop in facts.loops]


LINEAR = [
    ("for (int i = 0; i < n; i++) {}", C),
    ("for (int i = 0; i <= n - 1; ++i) {}", C),
    ("for (int i = n - 1; i >= 0; i--) {}", C),
    ("for (i = 0; i < strlen(s); i += 1) {}", C),
    ("for (int i = 0; n > i; i++) {}", C),
    ("for (int i = 0, j = n - 1; i < j; i++, j--) {}", C),
    ("int i = 0; while (i < n) { i++; }", C),
    ("while (n > 0) { n--; }", C),
    ("do { n -= 1; } while (n > 0);", C),
    ("for (size_t i = 0; i < v.size(); ++i) {}", CPP),
    ("for (auto& x : v) {}", CPP),
    ("int i = 0; while (i < n) { ++i; }", CPP),
    ("do { --n; } while (n > 0);", CPP),
    ("for (const auto& [k, val] : m) {}", CPP),
    ("for (int i = 0; i < arr.Length; i++) {}", CS),
    ("for (int i = 0; i < list.Count; i++) {}", CS),
    ("foreach (var x in list) {}", CS),
    ("int j = 0; while (j < n && arr[j] < 5) { j++; }", CS),
    ("int l = 0, r = n - 1; while (l < r) { l++; r--; }", CS),
]

LOG = [
    ("for (int i = 1; i < n; i *= 2) {}", C),
    ("for (int i = n; i > 0; i /= 2) {}", C),
    ("for (int i = n; i > 0; i >>= 1) {}", C),
    ("for (int i = 1; i < n; i = i * 2) {}", C),
    ("while (n > 1) { n /= 2; }", C),
    ("while (n > 0) { n = n >> 1; }", CPP),
    (
        "int lo = 0, hi = n;\n"
        "while (lo < hi) { int mid = (lo + hi) / 2;"
        " if (arr[mid] < 3) lo = mid + 1; else hi = mid; }",
        CPP,
    ),
    (
        "int lo = 0, hi = n - 1;\n"
        "while (lo <= hi) { int mid = lo + (hi - lo) / 2;"
        " if (arr[mid] < 3) lo = mid + 1; else hi = mid - 1; }",
        C,
    ),
    (
        "int lo = 0, hi = arr.Length - 1;\n"
        "while (lo < hi) { int mid = (lo + hi) >> 1;"
        " if (arr[mid] < 3) lo = mid + 1; else hi = mid; }",
        CS,
    ),
]

CONSTANT = [
    ("for (int i = 0; i < 10; i++) {}", C),
    ("for (int i = 0; i <= 3; ++i) {}", CPP),
    ("for (int i = 10; i > 0; i--) {}", C),
    ("for (int i = 0; i < 8; i++) {}", CS),
    ("int k = 0; while (k < 5) { k++; }", C),
]

UNKNOWN = [
    ("for (;;) { break; }", C),
    ("while (1) { break; }", C),
    ("while (true) { break; }", CS),
    ("for (int i = 0; i * i <= n; i++) {}", C),
    ("while (node != 0) { node = next(node); }", C),
    ("for (int i = 0; i < n; i = next(i)) {}", C),
    ("for (int i = 0; i < n;) { i = arr[i]; }", C),
    ("while (Check()) {}", CS),
]


def _ids(cases: list[tuple[str, Language]]) -> list[str]:
    return [f"{lang.value}:{body[:40]}" for body, lang in cases]


@pytest.mark.parametrize(("body", "language"), LINEAR, ids=_ids(LINEAR))
def test_linear(body: str, language: Language) -> None:
    assert _bounds(body, language) == [LoopBound.LINEAR]


@pytest.mark.parametrize(("body", "language"), LOG, ids=_ids(LOG))
def test_log(body: str, language: Language) -> None:
    assert _bounds(body, language) == [LoopBound.LOG]


@pytest.mark.parametrize(("body", "language"), CONSTANT, ids=_ids(CONSTANT))
def test_constant(body: str, language: Language) -> None:
    assert _bounds(body, language) == [LoopBound.CONSTANT]


@pytest.mark.parametrize(("body", "language"), UNKNOWN, ids=_ids(UNKNOWN))
def test_unknown(body: str, language: Language) -> None:
    assert _bounds(body, language) == [LoopBound.UNKNOWN]


def test_loop_kinds() -> None:
    body = (
        "for (int i = 0; i < n; i++) {}\n"
        "while (n > 0) { n--; }\n"
        "do { n--; } while (n > 0);\n"
        "foreach (var x in list) {}\n"
    )
    code = normalize(
        f"class A {{ void F(int n, List<int> list) {{\n{body}}} }}\n",
        LanguageHint(language=CS),
    )
    assert [loop.kind for loop in extract_facts(code).loops] == ["for", "while", "do", "foreach"]


def test_cpp_range_for_is_foreach() -> None:
    code = normalize("void f() { for (int x : v) {} }\n", LanguageHint(language=CPP))
    assert extract_facts(code).loops[0].kind == "foreach"
