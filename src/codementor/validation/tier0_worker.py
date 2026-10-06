"""Tier 0 alt süreç işçisi (Faz 59, ADR-0025): `python -m codementor.validation.tier0_worker`.

stdin'den `NormalizedCode` JSON'u okur, `run_tier0` sonucunu (`Tier0Result` JSON) stdout'a
yazar. Ağaç süreçler arasında taşınamadığı için yalnız tanılar döner. Süre sınırı ve süreç
ağacının öldürülmesi çağıranın (`tier0_isolation`, `runner.run_process`) işidir.
"""

from __future__ import annotations

import sys

from codementor.models.request import NormalizedCode
from codementor.validation.tier0 import run_tier0


def main() -> int:
    """İşçi giriş noktası; çıkış kodu 0 başarı.

    Akışlar bayt olarak UTF-8 okunur/yazılır: Windows'ta borunun metin kodlaması yerel kod
    sayfasıdır ve Türkçe tanılar bozulurdu (`runner` UTF-8 gönderir ve çözer).
    """
    code = NormalizedCode.model_validate_json(sys.stdin.buffer.read().decode("utf-8"))
    sys.stdout.buffer.write(run_tier0(code).model_dump_json().encode("utf-8"))
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":  # pragma: no cover - alt süreçte koşar
    raise SystemExit(main())
