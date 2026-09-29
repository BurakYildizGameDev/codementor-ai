---
description: UYGULAMA_PLANI.md'deki bir fazı standart protokolle uygular
argument-hint: <faz-numarası>
---
Faz $ARGUMENTS üzerinde çalışacağız.

1. @docs/UYGULAMA_PLANI.md içinde "### Faz $ARGUMENTS " ile başlayan bölümü oku.
2. O bölümün atıf yaptığı @docs/mimari.md kısımlarını oku.
3. @PROGRESS.md'yi oku; önceki fazlardan kalan açık soruları not et.
4. Kod yazmadan önce şunları içeren bir plan sun:
   - oluşturulacak/değiştirilecek dosyalar
   - yazılacak testler (dosya ve test adlarıyla)
   - mimariyle çelişen veya belirsiz noktalar
   - kabul kriterlerinin nasıl doğrulanacağı
5. Onayımı bekle.
6. Onaydan sonra önce testleri, sonra uygulamayı yaz (mümkünse TDD).
7. make check çalıştır; yeşil olana kadar düzelt.
8. Kabul kriterlerini tek tek [x] ile raporla, PROGRESS.md'yi güncelle,
   commit mesajı öner. Commit'i ben atacağım.
