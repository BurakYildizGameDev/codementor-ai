"""agy (Antigravity CLI) stream-json taşıması (Faz 28).

agy 1.2.14'te `-p` prompt'u **değer** olarak alır; prompt argv'ye konamaz (mimari §12), bu yüzden
`--input-format stream-json` ile stdin'den verilir. Biçim canlı yoklamayla doğrulandı:

- girdi: satır başına bir NDJSON mesajı, her satır bir tur:
  `{"event": "user", "message": {"role": "user", "content": "..."}}`;
- çıktı: `{"event": "init", ...}` … ve son olarak `{"event": "result", "result": {status, response,
  error?, num_turns, usage}}`.

agy 1.3.1 (Faz 63, canlı gözlem): `result` içinde `structured_output` da gelir; agy yanıttan sonra
kendiliğinden ikinci bir tur açıp `response` metnine araç izi (`{"toolAction": ...}`) ekleyebilir.
Bu yüzden metinden **ilk** JSON nesnesi alınır; metin boşsa ilk yanıt adımının `text_delta`
parçaları birleştirilir.
"""

from __future__ import annotations

import json
from typing import Any

_MAX_MARGIN_S = 10


def encode_stdin(prompt: str) -> str:
    """Tüm prompt'u tek bir `user` olayına koyar (yeni satırlar kaçışlı: tek tur)."""
    event = {"event": "user", "message": {"role": "user", "content": prompt}}
    return json.dumps(event, ensure_ascii=False) + "\n"


def result_event(stdout: str) -> dict[str, Any] | None:
    """Son `result` olayının `result` nesnesi; yoksa None. Model metni JSON dizesi içinde
    kaldığından satır düzeyinde ayrıştırma sahte olaylara kanmaz."""
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
        except (ValueError, RecursionError):
            continue
        if isinstance(data, dict) and data.get("event") == "result":
            result = data.get("result")
            return result if isinstance(result, dict) else None
    return None


def _events(stdout: str) -> list[dict[str, Any]]:
    """JSON olay satırları (sırasıyla); JSON olmayan satırlar atlanır."""
    events: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
        except (ValueError, RecursionError):
            continue
        if isinstance(data, dict):
            events.append(data)
    return events


def _top_level_braces(text: str) -> list[int]:
    """Dış düzeydeki `{` konumları (dize içindeki ayraçlar sayılmaz)."""
    starts: list[int] = []
    depth = 0
    in_string = escaped = False
    for i, ch in enumerate(text):
        if depth and in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        elif depth and ch == '"':
            in_string = True
        elif ch == "{":
            if depth == 0:
                starts.append(i)
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
    return starts


def first_json_object(text: str) -> dict[str, Any] | None:
    """Metindeki ilk dış düzey JSON nesnesi (çit, önündeki metin ve arkadaki araç izi atlanır).

    Çözülemeyen (ör. yarım kalan) bir nesnenin **içine** girilmez: iç içe bir parça yanıt
    sayılmasın (denetim O1).
    """
    decoder = json.JSONDecoder()
    for index in _top_level_braces(text):
        try:
            value, _end = decoder.raw_decode(text, index)
        except (ValueError, RecursionError):
            continue
        if isinstance(value, dict):
            return value
    return None


def first_response_text(stdout: str) -> str:
    """İlk `agent_response` adımının `text_delta` parçaları; sonraki turlar (araç izi) katılmaz."""
    parts: list[str] = []
    first_step: object = None
    for event in _events(stdout):
        update = event.get("step_update")
        if event.get("event") != "step_update" or not isinstance(update, dict):
            continue
        if update.get("step_type") != "agent_response":
            continue
        step = update.get("step_index")
        if first_step is None:
            first_step = step
        if step != first_step:
            break
        delta = update.get("text_delta")
        if isinstance(delta, str):
            parts.append(delta)
    return "".join(parts)


def print_timeout_s(timeout_s: int) -> int:
    """agy'nin `--print-timeout`'u: kısmi sonucunu bizim süreç zaman aşımımızdan önce yazsın."""
    return max(1, timeout_s - min(_MAX_MARGIN_S, timeout_s // 10))
