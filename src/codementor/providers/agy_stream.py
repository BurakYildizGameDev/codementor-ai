"""agy (Antigravity CLI) stream-json taşıması (Faz 28).

agy 1.2.14'te `-p` prompt'u **değer** olarak alır; prompt argv'ye konamaz (mimari §12), bu yüzden
`--input-format stream-json` ile stdin'den verilir. Biçim canlı yoklamayla doğrulandı:

- girdi: satır başına bir NDJSON mesajı, her satır bir tur:
  `{"event": "user", "message": {"role": "user", "content": "..."}}`;
- çıktı: `{"event": "init", ...}` … ve son olarak `{"event": "result", "result": {status, response,
  error?, num_turns, usage}}`.
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


def print_timeout_s(timeout_s: int) -> int:
    """agy'nin `--print-timeout`'u: kısmi sonucunu bizim süreç zaman aşımımızdan önce yazsın."""
    return max(1, timeout_s - min(_MAX_MARGIN_S, timeout_s // 10))
