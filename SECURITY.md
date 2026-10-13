# Güvenlik politikası · Security policy

## Desteklenen sürümler

Yalnız en son release güvenlik düzeltmesi alır.

| Sürüm | Destek |
|---|---|
| 0.1.x (son) | ✅ |
| daha eski | ❌ |

## Açık bildirimi

Lütfen güvenlik açıklarını **herkese açık issue olarak açmayın**. GitHub'da depo sayfasındaki
**Security → Report a vulnerability** (özel güvenlik bildirimi) ile bildirin. Bildiriminizde:

- etkilenen sürüm ya da commit, işletim sistemi, arayüz (masaüstü / CLI / API / web);
- yeniden üretme adımları ve mümkünse en küçük girdi (kod parçası, istek gövdesi);
- beklenen ve gözlenen davranış, olası etki.

İlk yanıt hedefi 7 gün; doğrulanan açıklar için düzeltme bir yama sürümüyle yayımlanır ve
bildiren kişi (isterse) CHANGELOG'da anılır.

*English:* please do not open public issues for vulnerabilities. Use GitHub's **Report a
vulnerability** button (private advisory). We aim to respond within 7 days.

## Kapsam ve tehdit modeli

CodeMentor'a gönderilen kod **güvenilmeyen veridir** (`docs/mimari.md` §12). Özellikle ilgilendiğimiz
konular:

- **Kod çalıştırma / dosya sistemi:** kullanıcı kodu hiçbir zaman çalıştırılmaz. Tier 1 derleyicisi
  kodu yalnız stdin'den alır, boş geçici dizinde, temizlenmiş ortamla ve işletim sistemi kaynak
  sınırlarıyla çalışır; derleyiciyi kodun dışındaki bir dosyayı okumaya yönlendiren `#include`
  biçimleri reddedilir. Bunları aşan her girdi kapsamdadır.
- **Prompt injection ve çözüm sızıntısı:** kullanıcı kodu ve soru metinleri prompt'ta veri olarak
  sarılır; sınırlayıcı ve rol etiketi taklitleri etkisizleştirilir. Bunu aşıp modele talimat
  verdiren ya da referans çözümü öğrenciye taşıyan girdiler kapsamdadır.
- **Hizmet engelleme:** 40 KB sınırındaki bir girdinin analizi kilitlemesi (karesel/üstel regex,
  ayrıştırıcı patlaması) kapsamdadır.
- **API:** varsayılan yalnız `127.0.0.1`'e bağlanır; Host doğrulaması, gövde sınırı ve isteğe bağlı
  API anahtarı vardır (ADR-0023). Bu korumaları aşan istekler kapsamdadır.

Kapsam dışı: kullanıcının kendi makinesinde kendi yapılandırmasını (`codementor.toml`, ortam
değişkenleri) değiştirerek elde ettiği etkiler; imzasız exe için SmartScreen uyarısı; LLM
sağlayıcılarının kendi hizmetlerindeki sorunlar.
