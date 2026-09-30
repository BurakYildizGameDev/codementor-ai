# ADR-0005: v1'de kullanıcı kodu çalıştırılmaz

**Tarih:** 2026-09-30 (geriye dönük kayıt) · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §1.4, §5.2, §12, §22

## Bağlam

Karmaşıklığı ve doğruluğu ölçmenin en güçlü yolu kodu farklı girdilerle çalıştırmaktır. Ancak
kullanıcı kodu güvenilmeyen veridir (§12): çalıştırmak dosya sistemi, ağ ve süreç yalıtımı
gerektirir ve kurulum eşiğini yükseltir.

## Karar

v1'de kod çalıştırılmaz. Derleyici yalnızca `-fsyntax-only` / sözdizimi ayrıştırması için
kullanılır; ikili dosya üretilmez (ADR-0009). Big-O statik ipucu ve LLM gerekçesiyle
belirlenir.

## Sonuçlar

- Güvenlik yüzeyi derleyicinin kaynak okuma davranışıyla sınırlı kalır (include koruması,
  süreç sınırları; ADR-0009, ADR-0010).
- Big-O bir tahmindir, ölçülmüş çalışma süresi değildir; README "Sınırlamalar"da belirtilir.
- Ampirik karmaşıklık ve test senaryosu tabanlı doğruluk v2.0'a bırakıldı (§22); o zaman bu ADR
  ve ADR-0009 yeniden değerlendirilir.
