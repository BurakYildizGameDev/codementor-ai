# ADR-0033: Token tahmini 3 değil 2 karakter/token

**Tarih:** 2026-10-21 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.4.5, §13

## Bağlam

Prompt bütçesi (§5.4.5) sağlayıcıdan bağımsız yaklaşık sayımla hesaplanır:
`estimate_tokens = ceil(len(text) / CHARS_PER_TOKEN)`. Faz 8'de sabit, "kod ve Türkçede ~3
karakter/token; temkinli olmak için 3 (fazla tahmin, taşmadan iyidir)" gerekçesiyle 3 seçildi.
Sonraya'daki "token tahmininin gerçek `usage` ile kalibrasyonu" maddesi o günden beri açıktı.

2026-10-21 canlı dev ölçümünde (claude_cli, Opus 5.5, two_pass, 96 örnek) her örneğin Geçiş A
girdisi gerçek `usage` ile kaydedildi (`meta.stage_tokens.llm_a.input`). Aynı örneklerin Geçiş A
mesajları FakeProvider ile çevrimdışı yeniden üretilip `estimate_messages` ile sayıldı:

- 76 örnekte tahmin / gerçek medyanı **0,48**; hiçbir örnekte 0,5'i geçmiyor.
- Şema onarımı yapılan örnekler (Geçiş A iki kez çağrılır) çıkarılınca 53 örnekte
  `gerçek ≈ 1,64 × tahmin + 1379`, **r = 0,998**. Sabit terim çıkarılınca ~1,8 karakter/token.

Yani tahmin "temkinli" değil, gerçeğin yarısıydı. Bütçe denetimi taşan prompt'u geçirebilir;
`num_ctx`'i dar bir yerel sağlayıcı fazlasını sessizce kırpar. Bu da "kod asla kırpılmaz"
ilkesini (§5.4.5) delerdi.

## Karar

`CHARS_PER_TOKEN = 2`. Tahmin yine gerçeğin biraz altında kalır (sabit ek yük yüzünden kısa
prompt'larda daha çok), ama bütçe hesabı zaten çıktı payı ve şemayı ayrıca düşer. Daha küçük bir
sabit (ör. 1,8) Claude'a özgü olurdu; diğer sağlayıcıların tokenlaştırıcıları ölçülmedi. 2 yuvarlak
ve sağlayıcıdan bağımsız temkinli bir üst sınır olarak seçildi.

## Sonuçlar

- 40 KB'lık kod (`limits.max_bytes`) artık ~20k token sayılır (eskiden ~15k). Dar sağlayıcıda en
  büyük kod için ~24k token prompt bütçesi gerekir. Ollama'da `num_ctx = 32768` önerisi geçerli;
  varsayılan 16384 ile en büyük kodlar bütçe hatasıyla reddedilir, sessizce kırpılmaz.
- Kırpma (few-shot → kontrol listesi → olgular → kural bulguları) daha erken devreye girer. Claude
  ve Codex'in 200k bağlamında pratik etkisi yoktur.
- Onarım prompt'unda ham yanıtın kırpma sınırı (`room * CHARS_PER_TOKEN`) küçülür, yani daha temkinli olur.
- Sağlayıcı token bildirmediğinde kullanılan çıktı tahmini (`usage_estimated`) büyür, gerçeğe yaklaşır.
- Testlerdeki dar bağlam değerleri yeni orana göre büyütüldü; kırpma testleri sabiti içe aktarır.
