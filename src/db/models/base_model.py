from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, fields
from typing import Tuple


@dataclass(frozen=True)
class BaseModel(ABC):
    __tablename__ = None

    id: str
    # created_at: datetime = field(default_factory=datetime.now)
    # updated_at: datetime = field(default_factory=datetime.now)
    # is_deleted: bool = False


    @classmethod
    def get_fields(cls) -> Tuple[str, ...]:
        return tuple([field.name for field in fields(cls)])
