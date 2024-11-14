from __future__ import annotations

import traceback
import uuid
from dataclasses import fields
from typing import Type, TYPE_CHECKING, Union, Optional

from pypika.queries import Query, QueryBuilder, Table
from pypika.terms import PseudoColumn

from src.db import get_db_cursor, get_db

if TYPE_CHECKING:
    from src.db.models import BaseModel
    from src.db.database import Database

type PrimaryKey = Union[str, uuid.UUID]


def create_record_from_model(
        model: BaseModel,
        db: Database = get_db(),
) -> None:

    model_fields = fields(model)
    column_names = [field.name for field in model_fields if field.default is not None]
    column_values = [getattr(model, field.name) for field in model_fields if field.default is not None]

    q: QueryBuilder = (
        Query.into(model.__tablename__)
        .columns(*column_names)
        .insert(*column_values)
    )

    table_fields: str = ', '.join(model.get_fields())
    query: str = q.get_sql() + f" RETURNING {table_fields};"

    with get_db_cursor(db) as cur:
        cur.execute(query)
        result = cur.fetchone()


def update_record_from_model(
        model: BaseModel,
        db: Database = get_db(),
) -> None:

    table: Table = Table(model.__tablename__)
    q: QueryBuilder = Query.update(table)

    for field, value in model.__dict__.items():
        q = q.set(field, value)

    q = q.where(table.id == model.id)

    query: str = q.get_sql()

    with get_db_cursor(db) as cur:
        cur.execute(query)


def get_obj_or_none(
        model: Type[BaseModel],
        pk: Optional[PrimaryKey],
        db: Database = get_db(),
        **kwargs,
) -> Optional[BaseModel]:

    q: QueryBuilder = (
        Query.from_(model.__tablename__)
        .select(*model.get_fields())
    )

    if pk is not None and "id" not in kwargs.keys():
        q = q.where(PseudoColumn("id") == str(pk))
    else:
        raise Exception("Cannot contain both pk and id parameters")

    for key, value in kwargs.items():
        q = q.where(PseudoColumn(key) == value)

    query = q.get_sql()

    with get_db_cursor(db) as cur:
        cur.execute(query)
        fetched_data: list = cur.fetchone()

    if not fetched_data:
        return None

    return model(*fetched_data)


def check_record(
        model: Union[BaseModel, Type[BaseModel]],
        pk: PrimaryKey,
        db: Database = get_db(),
) -> bool:

    query: str = f"""SELECT 1 FROM {model.__tablename__} WHERE id = ? LIMIT 1;"""
    with get_db_cursor(db) as cur:
        cur.execute(query, (str(pk),))
        return cur.fetchone() is not None
