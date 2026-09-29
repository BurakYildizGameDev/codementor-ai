"""Big-O tokenizer ve özyinelemeli ayrıştırıcı (`bigo.py` iç modülü)."""

from __future__ import annotations

import re
import string
from dataclasses import dataclass
from fractions import Fraction
from typing import NoReturn

from codementor.models._bigo_algebra import (
    _CONSTANT,
    _SUPERSCRIPT_DIGITS,
    _add,
    _check_base,
    _Expr,
    _Factor,
    _InvalidError,
    _log,
    _mul,
    _pow,
    _var_expr,
)

MAX_EXPONENT = 100


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
