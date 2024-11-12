from __future__ import annotations

from abc import ABC
from typing import List, Type, TYPE_CHECKING, Tuple

from pypika import Table
from pypika.queries import QueryBuilder, Query
from pypika.terms import PseudoColumn

from src.db import get_db_cursor
from src.db.exceptions import RecordDoesNotExist
from src.db.models import BaseModel


class BaseManager(ABC):
    def __init__(self, model: Type[BaseModel]):
        self._model: type(BaseModel) = model
        self.table: Table = Table(model.__tablename__)
        self._fields: Tuple[str, ...] = model.get_fields()

    def _validate_fields(self, **kwargs):
        for field in kwargs.keys():
            if field not in self._fields:
                raise Exception("Invalid arguments for model")

    def get_by_id(self, pk) -> BaseModel:
        q: QueryBuilder = (
            Query.from_(self.table)
            .select(*self._fields)
            .where(self.table.id == pk)
        )
        query = q.get_sql()

        with get_db_cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()

        if not result:
            raise RecordDoesNotExist

        obj = self._model(*result)
        return obj

    def get_all(self) -> List[BaseModel]:
        q: QueryBuilder = (
            Query.from_(self.table)
            .select(*self._fields)
        )
        query = q.get_sql()

        with get_db_cursor() as cur:
            cur.execute(query)
            raw_data = cur.fetchall()

        if not raw_data:
            raise Exception("No record found")

        result: List[BaseModel] = list(map(lambda row: self._model(*row), raw_data))
        return result

    def update(self, pk: str, **kwargs) -> BaseModel:
        q: QueryBuilder = Query.update(self.table)

        self._validate_fields(**kwargs)
        for field, value in kwargs.items():
            q = q.set(field, value)

        q = q.where(self.table.id == pk)

        table_fields: str = ', '.join(self._fields)
        query: str = q.get_sql() + f" RETURNING {table_fields}"

        with get_db_cursor() as cur:
            cur.execute(query)
            result = self._model(*(cur.fetchone()))

        return result

    def delete(self, pk: str) -> None:
        q: QueryBuilder = (
            Query.from_(self.table)
            .delete()
            .where(self.table.id == pk)
        )
        query: str = q.get_sql()

        with get_db_cursor() as cur:
            cur.execute(query)
