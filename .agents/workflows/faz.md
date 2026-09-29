---
description: UYGULAMA_PLANI.md'deki bir fazı standart protokolle uygular
---
1. Kullanıcının belirttiği faz numarasını al. Belirtilmemişse PROGRESS.md'deki
   ilk tamamlanmamış fazı kullan ve bunu kullanıcıya söyle.
2. docs/UYGULAMA_PLANI.md içinde "### Faz <N> " bölümünü ve atıf yaptığı
   docs/mimari.md kısımlarını oku.
3. PROGRESS.md'yi oku.
4. Uygulama planı üret: dosyalar, testler, riskler, kabul kriterlerinin doğrulama yolu.
5. Kullanıcı onayını bekle.
6. Önce testleri, sonra uygulamayı yaz.
7. make check çalıştır; yeşil olana kadar düzelt.
8. Kabul kriterlerini raporla, PROGRESS.md'yi güncelle, commit mesajı öner.
