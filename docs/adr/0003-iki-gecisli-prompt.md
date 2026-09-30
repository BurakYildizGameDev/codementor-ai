# ADR-0003: İki geçişli prompt varsayılan kalır — gerekçe kalite değil güvenlik payı

**Tarih:** 2026-09-30 · **Durum:** Kabul edildi (ölçümle güncellendi) · **Etkilenen bölümler:** mimari §5.4.2, §14, §23; UYGULAMA_PLANI Faz 12

## Bağlam

Mimari §5.4.2 LLM aşamasını iki geçişe böler: A (analiz: karmaşıklık, ek bulgular) ve
B (mentorluk: doğrulanmış analizden Sokratik sorular). Gerekçe: doğrulanmamış bulgular soruya
dönüşmesin, sızıntı kontrolü ayrı yapılsın, ton bağımsız ayarlansın. `pipeline.mode =
"single_pass"` aynı işi tek çağrıda yapar. §23 tablosu kararı "eval ile teyit edilecek"
diye bırakmıştı. Faz 12'de ikisi aynı prompt sürümüyle (`v1+fbc08625`), aynı modelle
(`claude-opus-5-5`, `claude_cli`), önbellek kapalı ölçüldü. Ayrıntılar:
`docs/eval-findings.md`.

## Ölçüm

| | two_pass dev | single_pass dev | two_pass test | single_pass test |
|---|---|---|---|---|
| Örnek (LLM'e giden) | 31 (26) | 31 (26) | 49 (34) | 49 (34) |
| Şema (onarım sonrası) | 100% | 100% | 100% | 100% |
| Big-O birebir | 96% | 92% | 91% | 94% |
| Denetim P / R / F1 | 27 / 92 / 42 | 32 / 96 / 47 | 27 / 92 / 42 | 32 / 94 / 48 |
| Satır doğruluğu | 100% | 96% | 94% | 94% |
| Sızıntı / injection direnci | 0% / 100% | 0% / 100% | 0% / 100% | 0% / 100% |
| Sızıntı korumasının müdahalesi | 2 | 6 | 9 | 11 |
| p50 / p95 (sn) | 23.5 / 40.0 | 13.1 / 24.5 | 20.3 / 57.3 | 13.5 / 35.7 |
| Token ort. | 14.2 bin | 9.4 bin | 15.7 bin | 10.2 bin |

## Değerlendirme

- **Kalite:** two_pass'in kalite üstünlüğü **teyit edilmedi**. Farklar 1–2 örnek düzeyinde;
  denetim F1'de single_pass iki bölümde de biraz önde (47–48 vs 42), Big-O'da yön karışık.
  Bu model için ek bulguların doğrulanması B'den önce ya da sonra yapılsa da sonuç değişmiyor.
- **Maliyet:** single_pass ~%35–45 daha hızlı, ~%35 daha az token.
- **Güvenlik payı:** son çıktıdaki sızıntı iki modda da %0. Ancak sızıntı koruması
  (Faz 9/10; 5-gram + işaret listesi, sezgisel) single_pass'te LLM'e giden 60 örneğin
  17'sinde, two_pass'te 11'inde devreye girdi (~1,5×). Yani single_pass'in %0'ı korumaya
  daha çok yaslanıyor. Korumanın kaçırdığı biçimde (ör. başka dilde, yeniden adlandırılmış)
  bir sızıntı olursa bunu yakalayacak ikinci bir katman yok.
- Ölçülen tek model güçlü bir model. §5.4.2'nin asıl kaygısı (doğrulanmamış bulgunun
  soruya dönüşmesi) daha zayıf yerel modellerde daha belirgin olabilir; bu ölçülmedi.

## Karar

1. Varsayılan **`two_pass` kalır**. Gerekçe artık "daha iyi kalite" değil: ürünün birincil
   riski çözümün sızması ve two_pass bu riski sezgisel korumaya ulaşmadan azaltıyor.
   Ek maliyet (~1,5× token, ~1,6× gecikme) mentorluk kullanımında (tek öğrenci, tek dosya)
   kabul edilebilir.
2. `single_pass` **desteklenen hızlı mod** olarak kalır; kalite kaybı ölçülmediği için
   gecikme/maliyet öncelikliyse (toplu analiz, API yükü) önerilir. Sızıntı koruması her iki
   modda da zorunludur (değişmedi).
3. Karar model başına geçerlidir: başka bir model/sağlayıcı varsayılan yapılırsa iki mod
   dev bölümünde yeniden ölçülür (`codementor eval run --split dev --mode ...`).

## Sonuçlar

- Mimari §5.4.2 ve §23'teki "eval ile teyit edilecek" ifadeleri bu ADR'ye bağlanır.
- Sızıntı korumasının müdahale sayısı şu an yalnızca rapor uyarılarından sayılabiliyor;
  eval metriği olarak eklenmesi PROGRESS.md "Sonraya" bölümüne yazıldı.
