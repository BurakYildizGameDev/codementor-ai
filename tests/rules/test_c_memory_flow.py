"""C-MEM-001 sahiplik zinciri ve C-MEM-003 denetim akışı (iş 5 dilim 2, 5).

Fixture'lar tek halkalı ödünç aktarımını ve tipik denetim biçimlerini sabitler; buradakiler
onların ifade edemediği durumları: zincir derinliği, tur bütçesi, karşılıklı özyineleme ve
denetimin tahsise göre konumu (aynı dosyada korumalı/korumasız tahsisler).
"""

from __future__ import annotations

from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint
from codementor.rules import run_rules
from codementor.rules.c import _MAX_BORROW_ROUNDS


def lines(code: str, rule_id: str) -> list[int]:
    """C kodundaki `rule_id` bulgularının satırları (tüm kurallar çalışır)."""
    source = normalize(code, LanguageHint(language=Language.C, engine=Engine.NONE))
    result = run_rules(source, extract_facts(source))
    assert not result.warnings, result.warnings
    return [f.line_start for f in result.findings if f.rule_id == rule_id]


def _chain(links: int) -> str:
    """`f0` (tahsis eden) → `f1` → … → `f{links}` (yaprak okuyucu) zincirli dosya."""
    body = ["#include <stdlib.h>", ""]
    for i in range(1, links):
        body += [f"int f{i}(const int *v, int n) {{", f"    return f{i + 1}(v, n);", "}", ""]
    body += [
        f"int f{links}(const int *v, int n) {{",
        "    return v[0] + n;",
        "}",
        "",
        "int f0(int n) {",
        "    int *p = malloc(n * sizeof *p);",
        "    if (p == NULL) return 0;",
        "    p[0] = n;",
        "    return f1(p, n);",
        "}",
    ]
    return "\n".join(body) + "\n"


def _malloc_line(code: str) -> int:
    return next(i for i, row in enumerate(code.splitlines(), start=1) if "malloc(" in row)


def test_borrow_passes_through_one_link() -> None:
    """`f0` → `f1` (yaprak okuyucu): işaretçi hâlâ serbest bırakılmıyor."""
    code = _chain(1)
    assert lines(code, "C-MEM-001") == [_malloc_line(code)]


def test_borrow_passes_within_round_budget() -> None:
    """Tur bütçesine sığan zincir (6 halka) baştan sona çözülür."""
    code = _chain(6)
    assert lines(code, "C-MEM-001") == [_malloc_line(code)]


def test_chain_deeper_than_round_budget_is_conservative() -> None:
    """Bütçeden derin zincir kaçırılır (mimari §12: dosya başına sabit sayıda tur)."""
    code = _chain(_MAX_BORROW_ROUNDS + 4)
    assert lines(code, "C-MEM-001") == []


def test_mutual_recursion_terminates_and_is_conservative() -> None:
    """`a` ↔ `b` döngüsünde hangisinin sahiplendiği bilinmez: bulgu yok, süre sonsuz değil."""
    code = """#include <stdlib.h>

int a(const int *v, int n);
int b(const int *v, int n);

int a(const int *v, int n) {
    return n > 0 ? b(v, n - 1) : v[0];
}

int b(const int *v, int n) {
    return n > 0 ? a(v, n - 1) : v[0];
}

int f(int n) {
    int *p = malloc(n * sizeof *p);
    if (p == NULL) return 0;
    p[0] = n;
    return a(p, n);
}
"""
    assert lines(code, "C-MEM-001") == []


def test_guard_before_the_allocation_does_not_count() -> None:
    """`if (p == NULL) p = malloc(..);` denetimi tahsisten önce: kullanım yine korumasız."""
    code = """#include <stdlib.h>

void fill(int n) {
    int *p = NULL;
    if (p == NULL) p = malloc(n * sizeof *p);
    p[0] = n;
}
"""
    assert lines(code, "C-MEM-003") == [5]


def test_allocation_inside_the_condition_is_checked() -> None:
    """`if (!(p = malloc(..))) return;` denetimi tahsisle aynı deyimde: bulgu yok."""
    code = """#include <stdlib.h>

void fill(int n) {
    int *p;
    if (!(p = malloc(n * sizeof *p))) return;
    p[0] = n;
}
"""
    assert lines(code, "C-MEM-003") == []


def test_checked_and_unchecked_allocations_in_one_file() -> None:
    """Denetim tahsis başına değerlendirilir: yalnız kullanımdan sonra denetlenen bulgu olur."""
    code = """#include <stdlib.h>

int *late(int n) {
    int *p = malloc(n * sizeof *p);
    p[0] = n;
    if (p == NULL) return NULL;
    return p;
}

int *early(int n) {
    int *q = malloc(n * sizeof *q);
    if (q == NULL) return NULL;
    q[0] = n;
    return q;
}
"""
    assert lines(code, "C-MEM-003") == [4]


def test_guard_in_one_switch_case_does_not_cover_the_other_path() -> None:
    """Denetim tek dalda: `default` yolundan gelindiğinde işaretçi hâlâ denetlenmemiş."""
    code = """#include <stdlib.h>

int first(int mode, int n) {
    int *p = malloc(n * sizeof *p);
    switch (mode) {
        case 0:
            if (p == NULL) return -1;
            break;
        default:
            break;
    }
    return p[0];
}
"""
    assert lines(code, "C-MEM-003") == [4]


def test_use_only_in_a_condition_counts_as_use() -> None:
    """İlk kullanım koşulun içindeyse de denetimden önceki kullanımdır."""
    code = """#include <stdlib.h>

int any_positive(int n) {
    int *p = malloc(n * sizeof *p);
    if (p[0] > 0) return 1;
    return 0;
}
"""
    assert lines(code, "C-MEM-003") == [4]
