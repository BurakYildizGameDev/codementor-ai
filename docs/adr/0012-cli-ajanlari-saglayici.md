# ADR-0012: CLI ajanları (Claude Code, Antigravity) LLM sağlayıcısı olarak

**Tarih:** 2026-09-29 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.5.2, §12, §17; ADR-0009, ADR-0011

## Bağlam

Mimari §5.5 LLM'e yalnızca HTTP API'leriyle (Ollama, OpenAI, DeepSeek, Anthropic) erişiyordu.
Geliştirici bulut API anahtarı yerine abonelikli CLI ajanlarını kullanıyor: Claude Code
(`claude`) ve Antigravity (`agy`). Her ikisi de print modunda JSON şemasıyla yapılandırılmış
çıktı verebiliyor (`-p --output-format json --json-schema ...`). Canlı denemeler (2026-09-29):

- `claude -p --output-format json --json-schema S --tools ""` → `structured_output` (hazır
  nesne), `result`, `is_error`, `subtype`, `api_error_status`, `usage`, `modelUsage`.
  Basit istek ~4 sn; EnemyRadar analizi ~34 sn. Şemadaki `maxLength`/`maxItems` zorlanmıyor:
  kısıtlar çıkarılınca model 8 soru ve 80+ karakterlik kavram yazdı.
- `agy -p ...` oturum açılmamışken `status: SUCCESS`, `response: ""`, `num_turns: 0` döndürüyor
  (hata değil). Araçları kapatan bir bayrağı yok; yalnızca `--sandbox` ve `--print-timeout` var.
- Bu ajanlar dosya okuyabilen, komut çalıştırabilen araçlara sahip. Öğrenci kodu güvenilmez
  veridir (§12): kodun içine yazılmış bir talimat ajanı araç kullanmaya yönlendirebilir.

## Karar

1. `providers/cli_agent.py` → `CliAgentProvider` iki profil: `claude_cli`, `agy`
   (`[providers.claude_cli]`, `[providers.agy]`; `command`, `model`, `timeout_s = 300`).
2. **Güvenlik:**
   - **Tüm mesajlar** (sistem mesajı dahil) yalnızca **stdin** ile, `<system>`/`<user>`
     sınırlayıcılarıyla verilir; argv'de yalnızca sabit bayraklar, şema JSON'u, model adı ve
     sabit bir `--system-prompt` (`FIXED_SYSTEM`) bulunur. Böylece "argv'de kullanıcı verisi
     yok" çağıranın iyi niyetine değil koda bağlıdır (Linux `/proc/<pid>/cmdline` okunabilir).
   - Çalıştırılabilir dosya yalnızca PATH'teki **mutlak** dizinlerde aranır; çalışma dizini
     hiç denenmez (Windows'ta `shutil.which` önce cwd'ye bakıyordu: öğrenci projesindeki bir
     `claude.exe` kullanıcının oturumuyla çalışabilirdi). Göreli komut (`./claude`) reddedilir.
   - `.cmd`/`.bat` kısayolu çalıştırılmaz (cmd.exe argümanları yeniden ayrıştırır,
     "BatBadBut"); işaret ettiği `.exe` kısayolun dizini **içinde** çözülür (`..` reddedilir).
   - Faz 4 çalıştırıcısı (`validation/runner.run_process`): boş geçici çalışma dizini, izin
     listeli ortam (+ yalnızca CLI'nin oturumunu bulması için kullanıcı profil değişkenleri;
     başka sağlayıcıların anahtarları geçmez), zaman aşımında süreç ağacını öldürme, 64 KB
     çıktı sınırı, Windows'ta Job Object (bellek 4 GB, süreç sayısı 64 — Node/Bun tabanlı
     CLI'ler için `ProcessLimits.max_processes` eklendi, varsayılan 8 değişmedi).
   - Claude: `--tools ""` (hiç araç yok) ve katmanlı savunma: `--restricted`, `--safe-mode`,
     `--strict-mcp-config`, `--permission-mode dontAsk`, `--permission-prompts none`,
     `--disable-slash-commands`, `--no-session-persistence`; ortamda `DISABLE_AUTOUPDATER=1`,
     `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`. Bu bayraklarla canlı çağrı doğrulandı.
   - agy: `--sandbox`, `--mode plan`, `--disable-slash-commands`, `--print-timeout`. Araç
     kapatma bayrağı olmadığı için **deneysel** ve varsayılan olarak **kapalı**: yalnızca
     `[providers.agy] allow_tool_agent = true` ile kullanılabilir; paylaşılan sunucuda (Faz 11)
     açılmamalı. agy'nin prompt'u stdin'den okuduğu ve print modunda izin isteklerini nasıl
     ele aldığı oturum açılmadığı için canlı doğrulanamadı.
   - POSIX'te dosya boyutu sınırı CLI için 64 MB (`ProcessLimits.file_size_bytes`); CLI kendi
     ayar/log dosyalarını yeniden yazar.
3. **Çıktı:** Claude'da `structured_output` varsa o, yoksa `result` metni; `is_error` →
   `api_error_status`'a göre `ProviderRateLimitError`/`ProviderServerError`/
   `ProviderRequestError`, durum yoksa `ProviderUnavailableError`. agy'de boş `response` →
   `ProviderUnavailableError` ("oturum açık mı?"). Zaman aşımı yeniden denenir; sıfır dışı
   çıkış ve JSON olmayan çıktı yeniden denenmez; stderr maskelenip kırpılır. **Zaman aşımı
   yeniden denenmez** (her deneme dakikalar sürer; fallback hemen sıradakine geçer). CLI'nin
   kendi sonuç nesnesi çıktının **sonundan** ve türünü belirten alanla (`type`/`status`)
   seçilir; model metnindeki sahte bir JSON satırı seçilemez. Yanıt veren model `modelUsage`
   içinden istenen ya da en çok çıktı üreten olarak alınır.
   - İptal: `asyncio` görevi iptal edilirse iş parçacığı süreci zaman aşımına kadar bekletir
     (süreç ağacı yine öldürülür); pipeline (Faz 10) zaman aşımını buna göre seçmeli.
     **Güncelleme (Faz 19):** iptal artık `threading.Event` ile `run_process`'e iletilir; süreç
     ağacı ~0,1 sn içinde öldürülür (masaüstü "Durdur", API'de kopan bağlantı).
4. **Şema:** Anthropic varyantı kullanılır. Zorlanamayan kısıtlar artık yalnızca çıkarılmıyor,
   alan açıklamasına Türkçe not olarak ekleniyor ("en fazla 80 karakter", "en fazla 4 öğe");
   bu değişiklik OpenAI ve Anthropic HTTP varyantlarına da uygulanır. Ollama varyantı ise
   kısıtları olduğu gibi korur (Ollama şemayı dilbilgisine çevirip zorlar; `deepseek-r1:8b`
   ile canlı doğrulandı). K5 yine aynı Pydantic modeliyle doğrular.
5. Model adı yapılandırmadan zorunludur (CLI varsayılanına bırakılmaz; rapor hangi modelin
   yanıt verdiğini bilmeli). Claude'da yanıt veren model `modelUsage` anahtarından okunur.

**Güncelleme (Faz 63, 2026-10-09, agy 1.3.1 canlı gözlem):**
- Kullanıcının **global MCP sunucuları** (`~/.gemini/config/mcp_config.json`) her `agy` çağrısında
  başlatılır; bağlanamayan biri (Unity kapalıyken `unity-mcp`) turu hiç başlatmaz: `num_turns: 0`,
  boş yanıt, `--print-timeout` dolar. Sunucu kaldırılınca aynı istek 5-7 sn'de döndü.
  `agy mcp disable`'ın yazdığı `"disabled": true` başsız modda **yok sayılıyor**. agy'de
  Claude'daki `--strict-mcp-config` karşılığı yok; bu yüzden kodla çözülemez, kullanıcı mesajı
  ve README'de yönlendirilir (`AGY_STALL_HINT`).
- `result` olayında `structured_output` gelir; tercih edilir. agy yanıttan sonra kendiliğinden
  ikinci tur açıp `response` metnine araç izi ekleyebilir (`{"ok": true}
{"toolAction": ...}`);
  metinden **ilk** JSON nesnesi alınır, metin boşsa ilk `agent_response` adımının `text_delta`
  parçaları birleştirilir. Şema doğrulaması (K5) değişmedi. Fixture:
  `tests/providers/fixtures/agy_stream_result.ndjson`.
- `--mode plan`, `--disable-slash-commands` ile birlikte agy'ye göre etkisiz ("has no effect")
  ve izin modu `request-review` kalır. Bayrak zararsız olduğu için tutuldu; araç kapatma yine
  yok, risk değerlendirmesi değişmedi.

## Sonuçlar

- (+) API anahtarı olmadan, aboneliklerle geliştirme ve eval yapılabilir; fallback zincirine
  eklenebilir (`fallback = ["claude_cli"]`).
- (+) Claude CLI'de araçlar tamamen kapalı; prompt injection araç çağrısına dönüşemez.
- (−) CLI ajanları API'den yavaş (süreç başlatma + ajan döngüsü) ve maliyet/kota ölçümü
  CLI'nin bildirdiği `usage`'a bağlı.
- (−) agy'de araç kapatılamıyor; risk yalnızca sandbox ve boş çalışma dizini ile sınırlanıyor.
- (−) CLI çıktı biçimi sürümle değişebilir; kayıtlı gerçek çıktı fixture olarak tutuluyor
  (`tests/providers/fixtures/claude_cli_result.json`) ve canlı test (`-m live -k cli_agent`) var.

## Değerlendirilen seçenekler

- **Claude Agent SDK / resmi SDK:** ek bağımlılık ve ayrı kimlik akışı; kullanıcının CLI
  oturumunu doğrudan kullanmıyor. Reddedildi.
- **Prompt'u argv'de vermek:** Windows'ta 32 K komut satırı sınırı (40 KB koda yetmez) ve
  `.cmd` ayrıştırma riski. Reddedildi.
