# ADR-0021: OpenAI ve DeepSeek sağlayıcıları kaldırıldı; Gemini ve agy deneysel

**Tarih:** 2026-10-03 · **Durum:** Kabul edildi ·
**Etkilenen bölümler:** mimari §5.5, §17; ADR-0014, ADR-0020 (kısmen geçersiz kılar)

## Bağlam

Faz 7'de `openai` ve `deepseek` API sağlayıcıları, Faz 28'de `gemini` eklendi. Üçü de ortak
`OpenAICompatProvider` katmanını kullanıyordu: OpenAI ve Gemini katı `json_schema`, DeepSeek
JSON modu (şema prompt içinde). Kullanıcının bu servisler için API anahtarı yok ve
alamayacak. Sonuç:

- Hiçbiri gerçek bir istekle sınanmadı; Faz 28'deki düzeltmeler yalnızca belgelere göre yapıldı.
- Model adları sağlayıcı tarafında değişince sessizce bozuluyorlar. Faz 28'de DeepSeek'in
  `deepseek-chat` / `deepseek-reasoner` adlarını kapattığı ancak belge denetimiyle fark edildi.
- Eval'de hiç ölçülmediler; bakım ve test yükü taşıyor, kullanıcıya değer üretmiyorlardı.

Kullanıcı kararı (2026-10-03): OpenAI ve DeepSeek kaldırılsın; Gemini ve Antigravity (`agy`)
kalsın ama deneysel olarak işaretlensin. Codex CLI ve Anthropic API değişmez.

## Karar

1. `openai` ve `deepseek` sağlayıcı kaydından (`PROVIDER_NAMES`), yapılandırmadan
   (`OpenAIConfig`, `DeepSeekConfig`, `[providers.openai|deepseek]`), masaüstü Bağlantılar
   listesinden ve model öneri dosyalarından çıkarılır. API'nin `/v1/providers` yanıtı ve web
   arayüzü bu listeyi kullandığı için oralardan da kalkar.
2. Eski bir yapılandırmada `default` ya da `fallback` bu adlardan birini gösteriyorsa analiz
   "bu sağlayıcı kaldırıldı (ADR-0021)" hatasıyla durur (`REMOVED_PROVIDERS`). Eski TOML
   bölümleri yok sayılır, çökme olmaz. Masaüstü tercihindeki eski ad zaten varsayılana döner.
3. `OpenAICompatProvider` kalır, çünkü Gemini OpenAI uyumlu ucu kullanıyor (ADR-0020). Yalnızca
   katı şema modu kalır; DeepSeek'e özgü JSON modu ve `SchemaAdapter.prompt_text()` silinir.
4. Gemini ve agy "deneysel" olarak işaretlenir: masaüstü kart açıklaması ve `providers check` /
   `/v1/providers` durum metni ("deneysel, ADR-0020" / "deneysel, ADR-0012").
5. `data/retired_models.yaml` mekanizması korunur (Gemini için), DeepSeek girdileri silinir.

## Sonuçlar

- (+) Daha az kod ve test; doğrulanamayan üç sağlayıcıdan ikisi gitti. Desteklenen yollar:
  `claude_cli` (ölçülen, varsayılan), `codex`, `ollama`, `anthropic`; deneysel: `gemini`, `agy`.
- (+) Kullanıcı arayüzünde çalışmayacak seçenekler görünmüyor.
- (−) OpenAI veya DeepSeek anahtarı olan bir kullanıcı bu sürümde onları kullanamaz. Geri
  almak gerekirse: kod `ec6051e` / `30c86f8` commit'lerinde; uyumlu uç katmanı hâlâ
  mevcut olduğundan OpenAI'yi geri eklemek küçük bir iştir (config sınıfı + factory dalı).
- (−) Kullanıcının işletim sistemi kasasında (keyring) daha önce kaydedilmiş OpenAI/DeepSeek
  anahtarları silinmez; uygulama onları artık okumaz.
