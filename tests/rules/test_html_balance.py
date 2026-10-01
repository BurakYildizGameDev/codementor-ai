"""HTML-STD-003 ayrıntıları (Faz 20): açıklama türü, kapsam sınırı, RCDATA, `/>`."""

from __future__ import annotations

from codementor.models.enums import Language
from codementor.rules.html_balance import Imbalance, UnbalancedTag, imbalances
from tests.rules.test_engine import run_text


def test_stray_end_tag_uses_its_own_question() -> None:
    findings = run_text("<p>a</p>\n</div>\n", Language.HTML).findings
    (finding,) = [f for f in findings if f.rule_id == "HTML-STD-003"]
    assert finding.line_start == 2
    assert finding.description == UnbalancedTag.STRAY_DESCRIPTION


def test_unclosed_element_uses_default_question() -> None:
    findings = run_text("<main>\n<div>\n</main>\n", Language.HTML).findings
    (finding,) = [f for f in findings if f.rule_id == "HTML-STD-003"]
    assert finding.line_start == 2
    assert finding.description == UnbalancedTag.description


def test_end_tag_outside_cell_scope_is_stray_only() -> None:
    """Denetim O1: hücre sınırı dışındaki öğenin kapanışı yalnız eşsiz sayılır; yığın bozulmaz."""
    source = "<div>\n<table>\n<tr><td>a</div></td></tr>\n</table>\n</div>\n"
    assert imbalances(source) == [Imbalance(3, "stray", "div")]


def test_table_end_closes_open_cells() -> None:
    assert imbalances("<table><tr><td>a</table>\n") == []


def test_rcdata_content_is_text() -> None:
    """Denetim O2: Python yama sürümünden bağımsız olarak title/textarea içeriği metindir."""
    assert imbalances("<title>a </div> b</title>\n<textarea><span></textarea>\n") == []


def test_self_closing_syntax_ignored_only_for_void_and_foreign() -> None:
    assert imbalances("<br/><img src=a/><svg><path d='M0'/></svg>\n") == []
    assert imbalances("<main>\n<span/>\n</main>\n") == [Imbalance(2, "unclosed", "span")]


def test_hr_closes_paragraph() -> None:
    """Denetim D1: `hr` boş öğe olsa da açık `p`'yi kapatır; sonraki `</p>` eşsizdir."""
    assert imbalances("<p>a\n<hr>\n</p>\n") == [Imbalance(3, "stray", "p")]
