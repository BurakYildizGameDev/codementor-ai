# ADR-0020: Gemini sağlayıcısı OpenAI uyumlu uç nokta üzerinden

**Tarih:** 2026-10-03 · **Durum:** Kabul edildi, deneysel (canlı doğrulanmadı: API anahtarı
yok). OpenAI ve DeepSeek sağlayıcıları ADR-0021 ile kaldırıldı; uyumlu uç katmanını artık
yalnız Gemini kullanıyor ·
**Etkilenen bölümler:** mimari §5.5.2, §17; ADR-0008, ADR-0014

## Bağlam

Bağlantılar ekranında Gemini için API sağlayıcısı yoktu. Gemini yalnızca deneysel `agy`
CLI'ı üzerinden vardı. Kullanıcının API anahtarı yok ve canlı deneme yapılamıyor. Bu yüzden
karar, belgelenmiş ve en az belirsizlik taşıyan yola göre verildi. Belgeler 2026-10-03'te
okundu:

| Seçenek | Durum |
|---|---|
| OpenAI uyumlu uç (`https://generativelanguage.googleapis.com/v1beta/openai/`) | `Authorization: Bearer`, `/chat/completions`. Yapılandırılmış çıktının resmî örneği OpenAI SDK'nın `beta.chat.completions.parse()` çağrısı. Bu çağrı katı `json_schema` gönderir (`additionalProperties: false`, tüm alanlar zorunlu); bizim `openai_strict` şemamızla aynı biçim |
| Yerel API | Belgeler yeni Interactions API'ye (`/v1beta/interactions`, `response_format`) kaymış. `generateContent` ile `responseSchema`/`responseJsonSchema` ayrımı sürümler arasında değişmiş. Canlı doğrulama olmadan riskli |

## Karar

1. `gemini` sağlayıcısı mevcut `OpenAICompatProvider`'ın katı şema modudur. Ayrı bir HTTP
   istemcisi, şema dönüştürücüsü ya da hata eşlemesi yazılmadı. OpenAI'ın tüm sözleşme
   testleri Gemini düzeneğinde de koşar.
2. Farklar yapılandırılır, kodda dallanmaz:
   - çıktı sınırı `max_tokens` alanıyla gönderilir; `max_completion_tokens`'ın Gemini
     arka ucunda kaybolduğu bildirilmiş;
   - `seed` gönderilmez, çünkü belgelenmemiş;
   - `temperature` yalnızca yapılandırmada verilirse gönderilir.
3. `[providers.gemini]` yapılandırması:
   - `base_url` ve `api_key_env = "GEMINI_API_KEY"` varsayılan olarak gelir;
   - `model` boştur (ADR-0008); öneriler `data/desktop_models.yaml`'da;
   - anahtar Bağlantılar'dan kimlik kasasına kaydedilir (ADR-0014).
4. Gemini uyumlu ucunun hata gövdesi bazen tek öğeli liste (`[{"error": {...}}]`) olarak
   gelir. Ortak HTTP katmanı bu biçimi okur. Günlük kota (`quota_exceeded`) yeniden
   denenmez.

## Sonuçlar

- (+) Ek kod yok denecek kadar az. OpenAI yolunda bulunan her düzeltme Gemini'ye de gider.
- (+) Katı şema kuralları testle denetleniyor: her LLM şeması kök nesne, kapalı, tüm
  alanlar zorunlu, yalnızca izinli anahtar sözcükler, `minItems` yok.
- (−) Google uyumlu ucunu "beta" olarak tanımlıyor. Bir parametre sessizce yok sayılabilir.
  Bu durumda K5 doğrulaması ve onarım döngüsü yine korur.
- (−) **Canlı doğrulanmadı.** İlk anahtarla `codementor providers check --provider gemini`,
  ardından Bağlantılar → "Bağlantıyı sına" ve
  `uv run pytest tests/live -m live -k gemini` çalıştırılmalı.
