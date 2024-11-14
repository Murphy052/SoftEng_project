from __future__ import annotations

import uuid
from abc import ABC
from datetime import datetime
from dataclasses import field, dataclass, fields
from typing import Tuple

from src.db.exceptions import RecordDoesNotExist
from src.db.manager.shortcuts import check_record, update_record_from_model


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
