from __future__ import annotations

import uuid
from abc import ABC
from typing import List, Type, TYPE_CHECKING, Tuple, TypeVar, Generic, Union

from pypika import Table
from pypika.queries import QueryBuilder, Query
from pypika.terms import PseudoColumn

from src.db import get_db_cursor, get_db
from src.db.exceptions import RecordDoesNotExist
from src.db.models import BaseModel

if TYPE_CHECKING:
    from src.db.database import Database


Model = TypeVar("Model", bound=BaseModel)
type PrimaryKey = Union[str, uuid.UUID]


class BaseManager(ABC, Generic[Model]):

    def __init__(
            self,
            model: Type[Model]
    ) -> None:
        self._model: Type[Model] = model
        self.table: Table = Table(model.__tablename__)
        self._fields: Tuple[str, ...] = model.get_fields()

    def _validate_fields(
            self,
            **kwargs
    ) -> None:
        for field in kwargs.keys():
            if field not in self._fields:
                raise Exception("Invalid arguments for model")

    def get_by_id(
            self,
            pk: PrimaryKey,
            db: Database = get_db(),
    ) -> Model:
        q: QueryBuilder = (
            Query.from_(self.table)
            .select(*self._fields)
            .where(self.table.id == str(pk))
        )
        query = q.get_sql()

        with get_db_cursor(db) as cur:
            cur.execute(query)
            result = cur.fetchone()

        if not result:
            raise RecordDoesNotExist

        obj: Model = self._model(*result)
        return obj

    def get_all(
            self,
            db: Database = get_db(),
    ) -> List[Model]:
        q: QueryBuilder = (
            Query.from_(self.table)
            .select(*self._fields)
        )
        query = q.get_sql()

        with get_db_cursor(db) as cur:
            cur.execute(query)
            raw_data = cur.fetchall()

        if not raw_data:
            raise Exception("No record found")

        result: List[Model] = list(map(lambda row: self._model(*row), raw_data))
        return result

    def update(
            self,
            pk: PrimaryKey,
            db: Database = get_db(),
            **kwargs,
    ) -> Model:
        q: QueryBuilder = Query.update(self.table)

        self._validate_fields(**kwargs)
        for field, value in kwargs.items():
            q = q.set(field, value)

        q = q.where(self.table.id == str(pk))

        table_fields: str = ', '.join(self._fields)
        query: str = q.get_sql() + f" RETURNING {table_fields}"

        with get_db_cursor(db) as cur:
            cur.execute(query)
            result = self._model(*(cur.fetchone()))

        return result

    def delete(
            self,
            pk: PrimaryKey,
            db: Database = get_db(),
    ) -> None:
        q: QueryBuilder = (
            Query.from_(self.table)
            .delete()
            .where(self.table.id == str(pk))
        )
        query: str = q.get_sql()

        with get_db_cursor(db) as cur:
            cur.execute(query)
