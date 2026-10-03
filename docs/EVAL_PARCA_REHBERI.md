# Faz 36 canlı dev ölçümü: parça 3/4 ve 4/4 rehberi (Codex için)

Bu belge, Faz 36 (hata/öneri ayrımı, ADR-0022) canlı dev ölçümünün kalan iki parçasını
koşturacak ve sonuçlarını işleyecek ajan (Codex) içindir. Ajan bulduğu sorunları bu belgenin
sonundaki **"Bulunan sorunlar"** bölümüne yazar ve aşağıdaki kurallar içinde düzeltir.
**Amaç ölçmek ve kayıt tutmaktır; motoru ölçüme göre ayarlamak değil.**

---

## 1. Durum (2026-10-04)

- Dal: `faz/36-hata-oneri` (main'e birleştirilmedi, push edilmedi). Çalışmaya bu daldan devam et.
- Dev bölümü 96 örnek. `eval run --part k/4` onu 4 dengeli parçaya böler (`src/codementor/eval/parts.py`;
  her parça 24 örnek, dil/motor ve örnek türü orantılı, bölme belirleyici).
- Koşulan parçalar (Opus 5.5, `claude_cli`, two_pass, doğrulama açık; prompt `v1+7205d091`):

| Parça | Sonuç dosyası | P / R / F1 (yalnız hatalar) | Öneri |
|---|---|---|---|
| 1/4 | `eval/results/20261003T215350_claude_cli_claude-opus-5-5_two_pass_part1-4_dev.json` | 71 / 77 / 74 | 9 |
| 2/4 | `eval/results/20261003T220533_claude_cli_claude-opus-5-5_two_pass_part2-4_dev.json` | 78 / 90 / 84 | 5 |
| 1 + 2 | — | 75 / 83 / 78 (güncel etiketle 75 / 81 / 78) | 14 |

- Ayrıntı ve yorum: `docs/eval-findings.md` §11, `PROGRESS.md` "Faz 36 — Notlar" → "Canlı ölçüm planı".
- Karşılaştırma tabanı: Faz 35B Opus + doğrulama koşusu
  `eval/results/20261003T192757_claude_cli_claude-opus-5-5_two_pass_verify_dev.json` (eski 46 örnek, P/R/F1 79/89/84).

---

## 2. Değiştirilmeyecekler (ölçüm sürerken)

Parça 1 ve 2 ile karşılaştırılabilir kalmak için **parça 3 ve 4 bitene kadar** şunlara dokunma:

1. `prompts/v1/**` (şablonlar, few-shot'lar): `prompt_version` değişir, parçalar birleştirilemez.
2. `src/codementor/` altında analiz davranışını değiştiren kod (kurallar, `analysis/`, `verify/`,
   `pipeline/`, `providers/`), `codementor.toml` ve `data/`.
3. `eval/dataset/test/**`: test bölümü kapalıdır; okuma, koşma, değiştirme.
4. Sağlayıcı ve model: parçalar `claude_cli` + `claude-opus-5-5` ile koşulur. Codex'in kendi
   modeli (`codex_cli`) ile koşma; o ayrı bir ölçümdür.
5. Etiketleri modelin yanıtına göre değiştirme. Etiket yalnız **kodun gerçeğine** göre düzeltilir
   (bkz. §5.2).

---

## 3. Koşu

Proje kökünde, Git Bash ya da PowerShell'de. Her parça ~24 örnek, ~10-15 dk, ~0,3M token.

```bash
uv sync
# Windows: Türkçe çıktı için
export PYTHONIOENCODING=utf-8          # PowerShell: $env:PYTHONIOENCODING="utf-8"
claude --version                        # claude_cli oturumu açık olmalı

uv run codementor eval run --split dev --provider claude_cli --mode two_pass --part 3/4
uv run codementor eval run --split dev --provider claude_cli --mode two_pass --part 4/4
```

- Koşu sırasında bilgisayar uykuya geçerse süreler bozulur (Faz 12'de oldu). Uzun koşuyu uyku
  engelleyerek başlat. Örnek (Windows, `awake.py` adıyla geçici bir dizine kaydet, depoya ekleme):

  ```python
  import ctypes, subprocess, sys

  ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
  try:
      sys.exit(subprocess.call(sys.argv[1:]))
  finally:
      ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
  ```

  `python awake.py uv run codementor eval run ... --part 3/4`
- Kota (429) ya da oturum hatası olursa koşuyu yarıda bırakma; sonuç dosyası yazılmazsa parçayı
  baştan koş. Örnek bazında `hata` görünürse dosya yine yazılır; hatayı §6'ya not et.
- Her koşu `eval/results/*_part3-4_dev.json` ve `*_part4-4_dev.json` dosyasını yazar.

---

## 4. Analiz

### 4.1 Parça başına

```bash
uv run codementor eval analyze eval/results/<parça dosyası>.json --out <geçici>/part3.md
uv run codementor eval breakdown eval/results/<parça dosyası>.json
```

`eval analyze` çıktısındaki FP/FN listelerine bak. Her FP/FN için şu sorulardan birine cevap
ver ve §6'ya yaz: model mi yanılıyor, etiket mi yanlış, kategori mi karışmış, doğrulama geçişi mi
düşürmüş (rapordaki `meta.warnings` içinde "kanıtlayamadı; bulgu atıldı")?

### 4.2 Dört parçanın birleşimi ve öneriler

Aşağıdaki betik, güncel etiketlerle dört parçayı birleştirir, önerileri etiketlerle karşılaştırır
ve Faz 35B ile ortak örnekleri kıyaslar. Geçici bir dosyaya kaydedip `uv run python <dosya>` ile koş.

```python
from pathlib import Path

from codementor.eval.compare import load_results
from codementor.eval.dataset import load_split
from codementor.eval.metrics import audit_metrics, match_findings
from codementor.models.findings import issues_only

labels = {s.label.id: s.label for s in load_split(Path("eval/dataset"), "dev")}
parts = load_results(sorted(Path("eval/results").glob("*_two_pass_part*-4_dev.json")))
old = load_results(
    [Path("eval/results/20261003T192757_claude_cli_claude-opus-5-5_two_pass_verify_dev.json")]
)[0]
samples = [s for r in parts for s in r.samples]
assert len(parts) == 4 and len({s.id for s in samples}) == 96, "dört parça da koşulmalı"


def score(items):
    a = audit_metrics([(labels[s.id], s) for s in items])
    return [round(x * 100) if x is not None else None for x in (a.precision, a.recall, a.f1)]


print("96 örnek P/R/F1:", score(samples))
print("öneri toplamı:", sum(r.metrics.suggestions_total or 0 for r in parts))
common = {s.id for s in old.samples} & {s.id for s in samples}
print(
    "Faz 35B ile ortak",
    len(common),
    "örnek:",
    "eski",
    score([s for s in old.samples if s.id in common]),
    "yeni",
    score([s for s in samples if s.id in common]),
)
for s in samples:  # öneriye düşmüş gerçek hata var mı?
    if s.report is None:
        continue
    suggestions = [f for f in s.report.findings if f.kind == "suggestion"]
    hits = match_findings(labels[s.id].expected.findings, suggestions)
    if hits:
        print("ÖNERİ ↔ ETİKETLİ HATA:", s.id, [(e.category.value, e.line) for e, _ in hits])
```

Not: Sonuç dosyalarındaki kayıtlı metrikler koşu anındaki etiketle hesaplanır; betik güncel
etiketi kullanır. İkisi farklıysa ikisini de yaz (parça 2'de `unity-104` düzeltmesi böyle).

---

## 5. Kayıt ve düzeltme

### 5.1 Her zaman yapılacaklar

1. **README dev tablosu** sonuç dosyalarından üretilir, elle yazılmaz. Yeni parça dosyaları
   eklenince tabloyu yeniden üret (yoksa `tests/unit/eval/test_readme_table.py` düşer):

   ```python
   import re
   from pathlib import Path
   from codementor.eval.compare import compare_table, load_results

   res = [
       r
       for r in load_results(sorted(Path("eval/results").glob("*_dev.json")))
       if not r.config.languages or set(r.config.languages) == {"c", "cpp", "csharp"}
   ]
   table = compare_table(res).strip()
   p = Path("README.md")
   text = p.read_text(encoding="utf-8")
   text = re.sub(
       r"(<!-- eval-table:dev:start -->\n).*?(\n<!-- eval-table:dev:end -->)",
       lambda m: m[1] + table + m[2],
       text,
       flags=re.S,
   )
   p.write_text(text, encoding="utf-8", newline="\n")
   ```

   README'deki "Faz 36 (2026-10-04)" notunu dört parçayı ve birleşik sonucu anlatacak şekilde
   güncelle.
2. `docs/eval-findings.md` §11'e "Parça 3/4", "Parça 4/4" ve "Dört parça (96 örnek)" alt
   başlıkları: P/R/F1, öneri sayısı, önerilerin etiketlerle çakışması, Faz 35B ile ortak
   örneklerde kıyas, FP/FN'lerin nedene göre dağılımı (model / etiket / kategori / doğrulama).
3. `PROGRESS.md` "Faz 36 — Notlar" → "Canlı ölçüm planı" kutularını `[x]` yap ve sonucu bir satırla yaz.
4. Sonuçta Faz 36 için bir karar cümlesi: precision arttı mı, recall düştü mü ("kaçırma oranı
   düşmez" hedefi), öneriler gerçek hataları yutuyor mu? Rakamla, abartmadan.

### 5.2 Düzeltilebilecekler (ölçüm bittikten sonra, ayrı commit'lerle)

| Tür | Ne zaman | Nasıl |
|---|---|---|
| Etiket hatası | Kod incelendiğinde etiket kodun gerçeğiyle çelişiyorsa (ör. "temiz" örnekte gerçek hata) | `docs/EVAL_ORNEK_REHBERI.md` §3 ölçütü ve kategori tanımı; modelin kategorisine göre değil. Etiket yorum satırına tarih ve neden. §6'ya önce/sonra puanı |
| Belge / tablo tutarsızlığı | README, eval-findings, PROGRESS birbirini tutmuyorsa | Düzelt |
| Ölçüm aracı hatası | `eval` komutları yanlış sayıyorsa | Test yaz, düzelt (`tests/unit/eval/`) |
| Motor davranışı (prompt, kural, doğrulama) | **Yalnız** dört parça bitip kaydedildikten sonra ve sorun §6'da kanıtıyla yazılıysa | `docs/UYGULAMA_PLANI.md`'de karşılığı olan faz varsa (Faz 39-41) o fazın kapsamında; `prompt_version` değişirse eski sonuçlarla karşılaştırılamayacağını not et |

Etiket düzeltmek dışında bir şey düzelttiysen değişikliği küçük tut ve ilgisiz kodu
yeniden düzenleme.

### 5.3 Her değişiklikten sonra denetim

Windows'ta `make` yok; ayrı ayrı:

```bash
uv run ruff check .
uv run ruff format --check .      # .md içindeki python bloklarını da biçimler
uv run mypy --strict src/
uv run pytest -m "not live"
# web'e dokunduysan: cd web && npm run typecheck && npm test
```

Hepsi yeşil değilse commit atma.

### 5.4 Commit

- Dal: `faz/36-hata-oneri`. Mesajlar Türkçe, örnek: `eval(faz-36): canlı dev parça 3/4 (P/R/F1 ../../..)`.
- Commit mesajına yapay zekâ atfı satırı (Co-Authored-By vb.) ekleme.
- Push etme, main'e birleştirme: kullanıcı karar verir.

---

## 6. Bulunan sorunlar

Ajan burayı doldurur. Her sorun için bir satır; çözdüysen "Durum" sütununa commit kısa kimliğini yaz.

| # | Örnek / dosya | Sorun | Kanıt (satır, rapor alıntısı) | Tür (model / etiket / kategori / doğrulama / araç / belge) | Durum |
|---|---|---|---|---|---|
| 1 | `cpp-007` | Doğrulama geçişi performans bulgusunu "somut girdiyle kanıtlanamadı" diye düşürüyor | Parça 2 raporu `meta.warnings`; model bulguyu bulmuştu | doğrulama | Açık → Faz 39 |
| 2 | `unity-104` | "Temiz" etiketliydi ama `rb.velocity` ataması y = 0 ile yerçekimini iptal ediyor | 14. satır | etiket | Düzeltildi (`2f51cdc`) |
| 3 | `unity-009`, `cpp-106`, `csharp-014`, `unity-104` | Doğru satır, farklı kategori (performance↔garbage_collection, undefined_behavior↔memory_safety, resource_leak↔garbage_collection, design↔engine_best_practice) | Parça 1-2 `eval analyze` | kategori | Açık → Faz 40 |
