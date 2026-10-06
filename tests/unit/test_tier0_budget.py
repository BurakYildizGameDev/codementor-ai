"""Tier 0 en kötü durum ayrıştırma süresi gerileme testleri (Faz 55, ADR-0024).

Ölçülen sınırlı girdiler `run_tier0` için < 1,5 s eşikle sabitlenir. C# gramerinin
`a<`×20000 girdisinde ~11,9 s sürdüğü (parse'ın kendisi) ADR-0024 kararıyla kabul
edilmiş bilinen risktir; süresi nedeniyle bilinçli olarak bu testin kapsamı dışıdır.
"""

from __future__ import annotations

import time

import pytest

from codementor.ingest.normalize import normalize
from codementor.models.enums import Language
from codementor.models.request import LanguageHint
from codementor.validation.tier0 import run_tier0


def _deadline(seconds: float) -> float:
    """Zaman sınırı; kapsama ölçümü yavaşlattığı için ölçümde genişletilir (Faz 53 kalıbı)."""
    try:
        from coverage import Coverage
    except ImportError:  # pragma: no cover
        return seconds
    return seconds * (4.0 if Coverage.current() is not None else 1.0)


def _valid_cpp(max_lines: int = 600, max_bytes: int = 39 * 1024) -> str:
    """Sınıra yakın geçerli C++: 80 üyeli struct + ~516 kısa fonksiyon (≈39 KB, 600 satır)."""
    head = "namespace n {\nstruct Data {\n"
    members = "".join(f"    int member_{i:03d} = {i};\n" for i in range(80))
    funcs: list[str] = []
    size = len(head) + len(members) + len("};\n") + len("}\n")
    lines = 84  # namespace(1) + struct(2) + 80 üye + `};` + kapanış `}`
    i = 0
    target = 72  # fonksiyon satırı hedef genişliği (bayt)
    while lines < max_lines and size + target + 1 <= max_bytes:
        base = f"int func_{i:03d}(int v) {{ return v * {i % 9 + 1} + member_{i % 80:03d}; }}"
        pad = target - len(base) - 4  # boşluk + `//` + dolgu
        line = base + " " + "//" + "-" * pad
        funcs.append(line + "\n")
        size += len(line) + 1
        lines += 1
        i += 1
    return head + members + "};\n" + "".join(funcs) + "}\n"


# Ölçülen en kötü sınırlı girdiler (PROGRESS Faz 55 tablosu; C# `a<` hariç, ADR-0024)
@pytest.mark.parametrize(
    ("language", "text"),
    [
        (Language.CPP, "a<" * 20000),  # 279 ms — şablon belirsizliği
        (Language.HTML, "<div>" * 6666),  # 564 ms — kapanmamış etiketler
        (Language.CSS, "{" * 40000),  # 52 ms — iç içe bloklar
        (Language.C, "(" * 40000),  # 24 ms — kapanmamış parantezler
    ],
    ids=["cpp-template-ambiguity", "html-unclosed-div", "css-nested-braces", "c-open-parens"],
)
def test_tier0_worst_bounded_inputs(language: Language, text: str) -> None:
    code = normalize(text, LanguageHint(language=language))
    run_tier0(code)  # ısınma: dil yüklemesi ölçüme karışmasın
    start = time.perf_counter()
    run_tier0(code)
    elapsed = time.perf_counter() - start
    assert elapsed < _deadline(1.5), f"{language.value}: {elapsed * 1000:.1f} ms"


def test_valid_cpp_near_limit_parses_clean() -> None:
    """Sınıra yakın geçerli C++ (≈39 KB, 600 satır) hatasız ayrışmalı (ADR-0024)."""
    text = _valid_cpp()
    assert 35_000 < len(text.encode("utf-8")) <= 40_960
    code = normalize(text, LanguageHint(language=Language.CPP))
    result = run_tier0(code)
    assert result.diagnostics == [], [d.message for d in result.diagnostics]
