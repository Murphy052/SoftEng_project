from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from src.db.models import BaseModel
from src.app.cases.models.item import Item


@dataclass(frozen=True)
class CaseWithItems(BaseModel):
    id: int
    name: str
    image: str
    items: List[Item]
