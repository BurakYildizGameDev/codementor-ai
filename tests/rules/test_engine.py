"""Kural motoru: numaralama, tekilleştirme, yalıtım, kanıt, doğrusal süre."""

from __future__ import annotations

import time
from collections.abc import Iterator
from pathlib import Path

import pytest

from codementor.analysis.extractor import extract_facts
from codementor.analysis.parsers import parse
from codementor.ingest.normalize import normalize
from codementor.models.enums import AuditCategory, Engine, Language, Severity
from codementor.models.findings import Finding
from codementor.models.request import LanguageHint
from codementor.models.rules import RuleRunResult
from codementor.rules import run_rules
from codementor.rules.base import MAX_EVIDENCE, Rule, RuleContext
from codementor.rules.engine import RULE_FAILURE_WARNING, UNKNOWN_DISABLED_WARNING
from codementor.rules.registry import register_rule, unregister_rule

_LANG = {".c": Language.C, ".cpp": Language.CPP, ".h": Language.CPP, ".cs": Language.CSHARP}


def run_text(
    text: str, language: Language, engine: Engine = Engine.NONE, **kwargs: list[str]
) -> RuleRunResult:
    code = normalize(text, LanguageHint(language=language, engine=engine))
    return run_rules(code, extract_facts(code), **kwargs)


def run(path: Path, engine: Engine, **kwargs: list[str]) -> RuleRunResult:
    return run_text(path.read_text(encoding="utf-8"), _LANG[path.suffix], engine, **kwargs)


class _Probe(Rule):
    title = "t"
    description = "d"
    languages = frozenset({Language.C})
    category = AuditCategory.DESIGN
    default_severity = Severity.LOW


@pytest.fixture
def probes() -> Iterator[None]:
    @register_rule
    class Crash(_Probe):
        id = "TEST-CRASH-001"

        def check(self, ctx: RuleContext) -> list[Finding]:
            raise RuntimeError("bozuk kural")

    @register_rule
    class Twice(_Probe):
        id = "TEST-TWICE-001"

        def check(self, ctx: RuleContext) -> list[Finding]:
            return [self.finding(ctx, 3), self.finding(ctx, 3), self.finding(ctx, 1)]

    yield
    unregister_rule("TEST-CRASH-001")
    unregister_rule("TEST-TWICE-001")


C_TEXT = """#include <stdio.h>
int main(void) {
    char a[8];
    gets(a);
    return 0;
}
"""


@pytest.mark.usefixtures("probes")
def test_crashing_rule_isolated_with_warning() -> None:
    result = run_text(C_TEXT, Language.C, disabled=[])
    assert result.warnings == [RULE_FAILURE_WARNING.format("TEST-CRASH-001", "RuntimeError")]
    assert any(f.rule_id == "C-BUF-001" for f in result.findings)


@pytest.mark.usefixtures("probes")
def test_same_line_deduplicated() -> None:
    result = run_text(C_TEXT, Language.C, disabled=["TEST-CRASH-001"])
    twice = [f.line_start for f in result.findings if f.rule_id == "TEST-TWICE-001"]
    assert twice == [1, 3]


@pytest.mark.usefixtures("probes")
def test_finding_ids_sequential_sorted_by_line() -> None:
    result = run_text(C_TEXT, Language.C, disabled=["TEST-CRASH-001"])
    assert [f.id for f in result.findings] == [
        f"F-{i:03d}" for i in range(1, len(result.findings) + 1)
    ]
    assert [f.line_start for f in result.findings] == sorted(f.line_start for f in result.findings)
    gets = next(f for f in result.findings if f.rule_id == "C-BUF-001")
    assert gets.line_start == 4
    assert gets.evidence == "gets(a);"
    assert gets.source == "static"
    assert gets.line_end is None


def test_evidence_clipped() -> None:
    long_line = "    gets(a); /*" + "x" * 500 + "*/"
    text = C_TEXT.replace("    gets(a);", long_line)
    finding = next(f for f in run_text(text, Language.C).findings if f.rule_id == "C-BUF-001")
    assert len(finding.evidence) == MAX_EVIDENCE
    assert finding.evidence.endswith("…")


def test_line_text_out_of_range() -> None:
    code = normalize(C_TEXT, LanguageHint(language=Language.C))
    ctx = RuleContext(Language.C, Engine.NONE, code.lines, extract_facts(code), parse(code))
    assert ctx.line_text(0) == ""
    assert ctx.line_text(999) == ""


def test_unknown_disabled_rule_warns() -> None:
    result = run_text(C_TEXT, Language.C, disabled=["C-BUF-01", "C-BUF-001"])
    assert result.warnings == [UNKNOWN_DISABLED_WARNING.format("C-BUF-01")]
    assert not any(f.rule_id == "C-BUF-001" for f in result.findings)


def test_in_loop_uses_loop_bodies() -> None:
    text = (
        "public class P { public void F(int[] a) {\n"
        '  string s = "";\n'
        "  foreach (var x in a) { s += x; }\n"
        '  s += "son";\n'
        "} }\n"
    )
    found = [f.line_start for f in run_text(text, Language.CSHARP).findings]
    assert found == [3]


def test_no_rules_for_clean_code() -> None:
    text = "int add(int a, int b) { return a + b; }\n"
    assert run_text(text, Language.C) == RuleRunResult()


def _timed(text: str, language: Language, engine: Engine) -> float:
    start = time.perf_counter()
    run_text(text, language, engine)
    return time.perf_counter() - start


@pytest.mark.parametrize(
    ("text", "language", "engine"),
    [
        # 40 KB sınırına yakın: çok sayıda malloc + çağrı zinciri (C-MEM-001 ağaç gezintisi)
        (
            "#include <stdlib.h>\nvoid f(void) {\n"
            + "    char *p = malloc(1); g(p); char *q = calloc(1, 1); q[0] = 1;\n" * 560
            + "}\n",
            Language.C,
            Engine.NONE,
        ),
        # Unity: çok sayıda abonelik ve Update içinde tahsis
        (
            "using System; using UnityEngine;\npublic class P : MonoBehaviour {\n"
            "public event Action E;\nvoid H() {}\nvoid OnEnable() {\n"
            + "E += H; E += H; E += H; E += H; E += H; E += H;\n" * 330
            + "}\nvoid OnDisable() {\n"
            + "E -= H; E -= H; E -= H; E -= H; E -= H; E -= H;\n" * 250
            + "}\n}\n",
            Language.CSHARP,
            Engine.UNITY,
        ),
        # Denetim Y1: iç içe çağrı ve iç içe atama (eski C-MEM-001'de 106 s / 30 s)
        (
            "#include <stdlib.h>\nvoid f(void){ char *p = malloc(1);\n"
            + "g(" * 9000
            + "p"
            + ")" * 9000
            + ";\n}\n",
            Language.C,
            Engine.NONE,
        ),
        (
            "#include <stdlib.h>\nstruct S { int *a; };\n"
            "void f(struct S *s){ int *p = malloc(1);\n" + "s->a = " * 4500 + "p;\n}\n",
            Language.C,
            Engine.NONE,
        ),
        # Denetim O1: uzun üye erişim zinciri (Camera.main araması)
        (
            "using UnityEngine;\npublic class P : MonoBehaviour {\n"
            "void Update(){ var x = a" + ".b" * 19000 + "; }\n}\n",
            Language.CSHARP,
            Engine.UNITY,
        ),
        # İç içe `-=` zinciri ve döngüde uzun `+` zinciri (UNITY-EVT-001, CS-ALLOC-001)
        (
            "using System; using UnityEngine;\npublic class P : MonoBehaviour {\n"
            "public event Action E;\nvoid H() {}\nvoid OnEnable() { E += H; }\n"
            "void OnDisable() {\n" + "E -= " * 3000 + "H;\n}\n"
            'void Update() { string s = ""; for (;;) { s = s' + ' + "a"' * 3000 + "; } }\n}\n",
            Language.CSHARP,
            Engine.UNITY,
        ),
        # Faz 17: iç içe realloc/NULL denetimi (C-MEM-002/003) ve koşulda strlen (C-PERF-001)
        (
            "#include <stdlib.h>\n#include <string.h>\nvoid f(char *s){ char *p = malloc(1);\n"
            + "p = realloc(" * 1500
            + "p"
            + ", 1)" * 1500
            + ";\n"
            + "while ("
            + "(" * 2000
            + "strlen(s)"
            + ")" * 2000
            + ") { p[0] = 0; }\n"
            + "if ("
            + "!(" * 1500
            + "p"
            + ")" * 1500
            + ") {}\n}\n",
            Language.C,
            Engine.NONE,
        ),
        # Uzun shared_ptr zinciri ve geri dönen kenar (CPP-SP-001 Tarjan, özyinelemesiz)
        (
            "#include <memory>\n"
            + "".join(
                f"struct N{i}{{std::shared_ptr<N{i + 1}> n;}};" + "\n" * (i % 2) for i in range(900)
            )
            + "struct N900 { std::shared_ptr<N0> back; };\n",
            Language.CPP,
            Engine.NONE,
        ),
        # Çok sayıda scanf/fflush satırı (C-IO-001, C-UB-001)
        (
            "#include <stdio.h>\nint main(void){ int n;\n"
            + 'scanf("%d", &n); fflush(stdin); scanf("%d", &n); fflush(stdin);\n' * 560
            + "return 0; }\n",
            Language.C,
            Engine.NONE,
        ),
        # Update'te çok sayıda tag karşılaştırması ve LINQ (UNITY-PERF-002, CS-ALLOC-002)
        (
            "using System.Linq; using System.Collections.Generic; using UnityEngine;\n"
            "public class P : MonoBehaviour { public List<int> xs; void Update() {\n"
            + 'if (tag == "a" || xs.Distinct().Any()) {} if (tag != "b") {}\n' * 500
            + "} }\n",
            Language.CSHARP,
            Engine.UNITY,
        ),
        # İç içe sayılı döngüler ve Add (UE-MEM-001 en dıştaki döngüden tek geçiş)
        (
            "void AA::F(int32 N) { TArray<int32> Out;\n"
            + "for (int32 i = 0; i < N; ++i) {" * 1000
            + "\nOut.Add(1);\n"
            + "}" * 1000
            + "\n}\n",
            Language.CPP,
            Engine.UNREAL,
        ),
        # Faz 17 denetimi K1: sola iç içe atama zinciri (C-MEM-003 `_key`, 29.8 s idi)
        (
            "void f(int*a){malloc(1);\n" + "(" * 9900 + "a" + "=0)" * 9900 + ";}\n",
            Language.C,
            Engine.NONE,
        ),
        # K1: sola iç içe realloc ataması (C-MEM-002/003)
        (
            "#include <stdlib.h>\nvoid f(int*x){\n"
            + "(" * 2300
            + "x"
            + " = realloc(x,1))" * 2300
            + ";}\n",
            Language.C,
            Engine.NONE,
        ),
        # K2: döngü koşulunda iç içe GNU deyim ifadesi (C-PERF-001, 14.9 s idi)
        (
            "void f(char*s){strlen(s);" + "while(({" * 3700 + "0;" + "}))" * 3700 + ";}\n",
            Language.C,
            Engine.NONE,
        ),
        # K3: iç içe yerel struct metotları (UE-MEM-001, 8.8 s idi)
        (
            "TArray<int> X;\n" + "struct A{void g(){X.Add(1);" * 1200 + "}};" * 1200 + "\n",
            Language.CPP,
            Engine.UNREAL,
        ),
        # K4: iç içe yerel Update fonksiyonları (UNITY-PERF-002, 5.1 s idi)
        (
            "using UnityEngine;\nclass P:MonoBehaviour{void Update(){"
            + "void Update(){" * 2500
            + "}" * 2500
            + "}}\n",
            Language.CSHARP,
            Engine.UNITY,
        ),
        # K5: iç içe metotlarda değerle parametre (CPP-PERF-001, 3.2 s idi)
        (
            "using namespace std;\n" + "struct A{void g(string s){" * 1300 + "}};" * 1300 + "\n",
            Language.CPP,
            Engine.NONE,
        ),
    ],
    ids=[
        "c-malloc",
        "unity-events",
        "c-nested-call",
        "c-nested-assign",
        "cs-member-chain",
        "cs-nested-chains",
        "c-nested-realloc",
        "cpp-shared-chain",
        "c-scanf-lines",
        "unity-tag-linq",
        "ue-nested-loops",
        "c-left-nested-assign",
        "c-left-nested-realloc",
        "c-nested-statement-expr",
        "ue-nested-local-structs",
        "unity-nested-update",
        "cpp-nested-by-value",
    ],
)
def test_linear_time_large_input(text: str, language: Language, engine: Engine) -> None:
    assert len(text.encode()) <= 40960
    assert _timed(text, language, engine) < 2.0


def test_linq_in_update_reported_once() -> None:
    """Faz 17: Unity Update'teki LINQ yalnızca CS-ALLOC-002 ile raporlanır (UNITY-GC-001 değil)."""
    code = (
        "using System.Collections.Generic; using System.Linq; using UnityEngine;\n"
        "public class P : MonoBehaviour {\n"
        "    public List<string> names;\n"
        "    void Update() { int n = names.Distinct().Count(); }\n"
        "}\n"
    )
    findings = run_text(code, Language.CSHARP, Engine.UNITY).findings
    assert [(f.rule_id, f.line_start) for f in findings] == [("CS-ALLOC-002", 4)]
