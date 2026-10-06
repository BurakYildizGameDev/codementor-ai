"""Tier 0 en kötü durum ayrıştırma süresi gerileme testleri (Faz 55, ADR-0024).

Ölçülen sınırlı girdiler `run_tier0` için < 1,5 s eşikle sabitlenir. C# gramerinin
`a<`×20000 girdisinde süreç içinde ~10-12 s ve ~4,2 GB sürdüğü (parse'ın kendisi) ADR-0024'te
kabul edilmişti; Faz 59'dan beri `validation.tier0_isolation` açıkken alt süreçte süre ve
bellek sınırıyla durdurulur (ADR-0025) ve bu dosyada o yolla sabitlenir.
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


def test_csharp_bomb_bounded_with_isolation() -> None:
    """ADR-0025: süreç içinde ~10 s / ~4 GB olan C# `a<` girdisi yalıtımla hızla durur."""
    from codementor.config import ValidationSettings
    from codementor.validation.tier0_isolation import check_syntax

    code = normalize("a<" * 20000, LanguageHint(language=Language.CSHARP))
    settings = ValidationSettings(tier0_isolation=True, tier0_timeout_s=2)
    start = time.perf_counter()
    result = check_syntax(code, settings)
    assert time.perf_counter() - start < _deadline(6.0)
    assert result.has_errors  # erken çıkış: boru hattı bu girdiyi bir daha ayrıştırmaz
