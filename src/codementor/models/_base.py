"""Tüm modellerin ortak tabanı."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    """Bilinmeyen alanları reddeden taban model.

    LLM çıktısında uydurulmuş alanlar doğrulamada yakalanır; JSON şemasına
    `additionalProperties: false` olarak yansır (katı yapılandırılmış çıktı modları için).
    """

    model_config = ConfigDict(extra="forbid")
