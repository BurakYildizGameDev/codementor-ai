"""Kullanım toplamları (Geçmiş ekranı, Faz K; katman: `models`).

Faz G6 (denetimden ertelenenler): `UsageTotals` daha önce `storage.cache` içinde tanımlıydı ve
`report.usage` onu oradan içe aktarıyordu; rapor katmanı veritabanı katmanına bağlı kalıyordu.
Veri sözleşmesi olduğu için buraya taşındı.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UsageTotals:
    """Kayıtlı analizlerin toplam kullanımı (Geçmiş ekranı, Faz K). Önbellek isabetleri 0 token
    ve maliyetsiz kaydedilir: toplam gerçekten harcananı gösterir."""

    analyses: int
    tokens_in: int
    tokens_out: int
    cost: float | None  # hiçbir kayıtta fiyat yoksa None
