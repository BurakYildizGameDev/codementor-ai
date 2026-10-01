# ADR-0014: Masaüstünde sağlayıcı bağlantıları, model seçimi ve API anahtarı saklama

**Tarih:** 2026-10-01 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.5, §12, §17; ADR-0012, ADR-0013

## Bağlam

Masaüstü uygulamasında (ADR-0013) sağlayıcı yalnızca bir açılır listeden seçilebiliyordu; model
adı, Ollama adresi ve API anahtarları `codementor.toml` ve ortam değişkenleriyle veriliyordu.
Kullanıcı Ollama'yı bağladığında "hazır değil" gördü: yapılandırma `qwen2.5-coder:7b`
istiyordu, makinede `qwen2.5-coder:1.5b` ve `:14b` kuruluydu. Ayrıca Claude Code, Antigravity
(agy), Anthropic, OpenAI ve DeepSeek için oturum açma ve yetkilendirme yapılabilecek bir yer
istendi. Exe kullanıcısından toml düzenlemesi ya da ortam değişkeni tanımlaması beklenemez.

## Karar

1. **Bağlantılar ekranı:** sağlayıcı başına bir kart: durum, model seçici (öneri + canlı keşif
   + serbest metin), yetkilendirme, "Varsayılan yap", "Denetle", "Bağlantıyı dene".
2. **Model ve adres seçimleri** `DesktopPrefs.providers` (`models.desktop.ProviderOverride`:
   `model`, `base_url`, agy için `allow_tool_agent`) olarak `~/.codementor/desktop.json`'a
   yazılır ve `connections.apply_overrides` ile toml + ortamdan gelen ayarların **üstüne**
   uygulanır. Kaynak ayarlar değişmez. CLI, API ve Web bu tercihleri görmez; onlar için
   toml geçerlidir.
3. **API anahtarları** yalnızca işletim sisteminin kimlik kasasında (`keyring`; Windows'ta
   Kimlik Bilgisi Yöneticisi, hizmet adı "CodeMentor AI") saklanır. Dosyaya ve log'a yazılmaz.
   Açılışta ve kayıtta anahtar yalnızca **uygulama sürecinin** ortamına (`api_key_env`) konur.
   Sağlayıcı kodu anahtarı her zamanki gibi ortamdan okur (AGENTS kural 5 değişmez) ve
   `log.register_secret` ile maskelenir. Dış ortamda zaten tanımlı bir anahtar ezilmez.
4. **Durum yoklaması** mevcut `providers.health.check_providers` üstüne kurulur:
   - Ollama: `GET /api/tags`. Kurulu modeller seçici listesine gelir.
   - claude_cli: `claude auth status --json` → `loggedIn` ve hesap.
   - agy: `agy models` → oturum ve model listesi. Araç onayı (ADR-0012
     `allow_tool_agent`) kartta açık bir anahtar olarak verilir; onay yoksa "hazır değil".
   - API sağlayıcıları: anahtar var mı. "Bağlantıyı dene" ise birkaç token'lık gerçek bir
     yapılandırılmış istek gönderir (`ConnectionPing`).
   CLI'lar mevcut `validation.runner.run_process` ile çalıştırılır: mutlak yol, sabit argv,
   boş çalışma dizini, süre sınırı.
5. **Oturum açma:** CLI'nın kendi etkileşimli akışı yeni bir konsol penceresinde başlatılır
   (`claude auth login`, `agy`). Uygulama parola ya da token görmez.
6. Model önerileri koda gömülmez: `data/desktop_models.yaml` (yalnız öneri, alan serbest metin).

## Sonuçlar

- Exe kullanıcısı toml veya ortam değişkenine dokunmadan her sağlayıcıyı bağlayabilir.
- `keyring` yeni çalışma bağımlılığıdır. Kasa kilitliyse açılış etkilenmez; kart Türkçe hata
  gösterir.
- Masaüstü ile CLI/API farklı modeller kullanıyor olabilir. Ekran "Yapılandırma" konumunu
  gösterir; bu bilinçli bir ayrımdır (masaüstü tercihleri kişiseldir).
- Testler gerçek kasaya, ağa ya da CLI'lara dokunmaz: sahte kasa, respx, sahte süreç çalıştırıcı.
