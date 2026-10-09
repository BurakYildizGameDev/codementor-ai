# ADR-0023: API güven sınırı

**Tarih:** 2026-10-05 · **Durum:** Kabul edildi ·
**Etkilenen bölümler:** mimari §9, §12, §17; ADR-0009, ADR-0012, ADR-0017

## Bağlam

2026-10-04 tam taraması (K1, K2, K3, K7) yerel REST API'de istemcinin sunucu yapılandırmasını
aşabildiğini gösterdi:

1. `options.tier1: true`, `validation.tier1_enabled = false` ayarını eziyordu. Paylaşılan
   sunucuda Tier 1'i kapatma kararı (ADR-0009) istekle geri alınabiliyordu.
2. Host başlığı denetlenmiyordu. CORS yalnız tarayıcının yanıtı okumasını engeller; DNS
   rebinding ile kötü bir sayfa kendi alan adını 127.0.0.1'e çözdürüp aynı kökenden istek atabilir.
3. `provider` alanı serbestti. İstemci `claude_cli` ya da `codex` seçip kullanıcının
   aboneliğini (ADR-0012, ADR-0017) harcatabiliyordu. Bu sağlayıcılar yapılandırmada etkin
   olmasa bile kurulabiliyordu.
4. Kimlik alanlarında ve gövde boyutunda sınır yoktu. Eşzamanlı analiz sayısı sınırsızdı.
   Mimari §12 ise "API hız sınırlama" diyordu, yani gerçeği yansıtmıyordu.

## Karar

1. **İstek Tier 1'i yalnız kapatabilir:** etkin değer `settings.tier1_enabled and tier1 is not
   False`. Yerel CLI kullanıcısı kendi yapılandırmasının sahibi olduğundan `--tier1` ayarı
   açabilir. Bu yapılandırma düzeyinde yapılır, istekle değil.
2. **Host doğrulaması:** loopback adları (`127.0.0.1`, `localhost`, `[::1]`) her zaman
   kabul edilir. Ek adlar `api.allowed_hosts` ile verilir; `*` denetimi kapatır. Planda
   Starlette `TrustedHostMiddleware` geçiyordu. Onun yerine aynı denetimi yapan küçük bir saf
   ASGI ara katmanı (`api/guard.py`) yazıldı, çünkü Starlette düz metin `400` döndürüyor.
   Mimari §9 ise tüm hataları problem+json ister.
3. **Sağlayıcı izin listesi:** `api.allowed_providers`; boşsa `providers.default` +
   `fallback`. Dışındaki ad `422` alır ve sağlayıcı hiç kurulmaz. Liste yalnız API'de
   uygulanır; CLI ve masaüstü yerel kullanıcının kendi seçimidir.
4. **Girdi sınırları:**
   - `question_id`/`session_id`/`provider` ≤ 128 karakter ve `^[A-Za-z0-9_.-]+$`. Bu modelde
     tanımlıdır, yani tüm istemcilerde geçerlidir.
   - Kod `limits.max_bytes` × 4 karakteri aşarsa normalizasyona girmeden `413` alır. Bu kaba ön
     sınırdır; asıl bayt/satır sınırı K0'da kalır.
   - Gövde `api.max_body_bytes`'ı (1 MiB) aşarsa `413` alır. `Content-Length` varsa gövde hiç
     okunmaz; yoksa (chunked) okuma sınırda kesilir.
5. **Eşzamanlılık:** `api.max_concurrent_analyses` (4). Yuva dolunca `503` döner. Reddedilen
   istek yuva tutmaz. SSE yuvası akış bitince bırakılır; bağlantı akış başlamadan koparsa
   arka plan görevi yedek olarak bırakır.
6. İstek/dakika hız sınırı **eklenmedi**; tek kullanıcılı yerel araç için eşzamanlılık sınırı
   yeterli. Mimari §12 buna göre düzeltildi. `serve` uyarısı artık API anahtarı ve Host listesi
   durumunu söylüyor.

## Sonuçlar

- **Faz 62 notu (denetim L6):** `DELETE /v1/analyses/{id}` yıkıcı bir uçtur. API anahtarı
  tanımlıysa korunur (`tests/api/test_api_auth.py::test_delete_without_key_rejected_and_record_kept`);
  tanımlı değilse yerel makinedeki her istemci kayıt silebilir. Paylaşılan sunucuda anahtar
  zorunlu tutulmalı.

- Tarayıcıdaki bir sayfa ya da ağdaki bir istemci Tier 1'i açamaz, abonelik sağlayıcısı
  seçemez, devasa gövdeyle belleği dolduramaz.
- Dışa açık sunucuda (`--host 0.0.0.0`) `api.allowed_hosts` doldurulmadıkça uzak istekler
  `400` alır. Güvenli varsayılan budur ve `serve` bunu uyarıda söyler.
- API testleri `http://127.0.0.1` taban adresini kullanır.
- Gövde sınırı için gövde bellekte tamponlanır (≤ 1 MiB); akışlı gövde gerektiren bir uç nokta
  yok.
