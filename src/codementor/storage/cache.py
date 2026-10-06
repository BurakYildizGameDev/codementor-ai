"""Rapor önbelleği (mimari §11).

Anahtar: sha256(normalized_code | language | engine | question_id | hint_level | provider |
model | prompt_version | rules_version | schema_version | pipeline). Bozulmuş (degraded)
raporlar önbellekten dönmez: geçici sağlayıcı hatası kalıcı olmasın. Faz 49: bugünkü şemaya
uymayan eski `report_json` yok sayılır (geçmiş/GET çökmez); `max_analyses` üstü en eskiler budanır.
"""

from __future__ import annotations

import hashlib

from sqlmodel import col, delete, select

from codementor.log import get_logger
from codementor.models.report import AnalysisReport
from codementor.storage.db import AnalysisRow, Database

log = get_logger("codementor.storage")

_SEPARATOR = "\x1f"  # alan ayırıcı: kodda geçse bile uzunluk öneki çakışmayı önler


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
    pipeline ayarları (mod, doğrulama geçişi; Faz 35), ör. `"two_pass+verify"`."""
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


def save_analysis(
    db: Database,
    report: AnalysisReport,
    *,
    key: str,
    session_id: str | None,
    latency_ms: int,
    max_analyses: int | None = None,
) -> None:
    """Raporu `analyses` tablosuna yazar (önbellek isabetleri de iz için kaydedilir);
    `max_analyses` verilirse en yeni o kadar kayıt kalır."""
    row = AnalysisRow(
        id=report.analysis_id,
        created_at=report.created_at,
        cache_key=key,
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
