"""HTML-STD-003 ayrıntıları (Faz 20): açıklama türü, kapsam sınırı, RCDATA, `/>`."""

from __future__ import annotations

from codementor.models.enums import Language
from codementor.rules.html_balance import Imbalance, UnbalancedTag, imbalances
from tests.rules.engine_support import run_text


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


# ------------------------------------------------------------ Faz 56: kenar durumları


def test_unfinished_start_tag_at_eof_is_reported() -> None:
    assert set(imbalances("<main>\n<div class='a'")) == {
        Imbalance(1, "unclosed", "main"),
        Imbalance(2, "unfinished", "div"),
    }


def test_unfinished_tag_inside_script_is_text() -> None:
    """Script içeriğindeki `a<b` etiket değildir; yalnız kapanmamış script raporlanır."""
    assert imbalances("<script>\nif (a<b") == [Imbalance(1, "unclosed", "script")]


def test_implied_close_searches_below_inline_elements() -> None:
    """`<p><span>a<div>`: div açık `p`'yi span'in altından da kapatır; bulgu div satırında."""
    found = imbalances("<p><span>a\n<div>b</div>\n</span>\n</p>\n")
    assert found == [
        Imbalance(2, "implied", "div"),
        Imbalance(3, "stray", "span"),
        Imbalance(4, "stray", "p"),
    ]


def test_implied_close_stops_at_scope_element() -> None:
    """`button` gibi satır içi olmayan öğe aramayı durdurur (muhafazakâr)."""
    assert imbalances("<p><button>a<div>b</div></button></p>\n") == []


def test_li_closes_previous_item_through_div() -> None:
    assert imbalances("<ul>\n<li><div>a\n<li>b\n</ul>\n") == [Imbalance(3, "implied", "li")]


def test_table_closes_p_only_in_standards_mode() -> None:
    source = "<p>a\n<table><tr><td>x</td></tr></table>\n</p>\n"
    assert imbalances(source) == []  # DOCTYPE yok: quirks modunda table `p`'yi kapatmaz
    assert imbalances("<!DOCTYPE html>\n" + source) == [Imbalance(4, "stray", "p")]
    legacy = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n'
    assert imbalances(legacy + source) == []  # eski DOCTYPE: emin değiliz, kaçır


def test_same_line_mixed_kinds_reported_together() -> None:
    """Aynı satırdaki kapanmayan ve eşsiz etiket tek bulguda ikisini de anlatır."""
    findings = run_text("<main>\n<div><span>a</div></b>\n</main>\n", Language.HTML).findings
    (finding,) = [f for f in findings if f.rule_id == "HTML-STD-003"]
    assert finding.line_start == 2
    assert finding.description == UnbalancedTag.MIXED_DESCRIPTION


def test_implied_close_scan_is_linear() -> None:
    """Her `hr` aynı uzun satır içi zinciri yeniden taramamalı (mimari §12)."""
    import time

    source = "<p><button>" + "<b>" * 4000 + "<hr>" * 6000
    start = time.perf_counter()
    imbalances(source)
    assert time.perf_counter() - start < 1.0


def test_catalog_shows_scope_note_without_changing_question() -> None:
    """Kapsam/sınır notu yalnız katalogda; öğrenciye giden soru değişmez."""
    from codementor.rules.catalog import render_catalog

    catalog = render_catalog()
    assert f"*Kapsam ve sınırlar:* {UnbalancedTag.catalog_note}" in catalog
    assert UnbalancedTag.description.endswith("?")
    assert "Bilinen sınırlar" not in UnbalancedTag.description
    question = f"### HTML-STD-003 — Dengesiz etiket\n\n{UnbalancedTag.description}\n"
    assert question in catalog


def test_formatting_elements_are_not_passed() -> None:
    """Denetim Ö2: tarayıcı `b`/`em`/`a`'yı yeniden kurar; sonraki kapanış eşsiz değildir."""
    assert imbalances("<ul>\n<li><b>bold\n<li>also</b>\n</ul>\n") == []
    assert imbalances("<!DOCTYPE html>\n<p><em>Not:\n<p>devam</em>\n") == []
    # `a` biçimlendirme öğesi: arama durur, `p` açık kalır (main ile aynı, sessiz)
    assert imbalances("<!DOCTYPE html>\n<p><a href='#'>\n<div>card</div>\n</a></p>\n") == []


def test_implied_and_unfinished_use_own_questions() -> None:
    """Denetim Ö3 ve küçük bulgu: örtük kapanış tetikleyen satırda, yarım etiket `>` sorusuyla."""
    implied = run_text("<main>\n<p><span>a\n<div>b</div>\n</main>\n", Language.HTML).findings
    (finding,) = [f for f in implied if f.rule_id == "HTML-STD-003"]
    assert (finding.line_start, finding.description) == (3, UnbalancedTag.IMPLIED_DESCRIPTION)

    unfinished = run_text('<p>a</p>\n<img src="a.png"\n', Language.HTML).findings
    (finding,) = [f for f in unfinished if f.rule_id == "HTML-STD-003"]
    assert (finding.line_start, finding.description) == (2, UnbalancedTag.UNFINISHED_DESCRIPTION)
