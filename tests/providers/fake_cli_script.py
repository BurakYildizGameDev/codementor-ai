"""Sahte `claude`/`agy` (Faz 25): gerçek `run_process` ile başlatılır, gördüklerini yanıtlar.

Yanıtın yapılandırılmış çıktısı; argv, çalışma dizini, ortam adları ve stdin'i taşır. stdin'de
`UYU:<yol>` varsa yola işaret dosyası yazar ve uzun süre uyur (iptal testi).
"""

import json
import os
import re
import sys
import time


def main() -> None:
    stdin = sys.stdin.read()
    sleeper = re.search(r"UYU:(\S+)", stdin)
    if sleeper:
        with open(sleeper.group(1), "w", encoding="utf-8") as marker:
            marker.write(str(os.getpid()))
        time.sleep(60)
    probe = {
        "argv": sys.argv[1:],
        "cwd": os.getcwd(),
        "cwd_entries": sorted(os.listdir(".")),
        "env_keys": sorted(os.environ),
        "stdin": stdin,
    }
    usage = {"input_tokens": 11, "output_tokens": 7}
    if "--sandbox" in sys.argv:  # agy
        reply = {"status": "SUCCESS", "response": json.dumps(probe), "usage": usage}
    else:
        reply = {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "result": "",
            "structured_output": probe,
            "usage": usage,
        }
    print("bilgi: sahte CLI başladı")  # önündeki gürültü satırı ayrıştırmayı bozmamalı
    print(json.dumps(reply))


if __name__ == "__main__":
    main()
