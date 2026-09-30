# ADR-0002: Hibrit analiz — statik kanıt + LLM açıklama

**Tarih:** 2026-09-30 (geriye dönük kayıt) · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §1.2, §2, §5.3, §5.6

## Bağlam

Yalnızca LLM ile kod denetimi satır numarası ve Big-O uydurabilir, sonuçları tekrarlanamaz
ve ölçülemez. Yalnızca statik analiz ise deterministik ama dar kapsamlıdır ve öğrenciye
açıklama/soru üretemez.

## Karar

Deterministik araçlar (tree-sitter, derleyici, kural motoru) **kanıt** üretir; LLM bu kanıtı
açıklar, eksikleri tamamlar ve Sokratik sorular üretir. LLM iddiaları doğrulanır (K5): satır
numarası o satırdaki kanıt metniyle eşleşmeli, Big-O kanonik biçime ayrışmalı ve statik ipucuyla
karşılaştırılmalı. LLM yanıt vermezse rapor yalnızca statik çıktıyla döner (`meta.degraded`).

## Sonuçlar

- LLM'siz bir taban çizgisi ("yalnızca statik") her zaman vardır ve eval'de ölçülür.
- Faz 12 (test, 49 örnek): statik kurallar precision %100 / recall %42; LLM ile recall %92–94,
  precision %27–32. Statik olgular prompt'tan çıkarılınca Big-O birebir doğruluk dev'de %96 → %85.
- Kanıt doğrulaması halüsinasyonu tamamen engellemez; yalnızca kanıtı olmayan satır iddialarını
  eler. İçerik doğruluğu eval ile ölçülür.
