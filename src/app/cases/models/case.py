from __future__ import annotations

from dataclasses import dataclass

from src.db.models import BaseModel


@dataclass(frozen=True)
class Case(BaseModel):
    __tablename__ = "cases"

    id: int
    name: str
    image: str
