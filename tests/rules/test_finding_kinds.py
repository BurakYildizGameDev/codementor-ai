"""Statik kural bulgularında tür ayrımı (Faz 52).

`issue` → Sorunlar/Sokratik soru; `suggestion` → Öneriler (sayılmayan, kaynak filtre
simgesiyle gizlenen) bölümünde gider (ADR-0022). Tür burada kural bazında değil,
kural içi koşula göre verilir: aynı kapsamdaki kaynak tahsisle eşleşen `delete` /
`close()` varsa bulgu öneridir; eşleşme yoksa hata kalır.
"""

from __future__ import annotations

import pytest

from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, FindingKind, Language, Severity
from codementor.models.request import LanguageHint
from codementor.rules import all_rules, run_rules

_UNREAL_CPP = """void Fill(TArray<int32>& Out, int32 Count) {
    for (int32 i = 0; i < Count; ++i) {
        Out.Add(i * 3);
    }
}
"""


def kinds(
    code: str, language: Language, engine: Engine = Engine.NONE
) -> dict[FindingKind, set[int]]:
    """Kod parçasındaki bulguların türü → satır kümesi (tüm kurallar çalışır)."""
    source = normalize(code, LanguageHint(language=language, engine=engine))
    result = run_rules(source, extract_facts(source))
    assert not result.warnings, result.warnings
    grouped: dict[FindingKind, set[int]] = {}
    for f in result.findings:
        grouped.setdefault(f.kind, set()).add(f.line_start)
        if f.kind == FindingKind.SUGGESTION:
            assert f.severity is Severity.LOW, f"öneri düşük önemde olmalı: {f}"
    return grouped


def test_cpp_matched_pair_in_one_scope_is_suggestion() -> None:
    """Aynı fonksiyonda new[]/delete[] eşleşiyorsa sahiplik iddialı ama RAII'siz: öneri."""
    found = kinds(
        "void handle(int n) {\n    int* data = new int[n];\n    delete[] data;\n}\n", Language.CPP
    )
    assert found == {FindingKind.SUGGESTION: {2, 3}}


def test_cpp_allocation_without_delete_is_issue() -> None:
    found = kinds("void leaky(int n) {\n    int* data = new int[n];\n}\n", Language.CPP)
    assert found == {FindingKind.ISSUE: {2}}


def test_cpp_ctor_delete_dtor_is_issue() -> None:
    """Yıkıcıdaki delete farklı kapsamdır: eşleşme yok, hata kalır (cpp-009 gibi)."""
    found = kinds(
        "class Buffer {\n"
        "public:\n"
        "    explicit Buffer(int n) : data_(new char[n]) {}\n"
        "    ~Buffer() { delete[] data_; }\n"
        "private:\n"
        "    char* data_;\n"
        "};\n",
        Language.CPP,
    )
    assert found == {FindingKind.ISSUE: {3, 4}}


def test_cpp_mismatched_new_delete_kinds_do_not_match() -> None:
    """`new[]` ile `delete` eşleşmez: her ikisi de hata kalır."""
    found = kinds(
        "void bad(int n) {\n    int* data = new int[n];\n    delete data;\n}\n", Language.CPP
    )
    assert found == {FindingKind.ISSUE: {2, 3}}


def test_python_open_with_close_in_same_scope_is_suggestion() -> None:
    found = kinds(
        'def save(path: str) -> None:\n    f = open(path, "w")\n    f.write("x")\n    f.close()\n',
        Language.PYTHON,
    )
    assert found == {FindingKind.SUGGESTION: {2}}


def test_python_open_without_close_is_issue() -> None:
    found = kinds(
        "def load(path: str) -> str:\n    f = open(path)\n    return f.read()\n", Language.PYTHON
    )
    assert found == {FindingKind.ISSUE: {2}}


def test_python_module_level_open_with_close_is_suggestion() -> None:
    """Modül düzeyi tek kapsamdır; `close()` oradaysa eşleşme var sayılır."""
    found = kinds('cfg = open("settings.json", encoding="utf-8")\ncfg.close()\n', Language.PYTHON)
    assert found == {FindingKind.SUGGESTION: {1}}


def test_ue_mem_001_is_always_suggestion() -> None:
    """UE-MEM-001 hataya yol açmaz, yalnız uyarı niteliğinde performans önerisidir."""
    found = kinds(_UNREAL_CPP, Language.CPP, Engine.UNREAL)
    assert found == {FindingKind.SUGGESTION: {3}}


@pytest.mark.parametrize("rule", all_rules(), ids=lambda r: r.id)
def test_rule_info_carries_default_kind(rule: type) -> None:
    """Katalog satırı türü kuralın varsayılan türünden gelir (Faz 52 `RuleInfo.kind`)."""
    info = rule.info()
    assert info.kind == rule.default_kind
