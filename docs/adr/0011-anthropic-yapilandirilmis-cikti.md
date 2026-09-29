# ADR-0011: Anthropic yapılandırılmış çıktısı — zorunlu `tool_choice` yerine `output_config.format`

**Tarih:** 2026-09-29 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.5.2, §5.5.3, §17; UYGULAMA_PLANI Faz 7

## Bağlam

Mimari §5.5.2, Anthropic için yapılandırılmış çıktıyı "zorunlu araç çağrısı" ile almayı
öngörüyordu: şema bir aracın `input_schema`'sı olur, `tool_choice: {type: "tool"}` ile
model o aracı çağırmaya zorlanır. Aynı satırda "sağlayıcının güncel yapılandırılmış çıktı
özellikleri dokümandan kontrol edilmeli" notu vardı. Faz 7'de doküman kontrol edildi:

- Messages API artık yerel **JSON yapılandırılmış çıktı** sunuyor:
  `output_config: {format: {type: "json_schema", schema: {...}}}`. Beta başlığı gerekmez;
  yanıt, şemaya uyan JSON metni olarak `content[]` içindeki `text` bloğunda gelir. Şema
  kısıtlı çözümlemeyle zorlanır.
  Kaynak: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Güncel modellerin bir kısmı (Claude Opus 5.5, Sonnet 5.5, Fable 5.1) zorunlu
  `tool_choice` (`any` / `tool`) isteğini **400 ile reddediyor**. Mimarideki yol bu
  modellerde hiç çalışmaz.
- Aynı modeller `temperature` / `top_p` gibi örnekleme parametrelerini de reddediyor;
  Anthropic API'sinde `seed` hiç yok.
- Şema sınırları: `minLength`, `maxLength`, `pattern`, `minimum`, `maximum`, `multipleOf`
  desteklenmez; nesnelerde `additionalProperties: false` zorunlu; özyinelemeli şema yok.

## Karar

1. Anthropic adaptörü yapılandırılmış çıktıyı `output_config.format` ile ister; araç
   tanımlamaz, `tool_choice` göndermez. Sistem mesajları üst düzey `system` alanına taşınır;
   yanıttaki düşünme blokları atlanır, `text` blokları birleştirilir.
2. `temperature` yalnızca yapılandırmada ya da çağrı seçeneklerinde açıkça verilmişse
   gönderilir (varsayılan `None`). `seed` gönderilmez. Deterministiklik hedefi (§5.5.3)
   Anthropic'te sağlayıcı varsayılanlarına bırakılır.
3. `SchemaAdapter` desteklenmeyen kısıtları şemadan çıkarır; kısıtların kendisi K5'te
   (Faz 9) aynı Pydantic modeliyle doğrulanır, yani güvence kaybolmaz.
4. `stop_reason` `refusal` ise `parsed = None`; `max_tokens` ise yarım JSON `parsed = None`
   ile döner ve ham metin onarım (Faz 9) için korunur. `max_tokens` varsayılanı 16000
   (düşünme de bu bütçeden harcar).
5. Faz 7 kabul kriteri "araç `input_schema` = şema, `tool_choice` ile zorlanmış" yerine
   "`output_config.format.schema` = şema; `tools`/`tool_choice` yok" olarak test edilir.

## Sonuçlar

- (+) Güncel ve eski Claude modellerinin hepsinde tek yol; ek beta başlığı yok.
- (+) Araç çağrısı döngüsü gerekmez: yanıt doğrudan JSON metni.
- (−) Anthropic'te `temperature=0` + `seed` ile tekrarlanabilirlik yok; eval'de (Faz 12)
  tekrar sayısı artırılarak varyans ölçülmeli.
- (−) Yeni bir şemanın ilk kullanımında derleme gecikmesi olabilir (sağlayıcı 24 saat önbellekler).

## Değerlendirilen seçenekler

- **Zorunlu `tool_choice` (mimari ilk hali):** güncel modellerde 400; reddedildi.
- **`tool_choice: auto` + `strict: true` araç + prompt'ta "aracı çağır":** modelin aracı
  çağıracağı garanti değil; çağırmazsa yeniden deneme gerekir. Yerel JSON çıktısı varken
  gereksiz karmaşıklık; reddedildi.
- **Şemayı prompt'a gömüp serbest metin (DeepSeek gibi):** zorlama yok, onarım yükü artar;
  reddedildi.
