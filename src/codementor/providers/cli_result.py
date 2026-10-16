"""CLI ajanı yanıtlarının ayrıştırılması ve hata sınıflandırması (Faz G bölmesi).

`cli_agent.py` (Claude/agy) 400 satır sınırını aştığı için sonuç ayrıştırma (`_json_document`,
`_object_spans`, `_served_model`, `_mapping`) ve kimlik hatası sınıflandırması (`auth_error`)
buraya taşındı; davranış değişmedi. `cli_agent` bu adları eskisi gibi yeniden dışa aktarır
(G0'da `passes.py` için kullanılan kalıp), dış modüller ve testler etkilenmez.

Bu modül yalnız **CLI'nin kendi JSON çıktısını** çözer; şema uyumu ayrı katmanda doğrulanır ve
alt süreç garantisi verilmez (`ProviderResult.schema_enforced = False`, G7).
"""

from __future__ import annotations

import json
from typing import Any

from codementor.providers._common import as_int
from codementor.providers.base import ProviderConfigError, ProviderError

# G2 (O6): oturum/kimlik hataları kalıcıdır; yeniden denemek boşuna, kullanıcı giriş yapmalı
# (`codex_cli._classify` ile aynı sözleşme: `ProviderConfigError.retryable = False`).
_AUTH_HINTS: tuple[str, ...] = (
    "not logged in",
    "please run /login",
    "claude login",
    "unauthorized",
    "authentication",
    "invalid api key",
    "oturum açıl",
    "giriş yap",
)


def auth_error(provider: str, detail: str, command: str) -> ProviderError | None:
    """Ayrıntı oturum/kimlik sorununa işaret ediyorsa yeniden denenmeyen hata (G2)."""
    lowered = detail.lower()
    if not any(hint in lowered for hint in _AUTH_HINTS):
        return None
    return ProviderConfigError(provider, f"oturum açılmamış; terminalde `{command}` çalıştırın")


def _json_document(stdout: str, marker: str) -> dict[str, Any] | None:
    """Çıktının sonundaki, `marker` alanını taşıyan JSON belgesi. Önünde bilgi satırları ya da
    model metni olabilir; sahte bir satır yerine CLI'nin kendi sonuç nesnesi seçilir.

    D12: adaylar tek geçişte yığınla çıkarılır ve yalnız kapanışı metnin sonuna kadar boşluk
    kalan aday ayrıştırılır. Aksi hâlde her `{` konumundan yeniden ayrıştırma karesel sürüyordu.
    """
    decoder = json.JSONDecoder()
    text = stdout.strip()
    end_of_text = len(text.rstrip())
    for start, end in reversed(_object_spans(text)):
        if end != end_of_text:
            continue
        try:
            data, parsed_end = decoder.raw_decode(text, start)
        except (ValueError, RecursionError):
            continue
        if isinstance(data, dict) and marker in data and not text[parsed_end:].strip():
            return data
    return None


def _object_spans(text: str) -> list[tuple[int, int]]:
    """Eşleşen `{...}` blokları (en içteki önce), tek geçişte; tırnak içindeki ayraçlar
    sayılmaz ve eşsiz `}` yok sayılır. Kapanmayan ayraç (önündeki düz yazıda bir `{`) önceki
    adayların eşleşmesini bozmaz."""
    spans: list[tuple[int, int]] = []
    stack: list[int] = []
    in_string = escaped = False
    for i, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        elif stack and ch == '"':
            in_string = True
        elif ch == "{":
            stack.append(i)
        elif ch == "}" and stack:
            spans.append((stack.pop(), i + 1))
    return spans


def _served_model(served: object, requested: str) -> str:
    """`modelUsage` birden çok model içerebilir (arka plan işleri); isteneni ya da en çok
    çıktı üreteni seçer."""
    if not isinstance(served, dict) or not served:
        return requested
    if requested in served:
        return requested

    def output(name: str) -> int:
        stats = served.get(name)
        return as_int(stats.get("outputTokens")) if isinstance(stats, dict) else 0

    return str(max(served, key=output))


def _mapping(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
