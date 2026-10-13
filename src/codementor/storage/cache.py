"""Rapor önbelleği (mimari §11).

Anahtar: sha256(normalized_code | language | engine | question_id | hint_level | provider |
model | prompt_version | rules_version | schema_version | pipeline). Bozulmuş (degraded)
raporlar önbellekten dönmez: geçici sağlayıcı hatası kalıcı olmasın. Faz 49: bugünkü şemaya
uymayan eski `report_json` yok sayılır (geçmiş/GET çökmez); `max_analyses` üstü en eskiler budanır.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from sqlalchemy import and_, case, func, or_
from sqlmodel import col, delete, select

from codementor.log import get_logger
from codementor.models.report import AnalysisReport
from codementor.storage.db import AnalysisRow, Database

log = get_logger("codementor.storage")

_SEPARATOR = "\x1f"  # alan ayırıcı: kodda geçse bile uzunluk öneki çakışmayı önler


# sha256 özeti hiçbir zaman boş değildir: bu anahtarla kaydedilen satır önbellekten dönmez
NOT_CACHEABLE = ""


def cache_key(
    *,
    normalized_code: str,
    language: str,
    engine: str,
    question_id: str | None,
    hint_level: int,
    provider: str | None,
    model: str | None,
    prompt_version: str,
    rules_version: str,
    schema_version: str,
    pipeline: str,
) -> str:
    """§11'deki alanların tamamından belirleyici anahtar. `pipeline`: çıktıyı değiştiren
    ayarların imzası (`pipeline.signature`), ör. `"two_pass+verify:<özet>"`."""
    fields = [
        normalized_code,
        language,
        engine,
        question_id or "",
        str(hint_level),
        provider or "",
        model or "",
        prompt_version,
        rules_version,
        schema_version,
        pipeline,
    ]
    digest = hashlib.sha256()
    for value in fields:
        encoded = value.encode("utf-8")
        digest.update(f"{len(encoded)}:".encode() + encoded + _SEPARATOR.encode())
    return digest.hexdigest()


def _decode(row: AnalysisRow | None) -> AnalysisReport | None:
    """Kayıtlı raporu çözer; eski/bozuk biçim None (rapor içeriği loglanmaz)."""
    if row is None:
        return None
    try:
        return AnalysisReport.model_validate_json(row.report_json)
    except ValueError:  # pydantic ValidationError ve bozuk JSON (ValueError alt sınıfı)
        log.warning("stored_report_incompatible", analysis_id=row.id)
        return None


def find_cached(db: Database, key: str) -> AnalysisReport | None:
    """Bu anahtarla kaydedilmiş en yeni bozulmamış rapor."""
    with db.session() as session:
        row = session.exec(
            select(AnalysisRow)
            .where(AnalysisRow.cache_key == key, col(AnalysisRow.degraded).is_(False))
            .order_by(col(AnalysisRow.created_at).desc())
        ).first()
    return _decode(row)


def get_analysis(db: Database, analysis_id: str) -> AnalysisReport | None:
    """Kimlikle kayıtlı rapor (API `GET /v1/analyses/{id}`)."""
    with db.session() as session:
        row = session.get(AnalysisRow, analysis_id)
    return _decode(row)


def get_row(db: Database, analysis_id: str) -> AnalysisRow | None:
    """Kimlikle ham analiz satırı (şema uyumsuzsa bile üst veri okunabilir)."""
    with db.session() as session:
        row = session.get(AnalysisRow, analysis_id)
        if row is not None:
            session.expunge(row)
        return row


def list_analyses(db: Database, limit: int = 50) -> list[AnalysisRow]:
    """En yeni kayıtlı analizler (masaüstü geçmiş ekranı); rapor gövdesi ayrıca çözülür."""
    with db.session() as session:
        rows = session.exec(
            select(AnalysisRow).order_by(col(AnalysisRow.created_at).desc()).limit(limit)
        ).all()
    return list(rows)


def list_analyses_page(
    db: Database, *, limit: int, before: str | None
) -> tuple[list[AnalysisRow], str | None]:
    """Sayfalı analiz listesi (API `GET /v1/analyses`, Faz E).

    Sıralama `created_at` azalan, eşitlikte `id` azalan. `before` verilirse o kimliğin
    satırından sonra gelenleri (daha eski olanları) döndürür; `before` bulunamazsa boş sayfa döner.
    `limit + 1` satır çekilir; fazlası varsa `next_cursor` son döndürülen satırın kimliğidir.
    """
    with db.session() as session:
        query = select(AnalysisRow).order_by(
            col(AnalysisRow.created_at).desc(), col(AnalysisRow.id).desc()
        )
        if before is not None:
            before_row = session.get(AnalysisRow, before)
            if before_row is None:
                return [], None
            query = query.where(
                or_(
                    col(AnalysisRow.created_at) < before_row.created_at,
                    and_(
                        col(AnalysisRow.created_at) == before_row.created_at,
                        col(AnalysisRow.id) < before_row.id,
                    ),
                )
            )
        rows = list(session.exec(query.limit(limit + 1)).all())
        has_more = len(rows) > limit
        items = rows[:limit]
        for r in items:
            session.expunge(r)
        next_cursor = items[-1].id if has_more and items else None
        return items, next_cursor


def save_analysis(
    db: Database,
    report: AnalysisReport,
    *,
    key: str,
    session_id: str | None,
    latency_ms: int,
    max_analyses: int | None = None,
    cacheable: bool = True,
) -> None:
    """Raporu `analyses` tablosuna yazar (önbellek isabetleri de iz için kaydedilir);
    `max_analyses` verilirse en yeni o kadar kayıt kalır. `cacheable=False` (fallback ya da
    yarım LLM sonucu, Faz B) kayıt geçmişte durur ama boş anahtarla önbellekten hiç dönmez."""
    row = AnalysisRow(
        id=report.analysis_id,
        created_at=report.created_at,
        cache_key=key if cacheable else NOT_CACHEABLE,
        language=report.language.value,
        engine=report.engine.value,
        question_id=report.question_id,
        session_id=session_id,
        provider=report.meta.provider,
        model=report.meta.model,
        early_exit=report.meta.early_exit,
        degraded=report.meta.degraded,
        tokens_in=report.meta.tokens_in,
        tokens_out=report.meta.tokens_out,
        latency_ms=latency_ms,
        report_json=report.model_dump_json(),
    )
    with db.session() as session:
        session.add(row)
        if max_analyses is not None:
            keep = (
                select(AnalysisRow.id)
                .order_by(
                    col(AnalysisRow.created_at).desc(), col(AnalysisRow.id).desc()
                )  # eşitlikte kimlikle kararlı
                .limit(max_analyses)
            )
            session.flush()
            session.exec(delete(AnalysisRow).where(col(AnalysisRow.id).not_in(keep)))
        session.commit()


def delete_analysis(db: Database, analysis_id: str) -> bool:
    """Kimlikle analizi siler (Faz 62). Bulunup silindiyse True, yoksa False döner."""
    with db.session() as session:
        row = session.get(AnalysisRow, analysis_id)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True


def clear_analyses(db: Database) -> int:
    """Tüm analiz kayıtlarını siler (Faz 62); silinen satır sayısını döner."""
    with db.session() as session:
        result = session.exec(delete(AnalysisRow))
        session.commit()
        return int(result.rowcount)


@dataclass(frozen=True)
class UsageTotals:
    """Kayıtlı analizlerin toplam kullanımı (Geçmiş ekranı, Faz K). Önbellek isabetleri 0 token
    ve maliyetsiz kaydedilir: toplam gerçekten harcananı gösterir."""

    analyses: int
    tokens_in: int
    tokens_out: int
    cost: float | None  # hiçbir kayıtta fiyat yoksa None


def usage_totals(db: Database) -> UsageTotals:
    """`analyses` tablosundaki tüm kayıtların token ve tahmini maliyet toplamı."""
    # denetim (K O-6): tek bir bozuk `report_json` tüm toplamı düşürmesin
    cost = case(
        (
            func.json_valid(AnalysisRow.report_json) == 1,
            func.json_extract(AnalysisRow.report_json, "$.meta.cost_est"),
        ),
        else_=None,
    )
    with db.session() as session:
        count, tokens_in, tokens_out, cost_sum = session.exec(
            select(
                func.count(col(AnalysisRow.id)),
                func.coalesce(func.sum(AnalysisRow.tokens_in), 0),
                func.coalesce(func.sum(AnalysisRow.tokens_out), 0),
                func.sum(cost),
            )
        ).one()
    return UsageTotals(
        analyses=int(count),
        tokens_in=int(tokens_in),
        tokens_out=int(tokens_out),
        cost=float(cost_sum) if cost_sum is not None else None,
    )
