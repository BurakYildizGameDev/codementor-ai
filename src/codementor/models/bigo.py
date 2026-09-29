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

import re
import string
from dataclasses import dataclass
from fractions import Fraction
from typing import NoReturn

__all__ = [
    "MAX_EXPONENT",
    "MAX_INPUT_LENGTH",
    "BigO",
    "BigOComparisonError",
    "BigOError",
    "BigOParseError",
    "parse_bigo",
]

MAX_INPUT_LENGTH = 200
MAX_EXPONENT = 100
_MAX_EXP_BASE = 10**100


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


class _InvalidError(Exception):
    """Ayrıştırıcı içi hata; `parse_bigo` bunu `BigOParseError`a çevirir."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


# --------------------------------------------------------------------------- anlamsal model


@dataclass(frozen=True, slots=True, order=True)
class _Factor:
    """Tek bir değişkenin çarpan katkısı: `(n!)^factorial · exp_base^n · n^power · log^log_power n`.

    Alan sırası asimptotik büyüme önceliğidir; bu yüzden `order=True` ile gelen
    sözlüksel karşılaştırma tek değişkenli sıralamanın ta kendisidir.
    """

    factorial: int = 0
    exp_base: Fraction = Fraction(1)
    power: Fraction = Fraction(0)
    log_power: Fraction = Fraction(0)


_IDENTITY = _Factor()

_Term = tuple[tuple[str, _Factor], ...]  # değişkene göre sıralı, birim çarpanlar hariç
_Expr = tuple[_Term, ...]  # sadeleştirilmiş, biçime göre sıralı toplam

_CONSTANT_TERM: _Term = ()
_CONSTANT: _Expr = (_CONSTANT_TERM,)


def _make_term(factors: dict[str, _Factor]) -> _Term:
    return tuple(sorted((v, f) for v, f in factors.items() if f != _IDENTITY))


def _var_expr(var: str, factor: _Factor) -> _Expr:
    return (_make_term({var: factor}),)


def _check_base(base: Fraction) -> Fraction:
    if base.numerator > _MAX_EXP_BASE:
        raise _InvalidError("üstel taban çok büyük")
    return base


def _mul_factor(a: _Factor, b: _Factor) -> _Factor:
    return _Factor(
        factorial=a.factorial + b.factorial,
        exp_base=_check_base(a.exp_base * b.exp_base),
        power=a.power + b.power,
        log_power=a.log_power + b.log_power,
    )


def _pow_factor(f: _Factor, k: Fraction) -> _Factor:
    if k.denominator != 1 and (f.factorial or f.exp_base != 1):
        raise _InvalidError("üstel veya faktöriyel terimin kesirli üssü desteklenmiyor")
    return _Factor(
        factorial=f.factorial * int(k),
        exp_base=_check_base(f.exp_base ** int(k)),
        power=f.power * k,
        log_power=f.log_power * k,
    )


def _mul_term(a: _Term, b: _Term) -> _Term:
    merged = dict(a)
    for var, f in b:
        merged[var] = _mul_factor(merged.get(var, _IDENTITY), f)
    return _make_term(merged)


def _dominates(a: _Term, b: _Term) -> bool:
    """`a`, `b`yi asimptotik olarak baskılıyor mu (her değişkende ≥)?"""
    fa, fb = dict(a), dict(b)
    return all(fa.get(v, _IDENTITY) >= fb.get(v, _IDENTITY) for v in fa.keys() | fb.keys())


def _simplify(terms: set[_Term]) -> _Expr:
    kept = [t for t in terms if not any(o != t and _dominates(o, t) for o in terms)]
    return tuple(sorted(kept, key=_format_term))


def _add(a: _Expr, b: _Expr) -> _Expr:
    return _simplify(set(a) | set(b))


def _mul(a: _Expr, b: _Expr) -> _Expr:
    return _simplify({_mul_term(x, y) for x in a for y in b})


def _pow(a: _Expr, k: Fraction) -> _Expr:
    if len(a) == 1:
        (term,) = a
        return _simplify({_make_term({v: _pow_factor(f, k) for v, f in term})})
    if k.denominator != 1:
        raise _InvalidError("toplamın kesirli üssü desteklenmiyor")
    result = _CONSTANT
    for _ in range(int(k)):
        result = _mul(result, a)
    return result


def _log(a: _Expr) -> _Expr:
    if len(a) != 1:
        raise _InvalidError("toplamın logaritması desteklenmiyor")
    (term,) = a
    parts: set[_Term] = set()
    for var, f in term:
        if f.factorial:  # log(n!) = Θ(n log n)
            parts.add(_make_term({var: _Factor(power=Fraction(1), log_power=Fraction(1))}))
        elif f.exp_base != 1:  # log(c^n · ...) = Θ(n)
            parts.add(_make_term({var: _Factor(power=Fraction(1))}))
        elif f.power > 0:  # log(n^k · log^j n) = Θ(log n)
            parts.add(_make_term({var: _Factor(log_power=Fraction(1))}))
        else:
            raise _InvalidError("iç içe logaritma (log log n) desteklenmiyor")
    return _simplify(parts) if parts else _CONSTANT


# --------------------------------------------------------------------------- biçimlendirme


def _format_number(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    den, twos, fives = x.denominator, 0, 0
    while den % 2 == 0:
        den, twos = den // 2, twos + 1
    while den % 5 == 0:
        den, fives = den // 5, fives + 1
    if den != 1:  # yalnızca ondalık girdilerden türediği için oluşmaz
        raise _InvalidError("sonlu ondalık olmayan üs")
    k = max(twos, fives)
    digits = str(x.numerator * 10**k // x.denominator).rjust(k + 1, "0")
    return f"{digits[:-k]}.{digits[-k:]}".rstrip("0")


def _format_factor(var: str, f: _Factor) -> str:
    parts: list[str] = []
    if f.power:
        parts.append(var if f.power == 1 else f"{var}^{_format_number(f.power)}")
    if f.log_power:
        log = "log" if f.log_power == 1 else f"log^{_format_number(f.log_power)}"
        parts.append(f"{log} {var}")
    if f.exp_base != 1:
        parts.append(f"{_format_number(f.exp_base)}^{var}")
    if f.factorial:
        parts.append(f"{var}!" if f.factorial == 1 else f"{var}!^{f.factorial}")
    return " ".join(parts)


def _format_term(term: _Term) -> str:
    return "*".join(_format_factor(v, f) for v, f in term) if term else "1"


_SUPERSCRIPT_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
_TO_SUPERSCRIPT = str.maketrans("0123456789", _SUPERSCRIPT_DIGITS)
_INT_EXPONENT_RE = re.compile(r"\^(\d+)(?![\d.])")


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


# --------------------------------------------------------------------------- tokenizer


@dataclass(frozen=True, slots=True)
class _Token:
    kind: str  # num | var | log | sqrt | ^ * + / ( ) ! _
    text: str
    num: Fraction = Fraction(0)


_LETTERS = frozenset(string.ascii_lowercase)
_DIGITS = frozenset(string.digits)
_KEYWORDS = {"sqrt": "sqrt", "log": "log", "lg": "log", "ln": "log"}
_SUBSCRIPT_DIGITS = "₀₁₂₃₄₅₆₇₈₉"
_FROM_SCRIPT = str.maketrans(_SUPERSCRIPT_DIGITS + _SUBSCRIPT_DIGITS, "0123456789" * 2)
_SINGLE = {
    "^": "^",
    "*": "*",
    "·": "*",
    "×": "*",  # noqa: RUF001 — çarpı işareti bilerek destekleniyor
    "∙": "*",
    "⋅": "*",
    "+": "+",
    "/": "/",
    "(": "(",
    "[": "(",
    "{": "(",
    ")": ")",
    "]": ")",
    "}": ")",
    "!": "!",
    "_": "_",
}
_NUMBER_RE = re.compile(r"[0-9]+(?:\.[0-9]+)?")


def _split_word(word: str) -> list[_Token]:
    """Harf dizisini anahtar sözcük + tek harfli değişkenlere böler (`nlogn` → n log n)."""
    tokens: list[_Token] = []
    k = 0
    consecutive_vars = 0
    while k < len(word):
        for kw, kind in _KEYWORDS.items():
            if word.startswith(kw, k):
                tokens.append(_Token(kind, kw))
                k += len(kw)
                consecutive_vars = 0
                break
        else:
            tokens.append(_Token("var", word[k]))
            k += 1
            consecutive_vars += 1
            if consecutive_vars >= 3:
                raise _InvalidError(f"tanımsız sözcük {word!r}")
    return tokens


def _script_run(s: str, i: int, alphabet: str) -> tuple[Fraction, int]:
    j = i
    while j < len(s) and s[j] in alphabet:
        j += 1
    return Fraction(int(s[i:j].translate(_FROM_SCRIPT))), j


def _tokenize(text: str) -> list[_Token]:
    s = text.lower()
    tokens: list[_Token] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c in _DIGITS:
            m = _NUMBER_RE.match(s, i)
            assert m is not None
            tokens.append(_Token("num", m.group(), Fraction(m.group())))
            i = m.end()
        elif c in _LETTERS:
            j = i
            while j < len(s) and s[j] in _LETTERS:
                j += 1
            tokens.extend(_split_word(s[i:j]))
            i = j
        elif c in _SUPERSCRIPT_DIGITS:
            value, i = _script_run(s, i, _SUPERSCRIPT_DIGITS)
            tokens += [_Token("^", "^"), _Token("num", str(value), value)]
        elif c == "ⁿ":
            tokens += [_Token("^", "^"), _Token("var", "n")]
            i += 1
        elif c in _SUBSCRIPT_DIGITS:
            value, i = _script_run(s, i, _SUBSCRIPT_DIGITS)
            tokens += [_Token("_", "_"), _Token("num", str(value), value)]
        elif c in _SINGLE:
            tokens.append(_Token(_SINGLE[c], c))
            i += 1
        else:
            raise _InvalidError(f"beklenmeyen karakter {c!r} (konum {i})")
    return tokens


# --------------------------------------------------------------------------- ayrıştırıcı

_TERM_STARTS = frozenset({"num", "var", "log", "sqrt", "("})


class _Parser:
    def __init__(self, tokens: list[_Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _peek(self, offset: int = 0) -> _Token | None:
        i = self.pos + offset
        return self.tokens[i] if i < len(self.tokens) else None

    def _at(self, kind: str, offset: int = 0) -> bool:
        tok = self._peek(offset)
        return tok is not None and tok.kind == kind

    def _advance(self) -> _Token:
        tok = self._peek()
        if tok is None:
            raise _InvalidError("ifade beklenmedik şekilde bitti")
        self.pos += 1
        return tok

    def _expect(self, kind: str) -> _Token:
        tok = self._advance()
        if tok.kind != kind:
            self._fail(f"{kind!r} beklenirken {tok.text!r} geldi")
        return tok

    @staticmethod
    def _fail(reason: str) -> NoReturn:
        raise _InvalidError(reason)

    def parse(self) -> _Expr:
        self._strip_wrapper()
        if not self.tokens:
            self._fail("boş ifade")
        expr = self._expr()
        if (tok := self._peek()) is not None:
            self._fail(f"beklenmeyen {tok.text!r}")
        return expr

    def _strip_wrapper(self) -> None:
        t = self.tokens
        if len(t) >= 2 and t[0].kind == "var" and t[0].text == "o" and t[1].kind == "(":
            depth = 0
            for i in range(1, len(t)):
                depth += {"(": 1, ")": -1}.get(t[i].kind, 0)
                if depth == 0:
                    if i == len(t) - 1:
                        self.tokens = t[2:-1]
                    return

    def _expr(self) -> _Expr:
        expr = self._term()
        while self._at("+"):
            self._advance()
            expr = _add(expr, self._term())
        return expr

    def _term(self) -> _Expr:
        expr = self._postfix()
        while (tok := self._peek()) is not None:
            if tok.kind == "*":
                self._advance()
                expr = _mul(expr, self._postfix())
            elif tok.kind == "/":
                self._advance()
                if not self._at("num"):
                    self._fail("yalnızca sabit bir sayıya bölme desteklenir")
                self._advance()
            elif tok.kind in _TERM_STARTS:
                expr = _mul(expr, self._postfix())
            else:
                break
        return expr

    def _postfix(self) -> _Expr:
        if self._at("num"):
            base = self._advance().num
            if not self._at("^"):
                return _CONSTANT
            self._advance()
            exponent = self._exponent()
            if isinstance(exponent, Fraction):
                return _CONSTANT
            if base <= 1:
                self._fail("üstel taban 1'den büyük olmalı")
            return _var_expr(exponent, _Factor(exp_base=_check_base(base)))

        bare_var = self._at("var")
        expr = self._primary()
        while True:
            if self._at("!"):
                if not bare_var:
                    self._fail("faktöriyel yalnızca tek bir değişkene uygulanabilir (ör. n!)")
                self._advance()
                ((var, _),) = expr[0]
                expr = _var_expr(var, _Factor(factorial=1))
            elif self._at("^"):
                self._advance()
                exponent = self._exponent()
                if isinstance(exponent, str):
                    self._fail("değişken üs yalnızca sayısal tabanla desteklenir (ör. 2^n)")
                expr = _pow(expr, exponent)
            else:
                return expr
            bare_var = False

    def _primary(self) -> _Expr:
        tok = self._advance()
        if tok.kind == "var":
            return _var_expr(tok.text, _Factor(power=Fraction(1)))
        if tok.kind == "(":
            expr = self._expr()
            self._expect(")")
            return expr
        if tok.kind == "log":
            return self._log_call()
        if tok.kind == "sqrt":
            return _pow(self._func_arg(), Fraction(1, 2))
        self._fail(f"beklenmeyen {tok.text!r}")

    def _log_call(self) -> _Expr:
        # Taban yok sayılır: log_2 n, log2 n, log₂ n → log n
        if self._at("_"):
            self._advance()
            if self._advance().kind not in {"num", "var"}:
                self._fail("logaritma tabanı geçersiz")
        elif self._at("num") and (nxt := self._peek(1)) is not None and nxt.kind in _TERM_STARTS:
            self._advance()
        power = Fraction(1)
        if self._at("^"):
            self._advance()
            exponent = self._exponent()
            if isinstance(exponent, str):
                self._fail("logaritmanın üssü sayı olmalı")
            power = exponent
        return _pow(_log(self._func_arg()), power)

    def _func_arg(self) -> _Expr:
        if self._at("("):
            self._advance()
            expr = self._expr()
            self._expect(")")
            return expr
        return self._postfix()

    def _exponent(self) -> str | Fraction:
        """Üs: sayı ise `Fraction`, değişken ise adı."""
        tok = self._advance()
        if tok.kind == "(":
            inner = self._advance()
            self._expect(")")
            tok = inner
        if tok.kind == "var":
            return tok.text
        if tok.kind != "num":
            self._fail(f"üs beklenirken {tok.text!r} geldi")
        if tok.num > MAX_EXPONENT:
            self._fail(f"üs çok büyük (en fazla {MAX_EXPONENT})")
        return tok.num


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
