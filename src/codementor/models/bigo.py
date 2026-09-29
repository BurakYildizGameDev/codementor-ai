"""Big-O ifadesi ayrıştırıcı ve normalleştirici (mimari §5.6).

Dilbilgisi (EBNF, büyük/küçük harf duyarsız; `O(...)` sarmalayıcısı isteğe bağlı):

    expr     := term ("+" term)*
    term     := postfix (("*" | "/" NUMBER | <bitişik>) postfix)*
    postfix  := NUMBER ("^" exponent)?
              | primary ("!" | "^" exponent)*
    primary  := VAR | "(" expr ")" | LOG base? ("^" exponent)? arg | SQRT arg
    arg      := "(" expr ")" | postfix
    exponent := NUMBER | VAR | "(" (NUMBER | VAR) ")"

Anlamsal model: ifade, terimlerin toplamıdır; her terim değişken başına
`n^a · log^b n · c^n · (n!)^k` çarpanlarından oluşur. Sabit katsayılar atılır,
başka bir terim tarafından asimptotik olarak baskılanan terimler silinir.
"""

from __future__ import annotations

from dataclasses import dataclass

from codementor.models._bigo_algebra import (
    _INT_EXPONENT_RE,
    _TO_SUPERSCRIPT,
    _Expr,
    _format_term,
    _InvalidError,
)
from codementor.models._bigo_parser import MAX_EXPONENT, _Parser, _tokenize

__all__ = [
    "MAX_EXPONENT",
    "MAX_INPUT_LENGTH",
    "BigO",
    "BigOComparisonError",
    "BigOError",
    "BigOParseError",
    "parse_bigo",
    "parse_cost",
]

MAX_INPUT_LENGTH = 200


class BigOError(ValueError):
    """Big-O işlemleri için temel hata."""


class BigOParseError(BigOError):
    """Metin geçerli bir Big-O ifadesi değil."""

    def __init__(self, text: str, reason: str) -> None:
        super().__init__(f"Big-O ifadesi ayrıştırılamadı: {text!r} ({reason})")
        self.text = text
        self.reason = reason


class BigOComparisonError(BigOError):
    """Çok değişkenli ifadeler arasında sıralama istendi."""


# --------------------------------------------------------------------------- değer nesnesi


@dataclass(frozen=True, slots=True, repr=False)
class BigO:
    """Normalleştirilmiş Big-O sınıfı. `parse_bigo` ile oluşturulur.

    Eşitlik ve hash kanonik biçime dayanır. `<`, `<=`, `>`, `>=` yalnızca tek
    değişkenli (veya sabit) ifadelerde tanımlıdır; aksi halde `BigOComparisonError`.
    """

    terms: _Expr

    @property
    def canonical(self) -> str:
        """Kanonik metin, ör. `n^2`, `n log n`, `e + v`."""
        return " + ".join(_format_term(t) for t in self.terms)

    @property
    def display(self) -> str:
        """Okunabilir gösterim, ör. `O(n²)`."""
        body = _INT_EXPONENT_RE.sub(lambda m: m.group(1).translate(_TO_SUPERSCRIPT), self.canonical)
        return f"O({body})"

    @property
    def variables(self) -> frozenset[str]:
        """İfadedeki değişken adları (küçük harf)."""
        return frozenset(v for term in self.terms for v, _ in term)

    @property
    def is_constant(self) -> bool:
        return not self.variables

    @property
    def is_univariate(self) -> bool:
        return len(self.variables) == 1

    def same_class(self, other: BigO) -> bool:
        """Aynı asimptotik sınıf mı? Çok değişkenli ifadelerde de çalışır."""
        return self.terms == other.terms

    def _compare(self, other: BigO) -> int:
        if self.is_constant or other.is_constant:
            return int(not self.is_constant) - int(not other.is_constant)
        if len(self.variables | other.variables) > 1:
            raise BigOComparisonError(
                f"Çok değişkenli Big-O ifadeleri karşılaştırılamaz: "
                f"{self.canonical!r} ile {other.canonical!r}; same_class() kullanın."
            )
        a, b = self.terms[0][0][1], other.terms[0][0][1]
        return (a > b) - (a < b)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BigO):
            return NotImplemented
        return self._compare(other) < 0

    def __le__(self, other: object) -> bool:
        if not isinstance(other, BigO):
            return NotImplemented
        return self._compare(other) <= 0

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, BigO):
            return NotImplemented
        return self._compare(other) > 0

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, BigO):
            return NotImplemented
        return self._compare(other) >= 0

    def __str__(self) -> str:
        return self.canonical

    def __repr__(self) -> str:
        return f"BigO({self.canonical!r})"


def parse_bigo(text: str) -> BigO:
    """Serbest biçimli Big-O metnini normalleştirir (`O(N²)` → `n^2`).

    Raises:
        BigOParseError: metin desteklenen dilbilgisine uymuyorsa.
    """
    if not isinstance(text, str):
        raise TypeError(f"parse_bigo metin bekler, {type(text).__name__} geldi")
    if len(text) > MAX_INPUT_LENGTH:
        raise BigOParseError(text, f"ifade çok uzun (en fazla {MAX_INPUT_LENGTH} karakter)")
    try:
        return BigO(_Parser(_tokenize(text)).parse())
    except _InvalidError as exc:
        raise BigOParseError(text, exc.reason) from None
    except RecursionError:
        raise BigOParseError(text, "ifade çok derin iç içe") from None


def parse_cost(text: str) -> tuple[BigO, bool]:
    """Maliyet metni: sondaki `*` amortize işaretidir (`1*` → (O(1), True)).

    Raises:
        BigOParseError: `*` atıldıktan sonra metin geçerli bir Big-O değilse.
    """
    stripped = text.strip()
    amortized = stripped.endswith("*")
    return parse_bigo(stripped.removesuffix("*")), amortized
