# Değişiklikler

Biçim [Keep a Changelog](https://keepachangelog.com/tr-TR/1.1.0/) esinli; sürümler
[Semantic Versioning](https://semver.org/lang/tr/). Ayrıntılı notlar: [PROGRESS.md](PROGRESS.md).

## [0.1.1] - 2026-10-13

Public yayın öncesi güvenlik ve doğruluk sürümü (Faz A-D, K).

### Güvenlik
- Include koruması yorumla bölünmüş yönergeleri de (`#/**/include`, `%:/**/include`) reddediyor.
- Dil tespitindeki kübik/karesel regex'ler doğrusal; 40 KB kötü niyetli girdi < 1 sn. Dil tespiti
  olay döngüsünü kilitlemiyor.
- Derleyici keşfi çalışma dizinindeki ve göreli `PATH` girdilerindeki çalıştırılabilirleri hiç
  denemiyor (öğrenci projesindeki sahte `gcc.bat` seçilemez).
- Prompt sınırlayıcı korumasına ek benzer karakterler ve `&lt;` biçimi eklendi.
- Kavram adı yalnız açılması gereken denemede rapora giriyor ve sızıntı denetiminden geçiyor.

### Düzeltilenler
- Onarım ya da mentorluk geçişi başarısız olunca doğrulanmış bulgular artık atılmıyor; süre
  sınırında da korunuyor.
- Yedek sağlayıcının ya da yarım kalan LLM'in raporu önbelleğe girmiyor; önbellek anahtarı
  çıktıyı etkileyen tüm ayarları, derleyiciyi ve soru içeriğini kapsıyor; önbellekten dönen
  raporda maliyet gösterilmiyor.
- Tek geçiş modunda doğrulanmamış bulgudan soru üretilmiyor.
- Masaüstünün "toml'a yaz" düğmesi kullanıcının satır içi/nokta anahtarlı ayarlarını silmiyor;
  yazım atomik; BOM'lu `codementor.toml` okunuyor. Exe'de ve pip kurulumunda yazılan dosya
  etkinleşiyor; pip kurulumu paketle gelen varsayılanları kullanıyor.
- CLI sistem hatalarında (veritabanı, dosya, bozuk yapılandırma) Türkçe mesaj ve çıkış kodu 3;
  kök `--help` UTF-8; `rules list` kapalı kuralları gösteriyor.

### Eklenenler
- Kendi sorunu ekleme: masaüstü formu ve `codementor questions add|remove` (ADR-0028).
- Token kullanımı her raporda (giriş/çıkış, aşama dağılımı, tahmini maliyet) ve Geçmiş'te toplam.
- Otomatik release (etiket → exe → duman testi → `SHA256SUMS`), Dependabot, güvenlik politikası,
  katkı rehberi, İngilizce README.

### Değişenler
- Sürüm tek kaynaktan (`codementor.__version__`).
- İç çalışma belgeleri `docs/gelistirme-gunlugu/` altına taşındı.

## [0.1.0] - 2026-10-09

İlk sürüm (Faz 0-63): hibrit analiz hattı, 34 statik kural, 64 görevlik soru bankası, masaüstü
uygulaması, web arayüzü, CLI ve REST API.
