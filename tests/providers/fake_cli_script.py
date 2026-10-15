"""Sahte `claude`/`agy`/`codex` (Faz 25, 28): gerçek `run_process` ile başlatılır, yanıtlar.

Yanıtın yapılandırılmış çıktısı; argv, çalışma dizini, ortam adları ve stdin'i taşır. stdin'de
`UYU:<yol>` varsa yola işaret dosyası yazar ve uzun süre uyur (iptal testi); `BOYUT:<n>` varsa
ayrıştırıcıyı bozmayan n bayt gürültü yazar (çıktı sınırı testi, G1).
"""

import json
import os
import re
import sys
import time


def noise(total: int) -> bytes:
    """`bilgi:` önekli gürültü satırları: JSONL/JSON ayrıştırmasını bozmaz (G1)."""
    if total <= 0:
        return b""
    line = b"bilgi: " + b"x" * 800 + b"\n"
    return line * max(1, total // len(line))


def main() -> None:
    # Gerçek CLI'lar gibi UTF-8 bayt düzeyinde; temizlenmiş ortamda konsol kodlaması cp1252
    # olabilir (Windows CI), Türkçe karakter metin akışında çökerdi
    stdin = sys.stdin.buffer.read().decode("utf-8")
    sleeper = re.search(r"UYU:(\S+)", stdin)
    if sleeper:
        with open(sleeper.group(1), "w", encoding="utf-8") as marker:
            marker.write(str(os.getpid()))
        time.sleep(60)
    sized = re.search(r"BOYUT:(\d+)", stdin)
    filler = noise(int(sized.group(1))) if sized else b""
    probe = {
        "argv": sys.argv[1:],
        "cwd": os.getcwd(),
        "cwd_entries": sorted(os.listdir(".")),
        "env_keys": sorted(os.environ),
        "stdin": stdin,
    }
    usage = {"input_tokens": 11, "output_tokens": 7}
    out = sys.stdout.buffer
    if "exec" in sys.argv:  # codex: JSONL olay akışı, şema dosyası çağrı sırasında var olmalı
        schema = sys.argv[sys.argv.index("--output-schema") + 1]
        probe["schema_exists"] = os.path.isfile(schema)
        events = [
            {"type": "thread.started", "thread_id": "t"},
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": json.dumps(probe)},
            },
            {"type": "turn.completed", "usage": usage},
        ]
        parts = [json.dumps(e, ensure_ascii=False).encode() + b"\n" for e in events]
        if filler:  # yanıttan SONRA: kesilse bile agent_message ayakta kalır (G1)
            parts.insert(2, filler)
        out.write(b"".join(parts))
        out.flush()
        return
    if "--sandbox" in sys.argv:  # agy: NDJSON `user` olayı girer, `init` + `result` olayları çıkar
        try:
            probe["content"] = json.loads(stdin)["message"]["content"]
            result = {"status": "SUCCESS", "response": json.dumps(probe), "usage": usage}
        except (ValueError, KeyError, TypeError) as exc:
            result = {"status": "ERROR", "response": "", "error": f"stream input: {exc}"}
        events = [{"event": "init", "init": {}}, {"event": "result", "result": result}]
        out.write("bilgi: sahte agy başladı\n".encode())  # gürültü satırı ayrıştırmayı bozmamalı
        out.write(filler)
        out.write("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in events).encode())
        out.flush()
        return
    reply = {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "result": "",
        "structured_output": probe,
        "usage": usage,
    }
    out.write("bilgi: sahte CLI başladı\n".encode())  # gürültü satırı ayrıştırmayı bozmamalı
    out.write(filler)  # sonuç nesnesinden ÖNCE: kesilme hâlinde JSON kaybolur (G1)
    out.write((json.dumps(reply, ensure_ascii=False) + "\n").encode())
    out.flush()


if __name__ == "__main__":
    main()
