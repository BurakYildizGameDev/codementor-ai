# ADR-0032: Tier 0 sıcak işçi havuzu soğuk yolla aynı güvenlik sınırında çalışır

**Tarih:** 2026-10-20 · **Durum:** Kabul edildi · **Genişlettiği:** ADR-0025 · **Etkilenen
bölümler:** mimari §5.2, §12, §16, §20

## Bağlam

ADR-0025 Tier 0'ı `validation.tier0_isolation` açıkken `runner.run_process` ile alt süreçte koşturur:
boş geçici dizin, izin listeli ortam, Windows'ta Job Object (bellek + süreç sayısı), POSIX'te rlimit,
fail-closed başlatma. Her analiz yeni bir Python süreci açtığı için (~280 ms) Faz J'de
`validation.tier0_warm_workers` ile sıcak işçi havuzu eklendi (`validation/tier0_pool.py`). Tam tarama
(2026-10-20) havuzun bu sınırların hiçbirini uygulamadığını gösterdi: işçi düz `subprocess.Popen` ile
açılıyordu (bellek sınırı yok, API anahtarları dahil tüm ortam işçide, çalışma dizini kullanıcınınki,
Windows'ta konsol penceresi), havuz boşken her istek sınırsız yeni işçi açıyordu, kapatılan işçilerin
boruları ve süreçleri beklenmiyordu. Havuz açıldığında ADR-0025'in kestiği ~4,2 GB'lık tepe bellek
sessizce geri geliyordu.

## Karar

1. **Aynı sınır:** sıcak işçi `runner`'ın parçalarıyla başlatılır — `ProcessTree` (Windows: askıda
   başlat, Job Object'e ata, sonra devam ettir; kurulamazsa işçi öldürülür, `INFRA_MESSAGE`),
   `sanitized_env` (izin listesi), `launch_argv` (POSIX rlimit başlatıcısı), işçi ömrü boyunca yaşayan
   boş geçici çalışma dizini, `close_fds`, `stderr` atılır (okunmayan boru işçiyi tıkamasın).
2. **Birikimli CPU sınırı:** POSIX `RLIMIT_CPU` süreç ömrü boyunca birikir. İşçi en fazla
   `MAX_REQUESTS_PER_WORKER` (100) istekten sonra geri dönüştürülür; ömür CPU sınırı istek sayısı ×
   `tier0_timeout_s`'tir. Her istek duvar saatiyle `tier0_timeout_s`'e bağlı ve işçi tek iş parçacıklı
   olduğundan birikim bu sınırı aşamaz; sınır yalnız kaçak işçiyi keser.
3. **Eşzamanlılık:** canlı işçi sayısı `tier0_warm_workers` ile sınırlıdır (engellemesiz semafor).
   Hepsi meşgulse havuz sonuç döndürmez ve çağıran **soğuk yola** (ADR-0025, aynı sınırlar) düşer:
   ne sınırsız sıcak süreç ne de "meşgul" diye yanlış durdurma olur.
4. **Hata dili:** süre aşımı, işçi hatası ve başlatma hatası soğuk yolla aynı mesajları
   (`TIMEOUT_MESSAGE`, `FAILURE_MESSAGE`, `INFRA_MESSAGE`) ve `stopped=True` bayrağını kullanır
   (ADR-0025 Ö2: altyapı hatası öğrencinin koduna yüklenmez). Loglara ham işçi çıktısı yazılmaz,
   yalnız hata türü (§12).
5. **Yaşam döngüsü:** havuz süreç geneli tektir; `tier0_warm_workers`, `tier0_memory_mb` ya da
   `tier0_timeout_s` değişirse eski havuz kapatılıp yenisi kurulur; süreç çıkışında `atexit` ile
   kapanır. İşçi kapatılırken önce stdin kapatılır (EOF ile kendisi çıkar), gerekirse ağaç öldürülür,
   süreç beklenir, borular ve Job Object kapatılır.
6. Exe'de (`sys.frozen`) yalıtım yapılmadığından havuz da kullanılmaz (ADR-0025).

## Sonuçlar

- `tier0_warm_workers > 0` artık güvenlik ödünü değildir: 40 KB'lık C# bombası sıcak işçide de
  1024 MB'de durur (`tests/unit/test_tier0_pool.py::test_warm_worker_enforces_memory_cap`, ~2 sn).
- Her 100 istekte bir işçi yeniden açılır (~280 ms); ortalama maliyet ihmal edilebilir.
- Havuz meşgulken düşülen soğuk yol eski davranışla aynıdır; eşzamanlılık API'nin analiz yuvalarıyla
  zaten sınırlıdır.
- Bilinen sınırlar (denetim, 2026-10-20): bellek sınırı işçinin **ömrüne** uygulanır; büyük bir istekten
  sonra geri verilmeyen bellek, soğuk yolda geçecek bir sonraki isteği sıcak işçide `FAILURE_MESSAGE` ile
  durdurabilir (100 istekte geri dönüşüm ve hata sonrası işçinin kapatılması etkiyi sınırlar). Ayar
  değişince havuz yeniden kurulurken eski havuzun meşgul işçileri bırakılana dek canlı işçi sayısı geçici
  olarak en çok 2× sınır olabilir; süreç başına ayar sabit olduğundan pratikte görülmez.
- `runner._Tree` / `_launch_argv` public adlar aldı (`ProcessTree`, `launch_argv`); `tier0_isolation._stopped`
  → `stopped_result`.
