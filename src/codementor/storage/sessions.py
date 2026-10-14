"""İpucu merdiveni oturumları (mimari §5.4.3, §11): aynı `session_id` + `question_id` ile
her yeni gönderim deneme sayısını 1 artırır; ipucu seviyesi `mentoring_profile`'dan gelir.

Faz 49: deneme analiz başında tek SQL ifadesiyle ayrılır (`INSERT … ON CONFLICT DO UPDATE …
RETURNING`); eşzamanlı iki gönderim farklı deneme alır. İptal/hata ayrılan denemeyi geri verir
(arada başka ayırma olmadıysa), böylece yarıda kalan analiz merdiveni ilerletmez (Faz 19).

Faz 61 (ADR-0026): Yalnız sayılan denemeler (bozulmamış ve erken çıkış olmayan) merdiveni ilerletir;
sayılmayan denemelerde ayrılan sayaç `release_attempt` ile geri verilir.
"""

from __future__ import annotations

from sqlalchemy import Table, update
from sqlalchemy.dialects.sqlite import insert
from sqlmodel import col, delete

from codementor.storage.db import Database, SessionRow, utcnow

FREE_MODE_QUESTION = ""  # soru bağlamı yoksa (serbest mod) oturum yine sayılır


def _table() -> Table:
    # SQLModel `__table__`'ı sınıf düzeyinde tiplemez; Core ifadeleri (upsert) tabloyu ister
    return SessionRow.__table__  # type: ignore[attr-defined, no-any-return]


def _key(session_id: str, question_id: str | None) -> tuple[str, str]:
    return session_id, question_id or FREE_MODE_QUESTION


def next_attempt(db: Database, session_id: str | None, question_id: str | None) -> int:
    """Sıradaki gönderimin kaçıncı deneme olacağı (salt okuma); oturum yoksa her zaman 1."""
    if not session_id:
        return 1
    with db.session() as session:
        row = session.get(SessionRow, _key(session_id, question_id))
    return (row.attempt_count if row else 0) + 1


def reserve_attempt(db: Database, session_id: str | None, question_id: str | None) -> int:
    """Bu gönderimin denemesini atomik olarak ayırır ve döndürür; oturum yoksa 1."""
    if not session_id:
        return 1
    sid, qid = _key(session_id, question_id)
    now = utcnow()
    table = _table()
    statement = (
        insert(table)
        .values(session_id=sid, question_id=qid, attempt_count=1, updated_at=now)
        .on_conflict_do_update(
            index_elements=["session_id", "question_id"],
            set_={"attempt_count": table.c.attempt_count + 1, "updated_at": now},
        )
        .returning(table.c.attempt_count)
    )
    with db.session() as session:
        attempt = int(session.execute(statement).scalar_one())
        session.commit()
    return attempt


def release_attempt(
    db: Database, session_id: str | None, question_id: str | None, attempt: int
) -> None:
    """Ayrılan denemeyi geri verir; yalnız sayaç hâlâ bu denemedeyse (sonraki ayırmayı bozmaz)."""
    if not session_id:
        return
    sid, qid = _key(session_id, question_id)
    table = _table()
    statement = (
        update(table)
        .where(
            table.c.session_id == sid,
            table.c.question_id == qid,
            table.c.attempt_count == attempt,
        )
        .values(attempt_count=attempt - 1)
    )
    with db.session() as session:
        session.execute(statement)
        session.commit()


def record_attempt(
    db: Database, session_id: str | None, question_id: str | None, *, attempt: int, hint_level: int
) -> None:
    """Tamamlanan gönderimin ipucu seviyesini yazar (oturum yoksa bir şey yapmaz). Sayaç
    `reserve_attempt`'te artar; burada yalnız geriye düşmemesi sağlanır (`max`)."""
    if not session_id:
        return
    key = _key(session_id, question_id)
    with db.session() as session:
        row = session.get(SessionRow, key) or SessionRow(session_id=key[0], question_id=key[1])
        row.attempt_count = max(row.attempt_count, attempt)
        # eşzamanlı gönderimlerde geç biten erken deneme seviyeyi geri çekmesin
        row.current_hint_level = max(row.current_hint_level, hint_level)
        row.updated_at = utcnow()
        session.add(row)
        session.commit()


def clear_sessions(db: Database) -> int:
    """Tüm oturum kayıtlarını siler (Faz 62); silinen oturum sayısını döner."""
    with db.session() as session:
        result = session.exec(delete(SessionRow))
        session.commit()
        return int(result.rowcount)


def delete_session(db: Database, session_id: str) -> bool:
    """Belirli bir oturumun tüm satırlarını siler (Faz E); silinen satır varsa True."""
    with db.session() as session:
        result = session.exec(delete(SessionRow).where(col(SessionRow.session_id) == session_id))
        session.commit()
        return bool(result.rowcount > 0)


def prune_old_sessions(db: Database, days: int) -> int:
    """Belirli günden eski oturumları siler (Faz F, D19); silinen satır sayısını döner."""
    from datetime import timedelta

    cutoff = utcnow() - timedelta(days=days)
    with db.session() as session:
        result = session.exec(delete(SessionRow).where(col(SessionRow.updated_at) < cutoff))
        session.commit()
        return int(result.rowcount)
