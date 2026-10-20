# ADR-0029: Çalışma dizinindeki codementor.toml güvenilmez katmandır

**Tarih:** 2026-10-13 · **Durum:** Kabul edildi · **Değiştirdiği:** ADR-0016 (hangi dosyanın
okunacağı) · **Etkilenen bölümler:** mimari §12, §17

## Bağlam

CLI, `codementor.toml`'u çalışma dizininden okur. Bir öğretmen ya da öğrenci `codementor analyze`'ı
öğrencinin proje klasöründen çalıştırırsa o klasördeki bir toml şunları değiştirebilir:
sağlayıcı `command` (keyfi komut çalıştırma), `base_url` (kod ve API anahtarı saldırganın sunucusuna
gider), `allow_tool_agent` (araç çalıştırabilen ajan), derleyici yolları ve indirme kaynakları,
`prompts.dir` (Jinja şablonları korumasızdır; şablon kod çalıştırabilir). Faz C'de `.env` aynı
gerekçeyle yüklenmemeye karar verilmişti; kod denetimi (2026-10-13) aynı tehdidin toml için açık
kaldığını gösterdi. Ayrıca kurulu wheel'de CLI, masaüstünün yazdığı `~/.codementor/codementor.toml`'u
okumuyordu.

## Karar

1. `CODEMENTOR_CONFIG_FILE` verilmişse yalnız o okunur ve tamamen güvenilir.
2. Verilmemişse katmanlar (önce gelen kazanır, bölümler birleşir): çalışma dizinindeki
   `codementor.toml` → `~/.codementor/codementor.toml` → paketteki varsayılan. İlk güvenilir
   katmanda durulur.
3. Çalışma dizinindeki dosya, paketin kendi `codementor.toml`'u değilse (depo kökünden geliştirme
   bu durumdadır, güvenilirdir) **güvenilmez katmandır**: tehlikeli anahtarları yok sayılır ve
   stderr'e uyarı basılır. Liste `config._UNTRUSTED_*`: sağlayıcı `command`, `base_url`,
   `api_key_env`, `allow_tool_agent`; `validation.toolchain_dir`, `zig`, `roslyn_check_*`,
   `stub_header`; `storage.db_path`, `max_analyses`, `session_retention_days`; `data`'nın tüm
   yolları (`questions_dir`, `checklists_dir`, `call_costs_file`, `mentor_templates_file`,
   `pricing_file`, `user_questions_dir`); `verify.common_identifiers_file`; `prompts.dir`;
   `api.host`, `cors_origins`, `allowed_hosts`, `api_key_env`, `allowed_providers`.
   *Güncelleme 2026-10-20 (tam tarama #3):* saklama ayarları ve veri dosyası yolları eklendi —
   öğrenci projesindeki `max_analyses = 1` global geçmişi budayabiliyor, kontrol listesi / mentor
   şablonu / yaygın tanımlayıcı dosyası prompt'a, öğrenciye ve sızıntı denetimine giden içeriği
   değiştirebiliyordu. Gerekçe aynı ("dosya sistemi yolları"); karar genişletildi, değişmedi.
4. Güvenli anahtarlar (model adı, varsayılan sağlayıcı, süre ve bütçe ayarları, kurallar, sınırlar)
   çalışma dizininden uygulanmaya devam eder: proje başına ayar akışı bozulmaz.

## Sonuçlar

- Öğrenci projesindeki toml komut çalıştıramaz, veriyi başka sunucuya gönderemez, dosya sistemine
  yazdıramaz. Gerçekten farklı bir komut gerekiyorsa dosya `CODEMENTOR_CONFIG_FILE` ile açıkça verilir.
- Masaüstü ve CLI aynı kullanıcı dosyasını okur (kurulu wheel).
- Testler geliştiricinin `~/.codementor/codementor.toml`'unu görmez (`tests/conftest.py`).
