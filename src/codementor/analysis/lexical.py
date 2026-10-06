"""Doğrusal zamanlı sözcük düzeyi yardımcılar (C, C++, C#).

`mask_non_code` yorumların ve metin/karakter sabitlerinin **içeriğini** aynı uzunlukta
boşlukla değiştirir; satır sonlarını ve tırnakları korur. Böylece:

- dil tespiti, `printf("=> ::")` gibi metinlerden sahte sinyal almaz,
- makro/parantez eşleme, yorum veya metin içindeki `(`/`)` ile şaşmaz,
- konumlar (satır/karakter) değişmez.

C++ ham metinleri (`R"(...)"`, `u8R"x(...)x"`, `LR"(...)"` ...) kaçış ve satır sonu
tanımadığından ayrıca işlenir (Faz 55): `/*` ya da `#include` görünümü taşıyan
içerik maske girer, açılış/kapanış dizileri yerinde kalır.

Tek geçişlidir: kullanıcı kodu güvenilmez veridir (mimari §12), kötü niyetli girdide
bile süre girdi boyutuyla doğrusal kalmalıdır.
"""

from __future__ import annotations

import re

# Sabit genişlikli pencerede aranır: uzun satırlarda da doğrusal kalsın
_INCLUDE_TAIL = re.compile(r"#[ \t]*include[ \t]*$")
_INCLUDE_WINDOW = 32

_WORD_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")


def _blank(segment: str) -> str:
    return "".join("\n" if c == "\n" else " " for c in segment)


def _string_end(text: str, start: int, quote: str, *, verbatim: bool) -> int:
    """`start` açılış tırnağı; kapanış tırnağının konumu (yoksa içerik sonu)."""
    i = start + 1
    n = len(text)
    while i < n:
        c = text[i]
        if verbatim:  # C# @"..." : satır sonu serbest, "" kaçıştır
            if c == '"':
                if i + 1 < n and text[i + 1] == '"':
                    i += 2
                    continue
                return i
        elif c == "\\":
            i += 2
            continue
        elif c == quote or c == "\n":
            return i
        i += 1
    return n


# C++ ham metin önekleri (raw string); dizi, tanımlayıcının parçası olmamalı
_RAW_PREFIXES = frozenset({"R", "LR", "uR", "UR", "u8R"})
_MAX_DELIM = 16  # C++ standardının d-char uzunluk sınırı
_DELIM_STOP = frozenset(" \t\r\n\f\v()\\")


def _raw_open(text: str, quote: int) -> int:
    """`quote` konumundaki `"` bir C++ ham metin açışıysa `(` konumu, değilse -1.

    `R"delim(` biçimi: önek (`R`, `u8R`, `LR` ...) bir tanımlayıcının parçası
    olmamalı (`FOO_R"x(" ham metin değildir); `delim` en fazla 16 karakter olmalı
    ve boşluk, `(`, `)` ya da `\\` içermemelidir.
    """
    start = quote - 1
    while start >= 0 and text[start] in _WORD_CHARS:
        start -= 1
    if text[start + 1 : quote] not in _RAW_PREFIXES:
        return -1
    k, n = quote + 1, len(text)
    while k < n:
        ch = text[k]
        if ch == "(":
            return k
        if k - quote > _MAX_DELIM or ch in _DELIM_STOP:
            return -1
        k += 1
    return -1


def _raw_string_end(text: str, open_paren: int, delim: str) -> int:
    """Kapanış `)delim"` dizisinin son `"` konumu; kapanmamışsa metin uzunluğu."""
    pos = text.find(")" + delim + '"', open_paren + 1)
    return pos + len(delim) + 1 if pos >= 0 else len(text)


def mask_non_code(text: str) -> str:
    """Yorum ve metin sabiti içeriklerini boşlukla maskeler; uzunluk ve satırlar korunur."""
    parts: list[str] = []
    cursor = 0
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == "/" and i + 1 < n and text[i + 1] in "/*":
            if text[i + 1] == "/":
                end = text.find("\n", i)
                end = n if end < 0 else end
            else:
                end = text.find("*/", i + 2)
                end = n if end < 0 else end + 2
            parts += [text[cursor:i], _blank(text[i:end])]
            cursor = i = end
        elif c == '"' and _INCLUDE_TAIL.search(text, max(0, i - _INCLUDE_WINDOW), i):
            # `#include "CoreMinimal.h"`: yol dil/motor sinyalidir; maskelenmeden atlanır
            i = _string_end(text, i, c, verbatim=False) + 1
        elif c == '"' or (c == "'" and (i == 0 or text[i - 1] not in _WORD_CHARS)):
            # `'` bir sözcük karakterinden sonra geliyorsa C++14 basamak ayırıcısıdır (1'000)
            verbatim = c == '"' and i > 0 and text[i - 1] == "@"
            raw = -1 if c != '"' or verbatim else _raw_open(text, i)
            if raw >= 0:  # C++ ham metni: kaçış yok, `)delim"` ile biter, satır sonu taşır
                delim = text[i + 1 : raw]
                close = _raw_string_end(text, raw, delim)
                if close < n:  # kapanmış: açılış/kapanış görünür kalır, içerik boşluk
                    closer = close - len(delim) - 1
                    parts += [
                        text[cursor : raw + 1],
                        _blank(text[raw + 1 : closer]),
                        text[closer : close + 1],
                    ]
                    cursor = i = close + 1
                else:  # kapanmamış ham metin: dosya sonuna kadar maskele
                    parts += [text[cursor : raw + 1], _blank(text[raw + 1 :])]
                    cursor = i = n
                continue
            close = _string_end(text, i, c, verbatim=verbatim)
            parts += [text[cursor : i + 1], _blank(text[i + 1 : close])]
            closed = close < n and text[close] == c
            cursor = i = close + 1 if closed else close
            if closed:
                parts.append(c)
        else:
            i += 1
    parts.append(text[cursor:])
    return "".join(parts)


def matching_parens(text: str) -> dict[int, int]:
    """Her `(` konumu için eşleşen `)` konumu (tek geçiş, yığın). Eşsizler yer almaz.

    Yorum/metin içindeki parantezlerin sayılmaması için `mask_non_code` çıktısı verilmelidir.
    """
    pairs: dict[int, int] = {}
    stack: list[int] = []
    for i, c in enumerate(text):
        if c == "(":
            stack.append(i)
        elif c == ")" and stack:
            pairs[stack.pop()] = i
    return pairs
