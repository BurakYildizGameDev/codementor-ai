# ADR-0025: Tier 0 ayrıştırmasını alt süreçte süre ve bellek sınırıyla yalıtma

**Tarih:** 2026-10-06 · **Durum:** Kabul edildi · **Günceller:** ADR-0024 ·
**Etkilenen bölümler:** mimari §4.3, §5.2.4, §12; plan Faz 59

## Bağlam

ADR-0024, tree-sitter 0.25.2'de ayrıştırmanın süreç içinde iptal edilemediğini ve 40 KB'lık
kasıtlı C# girdisinin (`a<`×20000) bir analiz iş parçacığını ~12 sn meşgul ettiğini kayda
geçirip yerel kullanım için kabul etmişti. Faz 59 ölçümü (2026-10-06, Windows 11, Python 3.12)
riskin yalnız süre olmadığını gösterdi:

| Ölçüm | Değer |
|---|---|
| C# `a<`×20000, süreç içi `run_tier0` | ~10 sn, **tepe bellek ~4,2 GB** (`K32GetProcessMemoryInfo`, PeakPagefileUsage) |
| Aynı girdi, alt süreç (1024 MB sınırı) | ~1 sn'de bellek sınırında ölür (`0xC0000005`), analiz durur |
| Aynı girdi, alt süreç (8192 MB, 1 sn süre) | 1 sn'de süre sınırında öldürülür |
| Geçerli C kodu (golden bağlı liste), süreç içi | p50 0,1 ms |
| Aynı kod, alt süreç | p50 278 ms, p95 296 ms (süreç açma + içe aktarma) |

API'de 4 eşzamanlı analiz sınırıyla bu girdi ~17 GB bellek isteyebilir: paylaşılan sunucuda
gerçek bir hizmet dışı bırakma riski.

## Karar

1. **İsteğe bağlı alt süreç.** `validation.tier0_isolation = true` iken Tier 0
   (`run_tier0`) `python -I -m codementor.validation.tier0_worker` alt sürecinde koşar;
   mevcut `runner.run_process` kullanılır: kod yalnız stdin ile gider, boş geçici çalışma
   dizini, temiz ortam, zaman aşımında süreç ağacı öldürülür, POSIX'te `RLIMIT_AS`,
   Windows'ta Job Object bellek sınırı. Süre ve bellek `tier0_timeout_s` (varsayılan 5) ve
   `tier0_memory_mb` (varsayılan 1024, en az 256: Linux'ta `RLIMIT_AS` sanal alanı sayar) ile yapılandırmadan gelir. Docker yok. İstemci iptali alt sürece bağlanmaz; işçi en fazla `tier0_timeout_s` yaşar.
2. **Varsayılan kapalı.** Araç yerelde tek kullanıcıyla çalışır; her analize ~280 ms eklemek
   yerel kullanımı yavaşlatır. Paylaşılan sunucuda açılmalıdır (`codementor.toml` notu).
3. **Fail-closed.** Süre aşımı, bellek sınırı (Windows'ta erişim ihlali olarak görünür, ayırt
   edilemez), çökme, iptal, kesilmiş ya da bozuk çıktı **error** tanısına çevrilir. Politika
   (§5.2.4) analizi erken bitirir; statik aşama aynı girdiyi süreç içinde yeniden
   ayrıştırmaz, LLM çağrılmaz. Rapora "eksik" uyarısı eklenir. Bu, plandaki "bozulmuş
   rapor olarak sürer" maddesinden bilinçli sapmadır: statik aşama aynı girdiyi süreç içinde
   yeniden ayrıştıracağı için sürdürmek riski geri getirirdi. Öğrenciye satır göstermeyen ayrı
   Sokratik şablonlar gider (`data/mentor_templates.yaml`); şablonlar `prefix: true` ile yalnız
   mesaj başında eşleşir, böylece tanıya giren kullanıcı kodu onları tetikleyemez. Alt süreç
   hiç başlatılamazsa (çalıştırılabilir yok, Job Object kurulamadı) mesaj kodu değil
   yapılandırmayı işaret eder ve `log.error` yazılır. Durdurma tanısı `tool="tree-sitter"`,
   `line=1` taşır (model satır ister); SARIF'te 1. satırda görünür (bilinen sınır).
4. **Yalnız tanılar taşınır.** Ağaç süreçler arasında taşınamaz; işçi `Tier0Result` JSON'u
   döndürür. Akışlar bayt düzeyinde UTF-8'dir (Windows borusu yerel kod sayfasıyla açılır).
5. **Exe'de desteklenmez.** PyInstaller exe'sinde `python -m` yoktur; masaüstü uygulaması tek
   kullanıcılıdır. Ayar açık olsa da uyarı loglanır ve süreç içinde koşulur.
6. **Kapsam:** yalnız Tier 0 yalıtılır. `extract_facts`'in hatalı ağaçtaki sorgu maliyeti
   (ADR-0024) boru hattında erişilemez kalır: Tier 0 hatasında analiz zaten erken biter.

## Sonuçlar

- Yalıtım açıkken ADR-0024'teki kabul edilmiş risk kapanır: kötü niyetli girdi bir iş
  parçacığını en fazla `tier0_timeout_s` meşgul eder, `tier0_memory_mb`'den fazla bellek alamaz.
- Yalıtım kapalıyken (varsayılan) davranış ve hız değişmez; risk ADR-0024'teki gibi kabul
  edilmiş durumdadır.
- Her yalıtılmış analiz bir Python süreci açar (Windows'ta ~280 ms). Daha yüksek yükte sıcak
  işçi havuzu: `validation.tier0_warm_workers`, aynı sınırlarla (ADR-0032).
- Testler: `tests/unit/test_tier0_isolation.py` (gerçek alt süreçle eşdeğerlik, süre ve bellek
  sınırı, hata yolları, exe geri dönüşü), `test_tier0_budget.py` (C# vakası artık kapsamda),
  `tests/integration/test_pipeline.py` (erken çıkış, LLM çağrısı yok).
