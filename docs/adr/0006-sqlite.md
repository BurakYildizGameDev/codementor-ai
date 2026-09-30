# ADR-0006: Depolama için SQLite

**Tarih:** 2026-09-30 (geriye dönük kayıt; Faz 10'da uygulandı) · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §11, §19

## Bağlam

Analiz sonuçlarının önbelleği, kayıtlı raporlar (`GET /v1/analyses/{id}`, SARIF) ve ipucu
merdiveni oturumları (`session_id` + `question_id` → deneme sayısı) kalıcı tutulmalı. Hedef
kullanım tek kullanıcılı yerel araç; kurulum eşiği düşük kalmalı.

## Karar

SQLite + SQLModel (`src/codementor/storage/`). Tablolar: `analyses` (önbellek anahtarı, rapor
JSON'u, token ve süre) ve `sessions` (deneme sayısı, güncel ipucu seviyesi). Dosya yolu
`storage.db_path` → `CODEMENTOR_DB_PATH` → `~/.codementor/` sırasıyla belirlenir. Eval'de
önbellek ve veritabanı kapalıdır.

## Sonuçlar

- Sıfır kurulum, tek dosya; testler geçici veritabanı kullanır.
- Çok kullanıcılı/paylaşılan sunucu için uygun değildir (eşzamanlı yazma, kimlik yok);
  PostgreSQL v2'de değerlendirilir. API'nin senkron veritabanı çağrıları `to_thread`'e taşınabilir
  (PROGRESS "Sonraya").
