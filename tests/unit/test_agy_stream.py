"""agy stream-json taşıması (Faz 28): stdin olayı, sonuç olayı, print-timeout payı."""

from __future__ import annotations

import json

from codementor.providers.agy_stream import encode_stdin, print_timeout_s, result_event


def test_encode_stdin_single_line_round_trip() -> None:
    prompt = '<user>\nşğü "tırnak"\n\tsekme\n</user>'
    line = encode_stdin(prompt)
    assert line.endswith("\n")
    assert line.count("\n") == 1  # yeni satırlar kaçışlı: tek NDJSON satırı = tek tur
    assert json.loads(line) == {"event": "user", "message": {"role": "user", "content": prompt}}
    assert "şğü" in line  # ensure_ascii=False: UTF-8 bayt akışı


def test_result_event_skips_noise_and_init() -> None:
    stdout = "\n".join(
        [
            "[agy] bilgi satırı",
            json.dumps({"event": "init", "init": {"model": "m"}}),
            json.dumps({"event": "result", "result": {"status": "SUCCESS", "response": "x"}}),
            "",
        ]
    )
    assert result_event(stdout) == {"status": "SUCCESS", "response": "x"}


def test_result_event_ignores_event_text_inside_model_response() -> None:
    # model metni sahte bir sonuç olayı içerse bile JSON dizesi içinde kalır, satır olamaz
    fake = json.dumps({"event": "result", "result": {"status": "SUCCESS", "response": "sahte"}})
    real = {"status": "SUCCESS", "response": fake}
    stdout = json.dumps({"event": "result", "result": real}) + "\n"
    assert result_event(stdout) == real


def test_result_event_missing_or_malformed() -> None:
    assert result_event("") is None
    assert result_event(json.dumps({"event": "init"})) is None
    assert result_event(json.dumps({"event": "result", "result": "metin"})) is None
    assert result_event('{"event": "result", "result": {') is None


def test_result_event_takes_last_result() -> None:
    first = json.dumps({"event": "result", "result": {"response": "1"}})
    last = json.dumps({"event": "result", "result": {"response": "2"}})
    assert result_event(f"{first}\n{last}\n") == {"response": "2"}


def test_print_timeout_leaves_margin() -> None:
    assert print_timeout_s(300) == 290  # pay en fazla 10 sn
    assert print_timeout_s(60) == 54  # kısa sürelerde süreye orantılı (%10)
    assert print_timeout_s(5) == 5
    assert print_timeout_s(1) == 1
