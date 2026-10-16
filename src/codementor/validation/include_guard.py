"""Include koruması (mimari §5.2.3, ADR-0009).

Derleyici konteyner olmadan çalıştığı için kullanıcı kodu, derleyiciye verilmeden önce
host dosya sistemine uzanabilecek her önişlemci yapısı için taranır. Bir bulgu varsa
Tier 1 hiç çalıştırılmaz (`SKIPPED` + uyarı).

**Fail-closed tasarım.** Güvenlik kararı yorum/metin maskeleyicisinin doğruluğuna
dayanmaz: maskeleyici derleyiciyle her sözcük ayrımında (önekli karakter sabitleri
`L'`, `u8'`; ham metinler `R"(...)"`; `@"`; `b'` ...) aynı fikirde olmayabilir ve bu
fark bir `#include` satırını "yorum içinde" gösterebilir. Bu yüzden:

1. Trigraph ve token yapıştırma (`##`, `%:%:`) tümden reddedilir.
2. `\\` + (boşluk) + satır sonu gcc/clang gibi birleştirilir; `\\f`/`\\v` boşluk sayılır.
3. `#include`/`#import`/`#include_next`/`#embed`/`#pragma` sözcükleri **maskelenmemiş**
   metinde her yerde aranır; hedef yolu güvenli değilse (mutlak, `..`, sürücü, `:`, `\\`,
   Windows aygıt adı, boş) yorum/metin içinde olsa bile reddedilir. `#embed` ve
   `#pragma ... dependency` her yerde reddedilir.
4. Hedefi olmayan (`#include MACRO`) biçim yalnızca yönerge konumunda reddedilir: satır
   başı (maskelenmiş veya maskelenmemiş metinde) ya da bir `*/` sonrası.
5. `__has_*` ve `_Pragma` her yerde reddedilir.
6. Derleyici yorumları boşluğa çevirdiği için `#/**/include "yol"` (satır aşan `#/*…*/include`
   dahil) geçerli bir yönergedir: maskelenmiş metinde `#` ile yönerge adı arasında ham metinde
   `/*` varsa, hedef ne olursa olsun reddedilir (Faz A1, K1).
7. `#pragma` operandı **izin listesidir** (Faz H3): yalnızca `once`, `region`, `endregion`
   geçer. Gerekçe: pragma operandı makro olabilir (`#define X GCC dependency "…"` +
   `#pragma X`), derleyici makroyu açar ve host dosyası yoklanır; izin listesi bu yolu
   kapatır. Aynı nedenle `once`/`region`/`endregion` adlarını tanımlayan `#define` de
   reddedilir. `#line` yalnızca `#line <sayı>` biçiminde geçer (dosya adı yok): sahte tanı
   konumu üretemez.

Yanlış pozitif yalnızca Tier 1'in atlanmasına yol açar (`SKIPPED`); güvenli yönde hatadır.
"""

from __future__ import annotations

import re

from codementor.analysis.lexical import mask_non_code

_WS = r"[ \t\f\v]"
_TRIGRAPH = re.compile(r"\?\?[=/'()!<>\-]")
_SPLICE_TAIL = re.compile(r"\\[ \t\f\v]*$")
_PASTE = re.compile(r"##|%:%:")
_KEYWORD = re.compile(rf"(?:#|%:){_WS}*(include_next|include|import|embed|pragma|line)\b")
# Maskede yorumlar boşluk olduğundan `\s` satır aşan blok yorumunu da kapsar
_SPLIT_KEYWORD = re.compile(r"(?:#|%:)\s*(include_next|include|import|embed|pragma|line)\b")
_AFTER_COMMENT_END = re.compile(rf"\*/(?:{_WS}|/\*.*?\*/)*$")
_FORBIDDEN_TOKENS = re.compile(r"__has_\w*|\b_Pragma\b")
_DEPENDENCY = re.compile(r"\bdependency\b")
# İzin listesi (Faz H3): pragma operandı makro olabilir, bu yüzden yalnızca bilinen güvenli
# biçimler geçer; operand MASKELENMİŞ metinden okunur (yorumlar boşluk, metin sabitleri boş).
_PRAGMA_ALLOWED = re.compile(r"(?:once|region|endregion)\b")
_PRAGMA_RESERVED = frozenset({"once", "region", "endregion"})
_DEFINE_NAME = re.compile(rf"(?:#|%:){_WS}*define{_WS}+([A-Za-z_]\w*)")
_LINE_ONLY = re.compile(rf"[0-9]+{_WS}*$")
_DEVICE = re.compile(r"^(?:CON|PRN|AUX|NUL|CLOCK\$|CONIN\$|CONOUT\$|COM\d|LPT\d)$", re.IGNORECASE)
_INCLUDE_LIKE = frozenset({"include", "include_next", "import"})


def _logical_lines(code: str) -> list[tuple[int, str]]:
    """Satır birleştirilmiş mantıksal satırlar; her biri başladığı fiziksel satır no ile.

    gcc/clang gibi `\\` ile satır sonu arasındaki boşluklara izin verir.
    """
    result: list[tuple[int, str]] = []
    parts: list[str] = []
    start = 1
    for number, physical in enumerate(code.split("\n"), start=1):
        if not parts:
            start = number
        tail = _SPLICE_TAIL.search(physical)
        if tail:
            parts.append(physical[: tail.start()])
            continue
        parts.append(physical)
        result.append((start, "".join(parts)))
        parts = []
    if parts:
        result.append((start, "".join(parts)))
    return result


def _target(rest: str) -> str | None:
    """Yönerge adından sonraki metinden `"yol"` / `<yol>` hedefini çıkarır; yoksa None."""
    rest = rest.lstrip(" \t\f\v")
    if not rest or rest[0] not in '"<':
        return None
    close = rest.find('"' if rest[0] == '"' else ">", 1)
    if close < 0:
        return None
    return rest[1:close]


def _unsafe_path(path: str) -> str | None:
    if not path.strip():
        return "boş yol"
    if path.startswith(("/", "\\")):
        return "mutlak yol"
    if ":" in path:
        return "sürücü harfi veya `:`"
    if "\\" in path:
        return "ters eğik çizgi"
    if ".." in path:
        return "üst dizin (`..`)"
    name = path.rsplit("/", 1)[-1].split(".", 1)[0].strip()
    if _DEVICE.match(name):
        return "aygıt adı"
    return None


def _directive_position(raw: str, masked: str, index: int) -> bool:
    """`index`teki `#` derleyici için bir yönerge başı olabilir mi (fail-closed)."""
    before_raw, before_masked = raw[:index], masked[:index]
    return (
        not before_raw.strip(" \t\f\v")
        or (masked[index : index + 1] in ("#", "%") and not before_masked.strip(" \t\f\v"))
        or _AFTER_COMMENT_END.search(before_raw) is not None
    )


def _operand(text: str, index: int) -> str:
    """Yönerge adından sonraki operand metni (baştaki boşluklar atılır)."""
    return text[index:].lstrip(" \t\f\v")


def _check_line(line: int, raw: str, masked: str) -> list[str]:
    reasons: list[str] = []
    token = _FORBIDDEN_TOKENS.search(raw)
    if token:
        reasons.append(f"Satır {line}: `{token.group()}` kullanımı")
    defined = _DEFINE_NAME.search(masked)
    if defined is not None and defined.group(1) in _PRAGMA_RESERVED:
        # `#define once …` + `#pragma once`: operand makroya dönüşür, izin listesi atlatılır
        reasons.append(
            f"Satır {line}: izin listesindeki `{defined.group(1)}` adını tanımlayan `#define`"
        )
    for match in _KEYWORD.finditer(raw):
        name = match.group(1)
        if name == "embed":
            reasons.append(f"Satır {line}: `#embed` yönergesi")
        elif name == "pragma":
            if _DEPENDENCY.search(raw, match.end()):
                reasons.append(f"Satır {line}: `#pragma ... dependency` yönergesi")
            elif _directive_position(raw, masked, match.start()) and not _PRAGMA_ALLOWED.match(
                _operand(masked, match.end())
            ):
                reasons.append(
                    f"Satır {line}: izin verilmeyen `#pragma` (yalnızca `once`, `region`, "
                    "`endregion`)"
                )
        elif name == "line":
            # Yönerge konumu aranır: `#line` dosya okumaz, riski sahte tanı konumudur ve
            # yorum/metin içindeki geçiş yanlış pozitif üretmemeli (Faz H3).
            if _directive_position(raw, masked, match.start()) and not _LINE_ONLY.match(
                _operand(raw, match.end())
            ):
                reasons.append(f"Satır {line}: izin verilmeyen `#line` (yalnızca `#line <sayı>`)")
        else:
            target = _target(raw[match.end() :])
            if target is None:
                if _directive_position(raw, masked, match.start()):
                    reasons.append(f"Satır {line}: makroyla hesaplanan veya bozuk `#{name}`")
                continue
            problem = _unsafe_path(target)
            if problem:
                reasons.append(f"Satır {line}: `#{name}` içinde {problem}")
    return reasons


def check_includes(code: str) -> list[str]:
    """Güvenli olmayan önişlemci kullanımlarını bulur; boş liste = derleyici çağrılabilir."""
    reasons: list[str] = []
    for pattern, label in ((_TRIGRAPH, "trigraph dizisi"), (_PASTE, "token yapıştırma")):
        found = pattern.search(code)
        if found:
            line = code.count("\n", 0, found.start()) + 1
            reasons.append(f"Satır {line}: {label} (`{found.group()}`)")

    logical = _logical_lines(code)
    joined = "\n".join(text for _, text in logical)
    # Denetim (Faz A sonrası): `#\` + yeni satır + `#` satır birleştirmeden sonra `##` olur;
    # ham kodda görünmeyen yapıştırma işleci birleştirilmiş metinde aranır
    if not any("token yapıştırma" in r for r in reasons):
        pasted = _PASTE.search(joined)
        if pasted:
            line = logical[joined.count("\n", 0, pasted.start())][0]
            reasons.append(f"Satır {line}: token yapıştırma (satır birleştirmeyle `##`)")
    masked_joined = mask_non_code(joined)
    masked = masked_joined.split("\n")
    for (line, raw), plain in zip(logical, masked, strict=True):
        reasons += _check_line(line, raw, plain)
    reasons += _comment_split_directives(joined, masked_joined, logical)
    return reasons


def _comment_split_directives(
    joined: str, masked: str, logical: list[tuple[int, str]]
) -> list[str]:
    """`#/**/include` gibi `#` ile yönerge adı arasına yorum giren yönergeler (fail-closed)."""
    reasons: list[str] = []
    for match in _SPLIT_KEYWORD.finditer(masked):
        if "/*" not in joined[match.start() : match.start(1)]:
            continue
        line = logical[masked.count("\n", 0, match.start())][0]
        reasons.append(f"Satır {line}: yorumla bölünmüş `#{match.group(1)}` yönergesi")
    return reasons
