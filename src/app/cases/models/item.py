from __future__ import annotations

from dataclasses import dataclass

from src.db.models import BaseModel


@dataclass(frozen=True)
class Item(BaseModel):
    __tablename__ = "items"

    id: int
    name: str
    rarity: int
    image: str
