# ADR-0008: Model adları yalnızca yapılandırmada

**Tarih:** 2026-09-30 (geriye dönük kayıt; Faz 0/7'de uygulandı) · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.5, §17; AGENTS.md altın kural 5

## Bağlam

Sağlayıcıların model adları sık değişir, bazıları kullanımdan kalkar. Koda gömülen bir model adı
hem kodu bayatlatır hem de testlerin gerçek bir modele bağımlı olmasına yol açar. API anahtarları
ve URL'ler için de aynı risk geçerlidir.

## Karar

Model adları, API anahtarı ortam değişkeni adları ve temel URL'ler yalnızca yapılandırmadan
gelir (`codementor.toml` → ortam değişkeni → CLI bayrağı; `src/codementor/config.py`). Kodda
varsayılan model adı yoktur; model boşsa sağlayıcı açık bir yapılandırma hatası verir.
Testler `FakeProvider` kullanır ve ağa çıkmaz; gerçek API testleri `@pytest.mark.live`.

## Sonuçlar

- Model değiştirmek kod değişikliği gerektirmez; eval sonuç dosyaları hangi modelle
  ölçüldüğünü kaydeder (`config.model`).
- Varsayılan yapılandırma (`codementor.toml`) `claude_cli` + `claude-opus-5-5` ile gelir
  (Faz 13); Faz 12 eval'i bu modelle ölçüldü.
