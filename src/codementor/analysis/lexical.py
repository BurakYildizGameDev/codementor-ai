"""Doğrusal zamanlı sözcük düzeyi yardımcılar (C, C++, C#).

`mask_non_code` yorumların ve metin/karakter sabitlerinin **içeriğini** aynı uzunlukta
boşlukla değiştirir; satır sonlarını ve tırnakları korur. Böylece:

- dil tespiti, `printf("=> ::")` gibi metinlerden sahte sinyal almaz,
- makro/parantez eşleme, yorum veya metin içindeki `(`/`)` ile şaşmaz,
- konumlar (satır/karakter) değişmez.

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
