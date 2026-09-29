"""Statik karmaşıklık ipucu (mimari §5.3.2).

Yalnızca olgulardan (`CodeFacts`) hesaplanır; basit ve açıklanabilir kalması amaçtır:

1. Her döngü için iç içe yol boyunca sınıflar çarpılır: `LINEAR` → n, `LOG` → log n,
   `CONSTANT` → 1, `UNKNOWN` → n (varsayım; güven düşer).
2. Döngü içindeki bilinen çağrı maliyeti (`data/call_costs.yaml`) yol çarpanına eklenir;
   döngü dışındaki bilinen çağrı kendi maliyetiyle katkı verir.
3. Aynı dosyadaki bir fonksiyon çağrılıyorsa onun ipucu çarpan olur (tek dosya, döngüsel
   çağrılar kesilir; güven en fazla `medium`).
4. Özyineleme: dallanma > 1 ve yarılama yok → `2^n` + üstel şüphe; yarılamalı dallanma →
   böl-yönet (`max(n, iş · log n)`); tek dal → `iş · log n` ya da `iş · n`. Güven `low`.
5. Fonksiyon ipucu terimlerin baskınıdır; dosya ipucu en pahalı fonksiyondur.

Güven: baskın terimde varsayım (`UNKNOWN`), dış döngüde sıfırlanmayan iç sayaç
(two-pointer/amortize şüphesi) veya özyineleme → `low`; amortize maliyet, `while` ile
bulunan `LOG` veya başka fonksiyonun ipucu → `medium`; aksi halde `high`.
Çıktı gerçek değil **ipucudur**; K5'te LLM ile uzlaştırılır, dayatılmaz.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from codementor.analysis._callgraph import strongly_connected
from codementor.analysis._symbols import simple_name
from codementor.models.bigo import BigO, BigOError, parse_bigo, parse_cost
from codementor.models.enums import LoopBound
from codementor.models.facts import CallFact, CodeFacts, ComplexityHint, LoopFact

Confidence = Literal["low", "medium", "high"]

FILE_SCOPE = "<dosya>"
MAX_BASIS = 8
_FACTOR = {
    LoopBound.LINEAR: "n",
    LoopBound.LOG: "log n",
    LoopBound.CONSTANT: "1",
    LoopBound.UNKNOWN: "n",
}
_LOW_FLAGS = frozenset({"unknown", "outer_counter", "callee_low", "recursion", "overflow"})
_MEDIUM_FLAGS = frozenset({"amortized", "callee_medium", "while_log"})
_RANK: dict[Confidence, int] = {"low": 0, "medium": 1, "high": 2}


@dataclass
class _Term:
    value: BigO
    basis: str
    flags: set[str] = field(default_factory=set)
    notes: list[str] = field(default_factory=list)


def _product(*factors: str) -> tuple[BigO, bool]:
    """Çarpım (ikişer katlanır). Üs sınırı aşılırsa (kırpılmış değer, True).

    Sonuç kanonik biçimi yeniden ayrıştırılarak doğrulanır: `n^60 * n^60` tek tek geçerli
    olsa da çarpım üs sınırını aşar.
    """
    acc = parse_bigo("1")
    for factor in factors:
        try:
            product = parse_bigo(f"({acc.canonical})*({factor})")
            acc = parse_bigo(product.canonical)
        except BigOError:
            return acc, True
    return acc, False


def _dominant(values: list[BigO]) -> BigO:
    """Toplamın baskın terimi (ikişer katlanır)."""
    acc = parse_bigo("1")
    for value in values:
        acc = parse_bigo(f"({acc.canonical}) + ({value.canonical})")
    return acc


_OVERFLOW_NOTE = "iç içe derinlik Big-O gösterim sınırını aşıyor; ipucu kırpıldı"


_MAX_LABELS = 5
_MAX_NOTES = 4


@dataclass(frozen=True)
class _Path:
    """Kök döngüden bir döngüye kadar olan yol; ebeveynden artımlı kurulur (önbellekli)."""

    value: BigO
    labels: tuple[str, ...] = ()
    depth: int = 0
    flags: frozenset[str] = frozenset()
    notes: tuple[str, ...] = ()

    def extend(self, loop: LoopFact) -> _Path:
        flags, notes = set(self.flags), list(self.notes)
        value = self.value
        if "overflow" not in flags:
            value, overflow = _product(self.value.canonical, _FACTOR[loop.bound])
            if overflow:
                flags.add("overflow")
                notes.append(_OVERFLOW_NOTE)
        if loop.bound is LoopBound.UNKNOWN:
            flags.add("unknown")
            notes.append(f"satır {loop.line}: sınırı belirlenemeyen döngü n varsayıldı")
        if loop.bound is LoopBound.LOG and loop.kind in ("while", "do"):
            flags.add("while_log")
        if loop.counter_outer:
            flags.add("outer_counter")
            notes.append(
                f"satır {loop.line}: iç döngü sayacı dış döngüde sıfırlanmıyor "
                "(two-pointer/amortize olabilir; iç içe çarpım abartabilir)"
            )
        label = f"satır {loop.line} {loop.kind} ({loop.bound.value})"
        labels = (*self.labels, label)
        if len(labels) > _MAX_LABELS:  # derin yuvalamada gerekçe okunur kalsın
            labels = (*labels[:2], "…", *labels[-2:])
        return _Path(value, labels, self.depth + 1, frozenset(flags), tuple(notes[:_MAX_NOTES]))

    @property
    def label(self) -> str:
        return " × ".join(self.labels)


_ROOT = _Path(parse_bigo("1"))


class _Hinter:
    def __init__(self, facts: CodeFacts) -> None:
        self.facts = facts
        self.by_line: dict[tuple[str | None, int], int] = {}
        self.loops_of: dict[str | None, list[int]] = {}
        for index, loop in enumerate(facts.loops):
            self.by_line.setdefault((loop.function, loop.line), index)
            self.loops_of.setdefault(loop.function, []).append(index)
        self.calls_of: dict[str | None, list[CallFact]] = {}
        for call in facts.calls:
            self.calls_of.setdefault(call.function, []).append(call)
        self.by_simple: dict[str, list[str]] = {}
        for fn in facts.functions:
            names = self.by_simple.setdefault(simple_name(fn.name), [])
            if fn.name not in names:
                names.append(fn.name)
        self.recursion_of = {r.function: r for r in reversed(facts.recursion)}
        self.paths: dict[int, _Path] = {}
        self.memo: dict[str, ComplexityHint] = {}
        self.component: dict[str, list[str]] = {}

    def _parent(self, index: int) -> int | None:
        """Dış döngü indeksi; indeks yoksa (elle kurulmuş olgu) satırdan çözülür."""
        loop = self.facts.loops[index]
        if loop.parent_index is not None:
            return loop.parent_index if loop.parent_index < len(self.facts.loops) else None
        if loop.parent_line is None:
            return None
        return self.by_line.get((loop.function, loop.parent_line))

    def _path(self, index: int | None) -> _Path:
        """Döngünün yolu; zincir yinelemeli çözülür, her döngü bir kez hesaplanır."""
        if index is None:
            return _ROOT
        chain: list[int] = []
        seen: set[int] = set()
        current: int | None = index
        while current is not None and current not in self.paths and current not in seen:
            seen.add(current)
            chain.append(current)
            current = self._parent(current)
        base = self.paths.get(current, _ROOT) if current is not None else _ROOT
        for item in reversed(chain):
            base = base.extend(self.facts.loops[item])
            self.paths[item] = base
        return self.paths[index]

    def _call_loop(self, call: CallFact) -> int | None:
        if call.loop_index is not None:
            return call.loop_index if call.loop_index < len(self.facts.loops) else None
        if call.loop_line is None:
            return None
        return self.by_line.get((call.function, call.loop_line))

    def _loop_terms(self, fn: str | None) -> list[_Term]:
        terms = []
        for index in self.loops_of.get(fn, []):
            path = self._path(index)
            basis = f"{path.label} → {path.value.canonical}"
            terms.append(_Term(path.value, basis, set(path.flags), list(path.notes)))
        return terms

    def targets(self, fn: str | None, call: CallFact) -> list[str]:
        """Çağrının hedeflediği (bu dosyadaki) kullanıcı fonksiyonları; alıcılı çağrılar hariç."""
        if call.known_cost is not None:
            return []
        name = call.name.replace("this->", "").replace("this.", "")
        if "." in name or "->" in name:
            return []
        return [t for t in self.by_simple.get(simple_name(name), []) if t != fn]

    def _callee(self, targets: list[str]) -> ComplexityHint | None:
        """Aşırı yüklemeler arasında Big-O sırasına göre en pahalısı (eşitlikte en düşük güven)."""
        hints = [self.memo[t] for t in targets if t in self.memo]
        if not hints:
            return None
        top = _dominant([parse_bigo(h.value) for h in hints])
        tied = [h for h in hints if parse_bigo(h.value).same_class(top)]
        return min(tied, key=lambda h: _RANK[h.confidence])

    def _call_terms(self, fn: str | None, calls: list[CallFact]) -> tuple[list[_Term], list[int]]:
        """Çağrı terimleri ve karşılıklı özyineleme çağrı satırları."""
        terms: list[_Term] = []
        mutual: list[int] = []
        family = set(self.component.get(fn, [])) if fn is not None else set()
        for call in calls:
            if call.known_cost is not None:
                cost, amortized = parse_cost(call.known_cost)
                source = f"`{call.name}` ({call.known_cost})"
                flags = {"amortized"} if amortized else set()
            else:
                targets = self.targets(fn, call)
                if any(t in family for t in targets):
                    mutual.append(call.line)
                    continue
                callee = self._callee(targets)
                if callee is None:
                    continue
                cost = parse_bigo(callee.value)
                source = f"`{call.name}` çağrısı ({callee.value})"
                flags = {"callee_low" if callee.confidence == "low" else "callee_medium"}
            loop = self._call_loop(call)
            if cost.is_constant and not (flags and loop is not None):
                continue  # sabit maliyet katkısızdır; döngüdeki amortize O(1) güveni etkiler
            path = self._path(loop)
            value, overflow = _product(path.value.canonical, cost.canonical)
            if overflow:
                flags.add("overflow")
            where = f" × {path.label}" if path.labels else ""
            basis = f"satır {call.line} {source}{where} → {value.canonical}"
            terms.append(_Term(value, basis, flags | path.flags, list(path.notes)))
        return terms, mutual

    def _mutual_term(self, fn: str, lines: list[int], work: BigO) -> _Term:
        others = " ↔ ".join(sorted(set(self.component[fn]) - {fn}))
        where = ", ".join(f"satır {n}" for n in sorted(set(lines)))
        if len(lines) > 1:
            return _Term(
                parse_bigo("2^n"),
                f"karşılıklı özyineleme ({fn} ↔ {others}; {where}): tek çağrıda birden çok "
                "dal → üstel şüphe",
                {"recursion", "exponential"},
            )
        value = _product(work.canonical, "n")[0]
        return _Term(
            value,
            f"karşılıklı özyineleme ({fn} ↔ {others}; {where}), iş {work.canonical} "
            f"→ {value.canonical} (derinlik bilinmiyor)",
            {"recursion"},
        )

    def _recursion_term(self, fn: str, work: BigO) -> _Term | None:
        rec = self.recursion_of.get(fn)
        if rec is None:
            return None
        branching = rec.branching_factor
        if branching > 1 and not rec.halving:
            return _Term(
                parse_bigo("2^n"),
                f"özyineleme: tek yolda {branching} öz-çağrı → üstel şüphe "
                "(memoizasyon statik olarak görülmez)",
                {"recursion", "exponential"},
            )
        if branching > 1:
            value = _dominant([parse_bigo("n"), _product(work.canonical, "log n")[0]])
            label = f"böl-yönet özyineleme ({branching} dal, yarılama)"
        elif rec.halving:
            value = _product(work.canonical, "log n")[0]
            label = "yarılayan özyineleme"
        else:
            value = _product(work.canonical, "n")[0]
            label = "doğrusal özyineleme"
        return _Term(value, f"{label}, iş {work.canonical} → {value.canonical}", {"recursion"})

    def _hint(self, fn: str | None) -> ComplexityHint:
        terms = self._loop_terms(fn)
        call_terms, mutual = self._call_terms(fn, self.calls_of.get(fn, []))
        terms += call_terms
        if fn is not None:
            work = _dominant([t.value for t in terms])
            recursion = self._recursion_term(fn, work)
            if recursion is not None:
                terms.append(recursion)
            if mutual:
                terms.append(self._mutual_term(fn, mutual, work))
        return _combine(terms, fn)

    def compute_all(self, names: list[str]) -> None:
        """Tüm fonksiyon ipuçları; çağrılanlar önce (yinelemeli, derin zincirde de güvenli)."""
        edges = {
            fn: [t for call in self.calls_of.get(fn, []) for t in self.targets(fn, call)]
            for fn in names
        }
        for component in strongly_connected(names, edges):
            for fn in component:
                self.component[fn] = component
            for fn in component:
                self.memo[fn] = self._hint(fn)


def _combine(terms: list[_Term], fn: str | None) -> ComplexityHint:
    label = fn or FILE_SCOPE
    if not terms:
        return ComplexityHint(
            value="1",
            confidence="high",
            basis=[f"{label}: döngü, bilinen maliyetli çağrı veya özyineleme yok → 1"],
            function=fn,
        )
    value = _dominant([t.value for t in terms])
    dominant = [t for t in terms if t.value.same_class(value)]
    flags = set().union(*(t.flags for t in dominant))
    if any("recursion" in t.flags for t in terms):
        flags.add("recursion")
    confidence: Confidence = "high"
    if flags & _LOW_FLAGS:
        confidence = "low"
    elif flags & _MEDIUM_FLAGS:
        confidence = "medium"
    # sıra: ilk baskın gerekçe, güveni açıklayan notlar, kalan gerekçeler (sınırda notlar kalsın)
    reasons = [f"{label}: {t.basis}" for t in dominant]
    notes = [n for t in dominant for n in t.notes]
    basis: list[str] = []
    for text in [*reasons[:1], *notes, *reasons[1:]]:
        if text not in basis:
            basis.append(text)
    return ComplexityHint(
        value=value.canonical,
        confidence=confidence,
        basis=basis[:MAX_BASIS],
        function=fn,
        exponential_suspect="exponential" in flags,
    )


def function_hints(facts: CodeFacts) -> dict[str, ComplexityHint]:
    """Fonksiyon adı → ipucu (fonksiyon dışı döngü/çağrılar `<dosya>` altında)."""
    hinter = _Hinter(facts)
    names: list[str] = []
    for fn in facts.functions:
        if fn.name not in names:
            names.append(fn.name)
    hinter.compute_all(names)
    result = {name: hinter.memo[name] for name in names}
    if hinter.loops_of.get(None) or any(c.known_cost for c in hinter.calls_of.get(None, [])):
        result[FILE_SCOPE] = hinter._hint(None)
    return result


def compute_hint(facts: CodeFacts) -> ComplexityHint:
    """Dosya ipucu: en pahalı fonksiyonun ipucu (eşitlikte en düşük güven).

    İstisna fırlatmaz: beklenmedik bir durumda düşük güvenli, gerekçeli `1` döner.
    """
    try:
        return _file_hint(facts)
    except Exception as exc:  # ipucu yardımcıdır; analizi asla durdurmamalı
        return ComplexityHint(
            value="1",
            confidence="low",
            basis=[f"İpucu hesaplanamadı ({type(exc).__name__}); yok sayılmalı."],
        )


def _file_hint(facts: CodeFacts) -> ComplexityHint:
    hints = list(function_hints(facts).values())
    if not hints:
        return ComplexityHint(
            value="1",
            confidence="low",
            basis=["Analiz edilecek fonksiyon veya döngü bulunamadı; ipucu yok sayılabilir."],
        )
    top = _dominant([parse_bigo(h.value) for h in hints])
    tied = [h for h in hints if parse_bigo(h.value).same_class(top)]
    winner = min(tied, key=lambda h: _RANK[h.confidence])
    return winner.model_copy(
        update={"exponential_suspect": any(h.exponential_suspect for h in tied)}
    )
