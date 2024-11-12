from __future__ import annotations

import uuid
from datetime import datetime
from dataclasses import field, dataclass, fields
from typing import Tuple

from src.db.exceptions import RecordDoesNotExist
from src.db.manager.shortcuts import check_record, update_record


@dataclass(kw_only=True)
class BaseModel:
    __tablename__ = None

    id: 'uuid.UUID' = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_deleted: bool = False

    def save(self) -> None:
        if not check_record(model=self, pk=str(self.id)):
            raise RecordDoesNotExist

        update_record(self)


    @classmethod
    def get_fields(cls) -> Tuple[str, ...]:
        return tuple([field.name for field in fields(cls)])
