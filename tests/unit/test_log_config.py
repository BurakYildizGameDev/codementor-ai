"""Faz 31: log yapılandırması anlık görüntüsü; `captured_logs` önceki ayarı geri yükler."""

from __future__ import annotations

import io
import logging

from codementor.log import configure_logging, logging_snapshot, restore_logging


def test_snapshot_restores_previous_configuration() -> None:
    before = logging_snapshot()
    custom = io.StringIO()
    try:
        configure_logging(custom, json=False, level=logging.INFO)
        snapshot = logging_snapshot()
        configure_logging(io.StringIO(), json=True, level=logging.DEBUG)
        restore_logging(snapshot)
        assert logging_snapshot() == snapshot
        assert snapshot.stream is custom
        assert snapshot.level == logging.INFO
        assert snapshot.json is False
    finally:
        restore_logging(before)
    assert logging_snapshot() == before
