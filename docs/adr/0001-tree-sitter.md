# ADR-0001: Temel ayrıştırıcı olarak tree-sitter

**Tarih:** 2026-09-30 (geriye dönük kayıt; karar Faz 0–3'te uygulandı) · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.2.1, §5.3, §19

## Bağlam

Sistem C, C++ ve C# kodunu (Unity/Unreal dahil) LLM'e göndermeden önce denetlemeli ve
kanıt üretmeli: sözdizimi hataları, döngü yapısı, çağrılar, bellek ayırma. Öğrenci kodu sık sık
yarım ya da hatalıdır ve çoğu makinede derleyici kurulu değildir. Seçenekler: her dil için ayrı
ayrıştırıcı (libclang yalnızca C/C++, Roslyn yalnızca C#), düzenli ifadeler ya da tree-sitter.

## Karar

Tier 0 ve statik olgu çıkarımı (K2) tree-sitter ile yapılır (`tree-sitter-c`, `-cpp`,
`-c-sharp`). Sözdizimi hataları `ERROR`/`MISSING` düğümlerinden, olgular sorgu dosyalarından
(`src/codementor/analysis/queries/`) çıkarılır. Derleyici (Tier 1) yalnızca isteğe bağlı ek
denetimdir (ADR-0009).

## Sonuçlar

- Tek API ile üç dil; hataya dayanıklı ayrıştırma sayesinde yarım koddan da olgu çıkar.
- Derleyici kurmadan çalışır; Tier 0 her zaman koşar ve erken çıkış kararını verir
  (Faz 12 eval'inde erken çıkış precision/recall %100).
- Tür bilgisi yoktur: çağrı maliyetleri ad tabanlı bir tabloyla tahmin edilir
  (`data/call_costs.yaml`); tabloda olmayan çağrılar kör noktadır (PROGRESS "Sonraya").
