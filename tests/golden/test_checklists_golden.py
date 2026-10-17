"""Kontrol listesi içerik anlık görüntüsü (Faz J): `data/checklists/*.yaml` sha256 özetleri.

Amaç: kontrol listesi içeriği **bilinçsizce** değişirse (yanlışlıkla düzenleme, satır kaybı,
kodlama bozulması, dosya ekleme/silme) test düşsün ve değişiklik `git diff` ile gözden geçirilsin.
Bu dosyalar prompt'a girer (mimari §8.3) ve ölçümü etkiler; sessiz değişim istenmez.

Beklenenleri bilinçli bir değişiklikten sonra güncellemek:
`uv run pytest tests/golden/test_checklists_golden.py --update-golden`

Yazma tarafı LF'e sabitlenir (`newline` açıkça verilir): Windows'ta `--update-golden`
çalıştırıldığında golden dosya CRLF baytlarıyla boşuna kirlenmesin (denetim Küçük-1).

Özet ham baytlardan hesaplanır; `.gitattributes` tüm metin dosyalarını LF'e sabitlediği için
platformlar arası fark oluşmaz (`\\r\\n` yine de `\\n`'e normalleştirilir: farklı çalışma kopyası
ayarları testi bozmasın).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

from codementor.questions._loader import DataFileError, list_yaml_files

DATA = Path(__file__).resolve().parents[2] / "data" / "checklists"
GOLDEN = Path(__file__).parent / "checklists_sha256.json"


def checklist_files(directory: Path) -> list[Path]:
    """Yükleyicinin okuduğu dosyalar (aynı yardımcı: yükleyici değişirse küme de değişir).

    Denetim Küçük-2: ölçüt burada kopyalanmaz, `_loader.list_yaml_files` çağrılır; böylece
    yükleyicinin listeleme kuralı değişirse anlık görüntü sessizce ayrışmaz (aynı sıralama +
    dizin yoksa anlaşılır hata).
    """
    return list_yaml_files(directory, DataFileError)


def digests(directory: Path) -> dict[str, str]:
    """Dosya adı → içerik sha256 özeti (LF normalleştirilmiş baytlar)."""
    return {
        path.name: hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        for path in checklist_files(directory)
    }


def write_golden(path: Path, data: dict[str, str]) -> None:
    """Kararlı biçimde yazar (anahtar sırası sabit, girinti 2, UTF-8/LF, sonda satır sonu)."""
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def test_checklists_content_snapshot(update_golden: bool) -> None:
    """Dizindeki içerik özetleri sabitlenmiş değerlerle aynı olmalı (Faz J)."""
    actual = digests(DATA)
    if update_golden:
        write_golden(GOLDEN, actual)
        return
    assert GOLDEN.is_file(), f"{GOLDEN.name} yok: uv run pytest tests/golden --update-golden"
    expected: dict[str, str] = json.loads(GOLDEN.read_text(encoding="utf-8"))
    changed = sorted(
        name for name in actual.keys() | expected.keys() if actual.get(name) != expected.get(name)
    )
    assert not changed, (
        "Kontrol listesi içeriği değişti: "
        + ", ".join(changed)
        + ". Değişiklik bilinçliyse gözden geçirip `uv run pytest "
        "tests/golden/test_checklists_golden.py --update-golden` ile sabitleyin."
    )


def test_golden_covers_exactly_the_loaded_files() -> None:
    """Anlık görüntü dosya kümesi dizinle birebir: eklenen/silinen dosya sessiz kalmaz."""
    assert GOLDEN.is_file(), f"{GOLDEN.name} yok: uv run pytest tests/golden --update-golden"
    expected: dict[str, str] = json.loads(GOLDEN.read_text(encoding="utf-8"))
    expected_files = set(expected)
    actual_files = {path.name for path in checklist_files(DATA)}
    missing = sorted(expected_files - actual_files)
    extra = sorted(actual_files - expected_files)
    assert expected_files == actual_files, (
        f"Anlık görüntü dosya kümesi uyuşmuyor (özet eksik: {missing}, özet fazla: {extra})."
    )


def test_digest_changes_with_content(tmp_path: Path) -> None:
    """Özet gerçekten içeriği izliyor: değişim algılanır (test kendini kanıtlar)."""
    target = tmp_path / "c.yaml"
    target.write_text("version: 1\n", encoding="utf-8")
    before = digests(tmp_path)
    target.write_text("version: 2\n", encoding="utf-8")
    assert digests(tmp_path) != before
    assert set(before) == {"c.yaml"}


def test_digest_ignores_line_endings(tmp_path: Path) -> None:
    """CRLF/LF farkı özeti değiştirmez (platformlar arası kararlılık)."""
    (tmp_path / "a.yaml").write_bytes(b"version: 1\nx: 2\n")
    (tmp_path / "b.yaml").write_bytes(b"version: 1\r\nx: 2\r\n")
    assert digests(tmp_path)["a.yaml"] == digests(tmp_path)["b.yaml"]


def test_write_golden_round_trip(tmp_path: Path) -> None:
    data = {"c.yaml": "0" * 64}
    target = tmp_path / "checklists_sha256.json"
    write_golden(target, data)
    text = target.read_text(encoding="utf-8")
    assert json.loads(text) == data
    assert text.endswith("}\n")


def test_write_golden_writes_lf_bytes(tmp_path: Path) -> None:
    """Diskte LF olmalı (denetim Küçük-1): `write_text` varsayılanı Windows'ta `os.linesep`'tir.

    CRLF yazılırsa `--update-golden` ağacı içerik değişmeden kirletir; okuma tarafı CRLF'i
    gizlediği için bu iddia `read_bytes()` üzerinden yapılır.
    """
    target = tmp_path / "checklists_sha256.json"
    write_golden(target, {"c.yaml": "0" * 64})
    raw = target.read_bytes()
    assert b"\r" not in raw
    assert raw.endswith(b"}\n")


def test_snapshot_detects_content_change_and_file_set_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Negatif yol süite içinde (denetim Küçük-4): değişen içerik ve dosya kümesi düşürür.

    Gerçek `data/checklists` ellenmez; modül sabitleri geçici dizine yönlendirilir.
    """
    module = sys.modules[__name__]
    (tmp_path / "a.yaml").write_text("version: 1\n", encoding="utf-8")
    golden = tmp_path / "checklists_sha256.json"
    monkeypatch.setattr(module, "DATA", tmp_path)
    monkeypatch.setattr(module, "GOLDEN", golden)
    write_golden(golden, digests(tmp_path))

    test_checklists_content_snapshot(update_golden=False)
    test_golden_covers_exactly_the_loaded_files()

    (tmp_path / "a.yaml").write_text("version: 2\n", encoding="utf-8")
    with pytest.raises(AssertionError) as content_error:
        test_checklists_content_snapshot(update_golden=False)
    assert "a.yaml" in str(content_error.value)

    (tmp_path / "b.yaml").write_text("version: 3\n", encoding="utf-8")
    with pytest.raises(AssertionError) as set_error:
        test_golden_covers_exactly_the_loaded_files()
    assert "b.yaml" in str(set_error.value)


def test_missing_golden_fails_with_actionable_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Golden yoksa mesaj güncelleme komutunu içermeli (denetim Küçük-4)."""
    module = sys.modules[__name__]
    (tmp_path / "a.yaml").write_text("version: 1\n", encoding="utf-8")
    monkeypatch.setattr(module, "DATA", tmp_path)
    monkeypatch.setattr(module, "GOLDEN", tmp_path / "yok.json")
    with pytest.raises(AssertionError, match="--update-golden"):
        test_checklists_content_snapshot(update_golden=False)
    with pytest.raises(AssertionError, match="--update-golden"):
        test_golden_covers_exactly_the_loaded_files()
