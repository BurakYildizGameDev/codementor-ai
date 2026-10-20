"""Kural motoru: numaralama, tekilleştirme, yalıtım, kanıt, doğrusal süre.

Bölüm 2/2.
"""

from __future__ import annotations

import pytest

from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language, Severity
from codementor.models.request import LanguageHint
from codementor.rules import run_rules
from tests.rules.engine_support import (
    FLOOD_TEXT,
    _timed,
    run_text,
)


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
        # Faz 20: HTML-STD-003 — kapanmayan iç içe div'ler, eşsiz kapanışlar, karışık satır içi
        ("<!DOCTYPE html>\n<body>\n" + "<div>" * 3000 + "\n</body>\n", Language.HTML, Engine.NONE),
        (
            "<!DOCTYPE html>\n<body>\n" + "</span>" * 4500 + "\n</body>\n",
            Language.HTML,
            Engine.NONE,
        ),
        (
            "<!DOCTYPE html>\n<body>\n" + "<b><i>x</b></i>\n" * 500 + "</body>\n",
            Language.HTML,
            Engine.NONE,
        ),
        # Derin açık yığın + her kapanışta eşsiz arama (konum listesiyle O(1) olmalı)
        (
            "<!DOCTYPE html>\n<body>\n" + "<section>" * 2000 + "</em>" * 2500 + "\n",
            Language.HTML,
            Engine.NONE,
        ),
        # Denetim: tablo hücresi sınırları ve sınır dışı kapanışlar (kapsam denetimi O(1))
        (
            "<!DOCTYPE html>\n<body>\n<div>" + "<table><tr><td></div>" * 1200 + "\n",
            Language.HTML,
            Engine.NONE,
        ),
        # HTMLParser'ın kendi zayıf noktaları: bitmemiş yorum, `<!` ve `</` tekrarı
        ("<!DOCTYPE html>\n<body>\n<!--" + "a" * 39000 + "\n", Language.HTML, Engine.NONE),
        (
            "<!DOCTYPE html>\n<body>\n" + "<!" * 9000 + "</" * 9000 + "\n",
            Language.HTML,
            Engine.NONE,
        ),
        # Faz 57: C-MEM-003 akış sırası — her tahsis önceki tüm denetimleri taramamalı (5.2 s idi)
        (
            "#include <stdlib.h>\nvoid f(void){int *p=0;\n"
            + "if(!p)return;" * 1100
            + "p=malloc(1);*p=1;" * 1300
            + "}\n",
            Language.C,
            Engine.NONE,
        ),
        (
            "#include <stdlib.h>\nvoid f(void){int *p=0;\n"
            + "p=malloc(1);" * 1600
            + "*p=1;" * 2000
            + "}\n",
            Language.C,
            Engine.NONE,
        ),
        # Faz 57 denetimi K1: `.parent` tırmanışı derin ağaçta karesel (32 KB'ta 56 s idi)
        (
            "#include <stdlib.h>\nvoid f(void){int *p=0;\nif("
            + "!p&&" * 8000
            + "1);p=malloc(1);*p=1;}\n",
            Language.C,
            Engine.NONE,
        ),
        (
            "#include <stdlib.h>\nvoid f(void){int *p=0;\nwhile("
            + "!p&&" * 4500
            + "1){p=malloc(1);}*p=1;}\n",
            Language.C,
            Engine.NONE,
        ),
        (
            "#include <stdlib.h>\nvoid f(void){int *p=0;\n"
            + "if(1){" * 2000
            + "p=malloc(1);"
            + "if(!p);" * 3000
            + "}" * 2000
            + "*p=1;}\n",
            Language.C,
            Engine.NONE,
        ),
        # Faz H: yeni kurallar (CSS-ACC-001, CSS-LAYOUT-001/002, CPP-PERF-002..004, C-BUF-002)
        (("a:focus{outline:none;}" * 3 + "\n") * 600, Language.CSS, Engine.NONE),
        ((".k{height:200px;}" * 4 + "\n") * 580, Language.CSS, Engine.NONE),
        (
            (".c{position:absolute;left:50%;margin-left:-100px;}" * 2 + "\n") * 400,
            Language.CSS,
            Engine.NONE,
        ),
        (
            "#include <string>\nvoid f(int n){std::string s;\nfor(int i=0;i<n;++i){s = s"
            + ' + "x"' * 5000
            + ";}}\n",
            Language.CPP,
            Engine.NONE,
        ),
        (
            "#include <iostream>\nvoid f(int n){for(int i=0;i<n;++i){\n"
            + ("std::cout << i << std::endl;" * 4 + "\n") * 356
            + "}}\n",
            Language.CPP,
            Engine.NONE,
        ),
        (
            "#include <vector>\nvoid f(int n){std::vector<int> v;\n"
            + ("for(int i=0;i<n;++i){v.push_back(i);}" * 4 + "\n") * 270
            + "}\n",
            Language.CPP,
            Engine.NONE,
        ),
        (
            "#include <stdio.h>\nvoid f(void){char b[8];\n"
            + ('scanf("%s", b);' * 5 + "\n") * 520
            + "}\n",
            Language.C,
            Engine.NONE,
        ),
        # Faz H2: CPP-OWN-001 erken çıkış taraması (tek kapsamda çok sayıda new/delete/return)
        (
            "int f(int x){\n"
            + ("int* p = new int(x); if (x > 0) { return 0; } delete p;" * 4 + "\n") * 165
            + "return 1;}\n",
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
        "html-unclosed-divs",
        "html-stray-ends",
        "html-misnested-lines",
        "html-deep-stack-strays",
        "html-cell-bounds",
        "html-unterminated-comment",
        "html-bang-and-slash",
        "c-checks-then-allocs",
        "c-allocs-then-uses",
        "c-deep-and-chain",
        "c-loop-condition-chain",
        "c-deep-blocks-many-checks",
        # Faz H: yeni kurallar (CSS-ACC-001, CSS-LAYOUT-001/002, CPP-PERF-002..004, C-BUF-002)
        "css-focus-outline",
        "css-fixed-height",
        "css-margin-center",
        "cpp-string-copy-chain",
        "cpp-endl-in-loop",
        "cpp-push-back-no-reserve",
        "c-scanf-string",
        # Faz H2
        "cpp-new-delete-early-return",
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


@pytest.mark.usefixtures("flood")
def test_findings_capped_keeping_most_severe() -> None:
    result = run_rules(
        normalize(FLOOD_TEXT, LanguageHint(language=Language.C, engine=Engine.NONE)),
        extract_facts(normalize(FLOOD_TEXT, LanguageHint(language=Language.C))),
        disabled=[],
        max_findings=5,
    )
    assert len(result.findings) == 5
    assert any(f.line_start == 3 and f.severity is Severity.HIGH for f in result.findings)
    assert [f.id for f in result.findings] == [f"F-{i:03d}" for i in range(1, 6)]
    assert [f.line_start for f in result.findings] == sorted(f.line_start for f in result.findings)
    assert any("40" in w and "5" in w for w in result.warnings)


@pytest.mark.usefixtures("flood")
def test_under_cap_untouched() -> None:
    result = run_text(FLOOD_TEXT, Language.C, disabled=[])
    assert len([f for f in result.findings if f.rule_id == "TEST-FLOOD-001"]) == 40
    assert not any("gösteriliyor" in w for w in result.warnings)


def test_cap_default_from_settings() -> None:
    from codementor.config import RulesSettings

    assert RulesSettings().max_findings == 50
    with pytest.raises(ValueError, match="greater than or equal"):
        RulesSettings(max_findings=0)
