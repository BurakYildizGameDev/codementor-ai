"""Big-O terim cebiri ve kanonik biçimlendirme (`bigo.py` iç modülü).

İfade, terimlerin toplamıdır; her terim değişken başına
`n^a · log^b n · (log log n)^j · c^n · (n!)^k` çarpanlarından oluşur.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction

_MAX_EXP_BASE = 10**100


class _InvalidError(Exception):
    """Ayrıştırıcı içi hata; `parse_bigo` bunu `BigOParseError`a çevirir."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


# --------------------------------------------------------------------------- anlamsal model


@dataclass(frozen=True, slots=True, order=True)
class _Factor:
    """Tek değişkenin çarpan katkısı:
    `(n!)^factorial · exp_base^n · n^power · log^log_power n · (log log n)^log_log_power`.

    Alan sırası asimptotik büyüme önceliğidir; bu yüzden `order=True` ile gelen
    sözlüksel karşılaştırma tek değişkenli sıralamanın ta kendisidir
    (`1 < log log n < log n < n`; `log_power` bu yüzden `log_log_power`dan önce gelir).
    """

    factorial: int = 0
    exp_base: Fraction = Fraction(1)
    power: Fraction = Fraction(0)
    log_power: Fraction = Fraction(0)
    log_log_power: Fraction = Fraction(0)


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
        log_log_power=a.log_log_power + b.log_log_power,
    )


def _pow_factor(f: _Factor, k: Fraction) -> _Factor:
    if k.denominator != 1 and (f.factorial or f.exp_base != 1):
        raise _InvalidError("üstel veya faktöriyel terimin kesirli üssü desteklenmiyor")
    return _Factor(
        factorial=f.factorial * int(k),
        exp_base=_check_base(f.exp_base ** int(k)),
        power=f.power * k,
        log_power=f.log_power * k,
        log_log_power=f.log_log_power * k,
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
        elif f.log_power > 0:  # log(log^j n) = j·log log n = Θ(log log n)
            parts.add(_make_term({var: _Factor(log_log_power=Fraction(1))}))
        else:  # yalnızca log log n: log log log n modellenmiyor
            raise _InvalidError("iç içe logaritma (log log log n) desteklenmiyor")
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
    if f.log_log_power:
        log_log = f"log log {var}"
        parts.append(
            log_log if f.log_log_power == 1 else f"({log_log})^{_format_number(f.log_log_power)}"
        )
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
