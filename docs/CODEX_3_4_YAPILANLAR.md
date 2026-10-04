# Codex dev ölçümü: 3/4 ve 4/4

**Tarih:** 2026-10-04  
**Dal:** `faz/36-hata-oneri`  
**Faz:** 36 / ölçüm takibi Faz 38  
**Sağlayıcı / model:** Codex CLI / `gpt-6-luna`  
**Mod:** `two_pass`, doğrulama açık, güncel dev etiketleri

## Neden Codex kullanıldı?

Claude CLI bu ortamda kapalıydı. Kullanıcı talimatıyla Codex CLI kullanıldı. Bu nedenle sonuçlar
Claude Opus 5.5 koşularının devamı olarak değerlendirilmedi. Aynı modele dayalı birleşik Codex
ölçümü elde etmek için yalnızca 3/4 ve 4/4 değil, daha önce Claude ile çalıştırılmış 1/4 ve 2/4
de Codex `gpt-6-luna` ile yeniden koşturuldu.

Codex sağlayıcısı bu koşuda `CODEMENTOR_PROVIDERS__CODEX__ALLOW_TOOL_AGENT=true` ve
`CODEMENTOR_PROVIDERS__CODEX__MODEL=gpt-6-luna` ayarlarıyla etkinleştirildi. CLI, ADR-0017
gereği `--sandbox read-only` ve geçici çalışma diziniyle çalıştı. Ayarlar yalnızca koşu sürecine
verildi; `codementor.toml` değiştirilmedi.

## Parça sonuçları

| Parça | P / R / F1 | FP / FN | Öneri | p50 (sn) | Token ort. | Sonuç |
|---|---:|---:|---:|---:|---:|---|
| 1/4 | 71 / 65 / 68 | 7 / 9 | 0 | 20,2 | 38 687 | [`20261003T231139_codex_gpt-6-luna_two_pass_part1-4_dev.json`](../eval/results/20261003T231139_codex_gpt-6-luna_two_pass_part1-4_dev.json) |
| 2/4 | 84 / 80 / 82 | 3 / 4 | 1 | 19,0 | 37 761 | [`20261003T231927_codex_gpt-6-luna_two_pass_part2-4_dev.json`](../eval/results/20261003T231927_codex_gpt-6-luna_two_pass_part2-4_dev.json) |
| 3/4 | 79 / 79 / 79 | 4 / 4 | 0 | 19,8 | 39 501 | [`20261003T223953_codex_gpt-6-luna_two_pass_part3-4_dev.json`](../eval/results/20261003T223953_codex_gpt-6-luna_two_pass_part3-4_dev.json) |
| 4/4 | 81 / 85 / 83 | 5 / 4 | 0 | 18,2 | 41 074 | [`20261003T224706_codex_gpt-6-luna_two_pass_part4-4_dev.json`](../eval/results/20261003T224706_codex_gpt-6-luna_two_pass_part4-4_dev.json) |
| **Birleşik 96** | **79 / 77 / 78** | **19 / 21** | **1** | — | — | dört sonuç dosyasından, güncel etiketlerle |

Birleşik ölçümde 70 doğru hata tahmini, 89 hata tahmini ve 91 etiketli hata vardır. Dört koşuda
da `errors=0`, model kullanılamadı uyarısı yok ve şema ilk denemede %100'dür.

## Öneri denetimi

Tek öneri `unity-104` satır 13'te `FixedUpdate` içinde girdi okunmasının kısa süreli girdileri
kaçırabileceğini belirtiyor. Eşleştirici bunu aynı kategori ve yakın satır nedeniyle satır 14'teki
etiketli hatayla aday çakışma olarak gösterdi. Etiketli hata `rb.velocity` atamasının dikey hızı
sıfırlayıp yerçekimini iptal etmesiyle ilgilidir. Önerinin açıklaması farklı bir konuyu kapsıyor;
elle incelemede gerçek hata öneriye düşmüş sayılmadı. Gerçek öneri-hata yutma: **0/1**.

## Faz 35B ile kıyas sınırı

Faz 35B Opus doğrulama koşusuyla ortak 46 örnekte Opus sonucu 79 / 89 / 84, Codex sonucu
75 / 73 / 74'tür. Sağlayıcı ve model farklı olduğu için bu betimleyici bir kıyastır; Faz 36'nın
precision artışı veya recall hedefi hakkında nedensel sonuç vermez. Codex alternatifi tek başına
"kaçırma oranı düşmez" hedefini doğrulamıyor.

## Belgelere işlenenler

- `docs/EVAL_PARCA_REHBERI.md`: dört Codex parçası, birleşik sonuç, alternatif koşu komutu ve
  yakın satır eşleşmelerinin elle denetlenmesi.
- `docs/eval-findings.md` §11: parça metrikleri, öneri denetimi ve karşılaştırma sınırı.
- `README.md`: güncel dev sonuç tablosu ve Claude/Codex ölçümlerinin ayrı olduğuna dair not.
- `PROGRESS.md` ve `docs/UYGULAMA_PLANI.md`: Codex alternatifi tamamlandı; özgün Claude
  karşılaştırması açık olarak kaydedildi.
- `docs/EVAL_PARCA_REHBERI.md` "Bulunan sorunlar": kategori karışıklıkları ve `unity-104` için
  otomatik eşleştiricinin yanlış aday çakışması.

Yalnızca dokümantasyon ve eval sonuç dosyaları değiştirildi; prompt, kural ve analiz davranışı
değiştirilmedi. Doküman değişikliği için test çalıştırılmadı; `git diff --check` temizdi.
