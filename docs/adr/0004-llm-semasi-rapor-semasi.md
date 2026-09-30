# ADR-0004: LLM şeması ≠ rapor şeması

**Tarih:** 2026-09-30 (geriye dönük kayıt; Faz 1'de uygulandı) · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §6.1, §6.3, §6.4

## Bağlam

Kullanıcıya dönen rapor (`AnalysisReport`) derleme durumu, bulgu kaynağı, güven skoru, sürümler
ve süre gibi sistemin bildiği alanları içerir. Bu şema LLM'e verilirse model bu alanları da
doldurmaya çalışır; uydurulan her alan doğrulanması gereken bir iddia olur.

## Karar

İki ayrı şema: LLM'e yalnızca küçük, düz çıktı modelleri verilir (`LLMAnalysisOutput`,
`LLMSocraticOutput`, `LLMSinglePassOutput`). `compilation`, `meta`, `source`, `confidence`,
`analysis_id` gibi alanları sistem doldurur. Rapor, doğrulanmış LLM çıktısı ile statik sonuçların
birleştirilmesiyle kurulur. Şemalar `schemas/` altına dışa aktarılır (`make schema`); Web UI
tipleri de bunlardan üretilir (Faz 13).

## Sonuçlar

- Modelin uydurabileceği alan sayısı azalır; `test_llm_schema_excludes_system_fields` bu ayrımı
  korur.
- Faz 12'de şema geçerliliği onarım sonrası %100 (yalnızca claude_cli ölçüldü).
- İki model kümesinin birbirinden sapmaması birleştirme koduyla (`verify/merge.py`) ve
  sözleşme testleriyle sağlanır.
