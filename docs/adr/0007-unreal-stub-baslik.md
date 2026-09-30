# ADR-0007: Unreal için stub başlık + uyarı seviyesine düşürme

**Tarih:** 2026-09-30 (geriye dönük kayıt; Faz 4'te uygulandı) · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.2.2, §5.2.4

## Bağlam

Unreal C++ kodu `UCLASS`, `UPROPERTY`, `GENERATED_BODY`, `AActor`, `TArray` gibi motor
makro ve türlerine dayanır. Motor başlıkları olmadan (onlarca GB, lisans) kod derlenemez;
derleyici her motor türü için hata verir ve bu hatalar gerçek hatalarla karışır.

## Karar

Tier 1'de Unreal kodu `clang++ -include data/stubs/ue_stubs.h -fsyntax-only` ile denetlenir.
Stub başlık yaygın makroları ve türleri boş tanımlarla sağlar. Stub kaynaklı ya da bilinmeyen
motor türü hataları `WARNING` seviyesine düşürülür; erken çıkışı yalnızca Tier 0'ın yapısal
sözdizimi hataları tetikler.

## Sonuçlar

- Unreal kodunda yapısal hatalar yakalanır, motor API'sinin yanlış kullanımı yakalanmaz.
- Stub kapsamı sınırlıdır; eksik tanımlar uyarı gürültüsü üretir (PROGRESS "Sonraya":
  `ue_stubs.h` genişletme).
- Windows'ta clang varsayılan olarak MSVC hedeflediği için stub denetimi atlanabilir
  (CI Windows işinde derleyici testleri kapalı; PROGRESS "Sonraya").
- README "Sınırlamalar"da "Unreal yalnızca stub derleme" olarak belirtilir.
