"""HTML etiket dengesi (Faz 20): kapanmayan, eşi olmayan ve iç içe karışan etiketler.

tree-sitter-html dengesiz etiketlerde tutarsızdır (tam belgede eşi olmayan `</div>` hata
değil, `<div><span>x</div>` hiç işaretlenmez); bu yüzden kural ağaç yerine stdlib
`html.parser` ile kendi açık etiket yığınını tutar. Tarayıcılar hoşgörülü olduğundan bu bir
sözdizimi hatası değil, bulgu olarak raporlanır (ADR-0015 notu). HTML5'in tam ağaç kurma
algoritması değil, sade bir örtük kapanış tablosu kullanılır: emin olunmayan durumda kaçırma.

Faz 56 kapsamı: dosya sonunda bitmemiş açılış (`<div`); örtük kapanışta açık `p`/`li` öğesi
yığının tepesinde değilse yalnız satır içi öğelerin altında aranır (`<p><span>a<div>`);
DOCTYPE'sız (quirks) belgede `table` açık `p`'yi kapatmaz. Bilinen sınırlar: biçimlendirme
öğelerinin yeniden kurulması (adoption agency), `form`/`button` kapsam ayrıntıları, tabloya
yanlış konan içeriğin dışarı taşınması (foster parenting) ve eski DOCTYPE'ların modu
modellenmez; bu durumlarda kural sessiz kalır.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Literal

from codementor.models.enums import AuditCategory, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

VOID = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)
# Kapanışı yazılmayabilen öğeler: açık kalmaları ya da örtük kapanmaları bulgu değildir
OPTIONAL_END = frozenset(
    {
        "p",
        "li",
        "dt",
        "dd",
        "tr",
        "td",
        "th",
        "thead",
        "tbody",
        "tfoot",
        "option",
        "optgroup",
        "colgroup",
        "caption",
        "rb",
        "rt",
        "rp",
        "html",
        "head",
        "body",
    }
)
# Eşi olmayan kapanışı raporlanmayan belge iskeleti (örtük açılıp kapanırlar)
_SKELETON = frozenset({"html", "head", "body"})
_CLOSES_P = frozenset(
    {
        "address",
        "article",
        "aside",
        "blockquote",
        "details",
        "div",
        "dl",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hgroup",
        "hr",
        "main",
        "menu",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "ul",
    }
)
# Örtük kapanışın aşağı inerek arayabildiği satır içi öğeler (HTML5 "special" değiller)
_PHRASING = frozenset(
    {
        "a",
        "abbr",
        "b",
        "bdi",
        "bdo",
        "big",
        "cite",
        "code",
        "data",
        "dfn",
        "em",
        "font",
        "i",
        "kbd",
        "label",
        "mark",
        "nobr",
        "q",
        "s",
        "samp",
        "small",
        "span",
        "strike",
        "strong",
        "sub",
        "sup",
        "time",
        "tt",
        "u",
        "var",
    }
)
# `li`/`dt`/`dd` önceki öğeyi `address`, `div`, `p` altından da kapatır (list item kapsamı)
_LIST_PASSABLE = _PHRASING | {"address", "div", "p"}
_SCAN_LIMIT = 64  # örtük kapanış aramasının derinliği: kötü niyetli girdide doğrusal kalır
_UNFINISHED_TAG = re.compile(r"<([a-zA-Z][^\s/>]*)")
_TABLE_SECTIONS = frozenset({"thead", "tbody", "tfoot", "tr", "td", "th"})
# açılan etiket → yığının tepesinde bulununca örtük kapattığı öğeler
_IMPLICIT: dict[str, frozenset[str]] = {
    **dict.fromkeys(_CLOSES_P, frozenset({"p"})),
    "li": frozenset({"li"}),
    "dt": frozenset({"dt", "dd"}),
    "dd": frozenset({"dt", "dd"}),
    "tr": frozenset({"tr", "td", "th"}),
    "td": frozenset({"td", "th"}),
    "th": frozenset({"td", "th"}),
    "thead": _TABLE_SECTIONS,
    "tbody": _TABLE_SECTIONS,
    "tfoot": _TABLE_SECTIONS,
    "option": frozenset({"option"}),
    "optgroup": frozenset({"option", "optgroup"}),
    "body": frozenset({"head"}),
}
# açılan etiket → örtük kapanışın aşağı inerken atlayabildiği öğeler (yoksa yalnız tepe)
_PASSABLE: dict[str, frozenset[str]] = {
    **dict.fromkeys(_CLOSES_P, _PHRASING),
    **dict.fromkeys(("li", "dt", "dd"), _LIST_PASSABLE),
}


# Kapsam sınırları: tarayıcı, sınırın dışında açılmış bir öğenin kapanışını yok sayar
# (`<div><table><tr><td></div>` → `</div>` eşsiz; tablo ve div bozulmaz)
_HARD_BOUNDS = frozenset({"table", "template", "object", "marquee", "applet"})
_CELL_BOUNDS = frozenset({"td", "th", "caption"})
_TABLE_TAGS = frozenset(
    {"table", "thead", "tbody", "tfoot", "tr", "td", "th", "caption", "colgroup"}
)
# İçeriği metin olan öğeler; HTMLParser'ın bu listesi Python yama sürümüne göre değiştiği için
# kural kendisi ayarlar (`<title>a </div></title>` her sürümde etiket sayılmaz)
_RAW_TEXT = frozenset({"title", "textarea", "xmp", "iframe", "noembed", "noframes"})
_FOREIGN = ("svg", "math")  # içlerinde `<x/>` gerçekten kendini kapatır


@dataclass(frozen=True)
class Imbalance:
    line: int
    kind: Literal["unclosed", "stray"]
    tag: str


class _Balance(HTMLParser):
    """Açık etiket yığını. Ad → yığın konumları ve sınır konumları ayrıca tutulur; böylece
    üyelik ve kapsam denetimi O(1), yığından çıkarma amorti doğrusal (mimari §12)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.positions: dict[str, list[int]] = defaultdict(list)
        self.hard_bounds: list[int] = []
        self.cell_bounds: list[int] = []
        self.found: list[Imbalance] = []
        self.standards = False  # `<!DOCTYPE html>` görüldü mü (yoksa quirks modu)

    def _push(self, tag: str) -> None:
        index = len(self.stack)
        self.stack.append((tag, self.getpos()[0]))
        self.positions[tag].append(index)
        if tag in _HARD_BOUNDS:
            self.hard_bounds.append(index)
        if tag in _HARD_BOUNDS or tag in _CELL_BOUNDS:
            self.cell_bounds.append(index)

    def _pop(self) -> tuple[str, int]:
        tag, line = self.stack.pop()
        self.positions[tag].pop()
        index = len(self.stack)
        if self.hard_bounds and self.hard_bounds[-1] == index:
            self.hard_bounds.pop()
        if self.cell_bounds and self.cell_bounds[-1] == index:
            self.cell_bounds.pop()
        return tag, line

    def handle_decl(self, decl: str) -> None:
        # Yalnız modern `<!DOCTYPE html>` standart moddur; eski DOCTYPE'larda emin değiliz
        words = decl.lower().split()
        self.standards = words[:2] == ["doctype", "html"] and "public" not in words

    def _close_implied(self, tag: str) -> None:
        """`tag` açılırken örtük kapanan öğeleri çıkarır; aradaki satır içi öğeler kapanmamıştır."""
        closes = _IMPLICIT.get(tag)  # boş `hr` de açık `p`'yi kapatır
        if not closes or (tag == "table" and not self.standards):
            return  # quirks modunda `table` açık `p`'yi kapatmaz
        passable = _PASSABLE.get(tag, frozenset())
        target = -1
        floor = max(len(self.stack) - _SCAN_LIMIT, 0)
        for index in range(len(self.stack) - 1, floor - 1, -1):
            name = self.stack[index][0]
            if name in closes:
                target = index
            elif name not in passable:
                break
        while target >= 0 and len(self.stack) > target:
            name, line = self._pop()
            if name not in closes and name not in OPTIONAL_END:
                self.found.append(Imbalance(line, "unclosed", name))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._close_implied(tag)
        if tag in VOID:
            return
        self._push(tag)
        if tag in _RAW_TEXT:
            self.set_cdata_mode(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # `<br/>` ve SVG/MathML `<path/>` kendini kapatır; HTML'de `<div/>`, `<script/>` ise
        # açık kalır (tarayıcı `/`'ı yok sayar; JSX alışkanlığı)
        if tag in VOID or any(self.positions[f] for f in _FOREIGN):
            return
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID:
            return
        opened = self.positions[tag]
        bounds = self.hard_bounds if tag in _TABLE_TAGS else self.cell_bounds
        if not opened or (bounds and bounds[-1] > opened[-1]):
            if tag not in _SKELETON:
                self.found.append(Imbalance(self.getpos()[0], "stray", tag))
            return
        while self.stack:
            name, line = self._pop()
            if name == tag:
                return
            if name not in OPTIONAL_END:
                self.found.append(Imbalance(line, "unclosed", name))

    def finish(self) -> list[Imbalance]:
        # `feed` bitmemiş açılışı (`<div class="a`) tamponda bırakır; `close` onu metin sayar
        unfinished = None if self.cdata_elem else _UNFINISHED_TAG.match(self.rawdata)
        if unfinished:
            self.found.append(Imbalance(self.getpos()[0], "unclosed", unfinished[1].lower()))
        self.close()
        self.found += [
            Imbalance(line, "unclosed", name)
            for name, line in self.stack
            if name not in OPTIONAL_END
        ]
        return self.found


def imbalances(source: str) -> list[Imbalance]:
    """Kaynaktaki dengesiz etiketler (satır sırası önemsiz)."""
    parser = _Balance()
    parser.feed(source)
    return parser.finish()


@register_rule
class UnbalancedTag(Rule):
    """HTML-STD-003: kapanmayan, eşi olmayan ya da iç içe karışan etiket."""

    id = "HTML-STD-003"
    title = "Dengesiz etiket"
    description = (
        "Bu etiket nerede kapanıyor? Kapanışı tarayıcı kendisi tahmin ederse sayfanın yapısı "
        "senin düşündüğünle aynı kalır mı?"
    )
    STRAY_DESCRIPTION = (
        "Bu kapanış etiketinin açılışı nerede? Tarayıcı eşi olmayan bir kapanışla "
        "karşılaşınca ne yapıyor olabilir?"
    )
    MIXED_DESCRIPTION = (
        "Bu satırda hem kapanmadan kalan hem de açılışı olmayan bir etiket var. Hangi kapanış "
        "hangi açılışa ait; tarayıcı bu satırı senin yazdığın gibi mi okuyor?"
    )
    catalog_note = (
        "Kapanmayan öğe, eşi olmayan kapanış, iç içe karışan etiketler ve dosya sonunda "
        "bitmemiş açılış (`<div`). İsteğe bağlı kapanışlar (`p`, `li`, tablo bölümleri…), "
        "örtük kapanış (`<p>` blok öğeyle, satır içi öğelerin altından da), tablo hücresi "
        "kapsamı ve DOCTYPE'sız (quirks) belgede `table`'ın `p`'yi kapatmaması dikkate alınır. "
        "Aynı satırdaki farklı türde ihlaller tek bulguda birlikte anlatılır. Bilinen sınırlar: "
        "HTML5 ağaç kurma algoritmasının tamamı değil; biçimlendirme öğelerinin yeniden "
        "kurulması, tabloya yanlış konan içeriğin dışarı taşınması ve eski DOCTYPE'ların modu "
        "modellenmez — emin olunmayan durumda kural sessiz kalır."
    )
    languages = frozenset({Language.HTML})
    category = AuditCategory.DESIGN
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        # Motor satır başına kural başına tek bulgu tutar (Faz 56): türler satırda birleşir
        kinds: dict[int, set[str]] = defaultdict(set)
        for item in imbalances(ctx.parsed.text):
            kinds[item.line].add(item.kind)
        return [
            self.finding(ctx, line, description=self._description(kinds[line]))
            for line in sorted(kinds)
        ]

    def _description(self, kinds: set[str]) -> str | None:
        if len(kinds) > 1:
            return self.MIXED_DESCRIPTION
        return self.STRAY_DESCRIPTION if kinds == {"stray"} else None
