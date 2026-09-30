"""İpucu merdiveni oturumları (mimari §5.4.3, §11): aynı `session_id` + `question_id` ile
her yeni gönderim deneme sayısını 1 artırır; ipucu seviyesi `mentoring_profile`'dan gelir."""

from __future__ import annotations

from codementor.storage.db import Database, SessionRow, utcnow

FREE_MODE_QUESTION = ""  # soru bağlamı yoksa (serbest mod) oturum yine sayılır


def next_attempt(db: Database, session_id: str | None, question_id: str | None) -> int:
    """Bu gönderimin kaçıncı deneme olacağı; oturum yoksa her zaman 1."""
    if not session_id:
        return 1
    with db.session() as session:
        row = session.get(SessionRow, (session_id, question_id or FREE_MODE_QUESTION))
    return (row.attempt_count if row else 0) + 1


def record_attempt(
    db: Database, session_id: str | None, question_id: str | None, *, attempt: int, hint_level: int
) -> None:
    """Gönderimi kaydeder (oturum yoksa bir şey yapmaz)."""
    if not session_id:
        return
    key = (session_id, question_id or FREE_MODE_QUESTION)
    with db.session() as session:
        row = session.get(SessionRow, key) or SessionRow(session_id=key[0], question_id=key[1])
        row.attempt_count = max(row.attempt_count, attempt)
        row.current_hint_level = hint_level
        row.updated_at = utcnow()
        session.add(row)
        session.commit()
