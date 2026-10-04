"""Uygulama durumu: ayarlar, veritabanı, soru bankası, istek başına orkestratör."""

from __future__ import annotations

from dataclasses import dataclass, field

from codementor.api.guard import AnalysisSlots
from codementor.config import Settings
from codementor.pipeline.events import EventBus
from codementor.pipeline.orchestrator import Orchestrator, ProviderFactory
from codementor.questions.bank import QuestionBank
from codementor.storage.db import Database


@dataclass
class ApiState:
    """`app.state.codementor`; veritabanı ve soru bankası ilk kullanımda açılır."""

    settings: Settings
    db: Database | None = None
    provider_factory: ProviderFactory | None = None
    _bank: QuestionBank | None = field(default=None, repr=False)
    slots: AnalysisSlots = field(init=False)

    def __post_init__(self) -> None:
        self.slots = AnalysisSlots(self.settings.api.max_concurrent_analyses)

    def database(self) -> Database:
        if self.db is None:
            self.db = Database.from_settings(self.settings)
        return self.db

    def questions(self) -> QuestionBank:
        if self._bank is None:
            self._bank = QuestionBank.load(self.settings.data.questions_dir)
        return self._bank

    def orchestrator(self, bus: EventBus | None = None) -> Orchestrator:
        """İstek başına orkestratör: her istek kendi olay yolunu kullanır (SSE karışmaz)."""
        return Orchestrator(
            self.settings,
            self.database(),
            provider_factory=self.provider_factory,
            bus=bus or EventBus(),
        )

    def close(self) -> None:
        if self.db is not None:
            self.db.close()
