import traceback
from dataclasses import fields
from typing import Type, TYPE_CHECKING, Union, Optional

from pypika.queries import Query, QueryBuilder, Table
from pypika.terms import PseudoColumn

from src.db import get_db_cursor

if TYPE_CHECKING:
    from src.db.models import BaseModel


def create_record(model: BaseModel) -> None:
    model_fields = fields(model)
    column_names = [field.name for field in model_fields if field.default is not None]
    column_values = [getattr(model, field.name) for field in model_fields if field.default is not None]

    q: QueryBuilder = (
        Query.into(model.__tablename__)
        .columns(*column_names)
        .insert(*column_values)
    )
    query = q.get_sql()

    with get_db_cursor() as cur:
        try:
            cur.execute(query)
        except:
            traceback.print_exc()


def update_record(model: BaseModel) -> None:
    table: Table = Table(model.__tablename__)
    q: QueryBuilder = Query.update(table)

    for field, value in model.__dict__.items():
        q = q.set(field, value)

    q = q.where(table.id == model.id)

    query: str = q.get_sql()

    with get_db_cursor() as cur:
        cur.execute(query)


def get_obj_or_none(model: Type[BaseModel], **kwargs) -> Optional[BaseModel]:
    q: QueryBuilder = (
        Query.from_(model.__tablename__)
        .select(*model.get_fields())
    )
    for key, value in kwargs.items():
        q = q.where(PseudoColumn(key) == value)

    query = q.get_sql()

    with get_db_cursor() as cur:
        cur.execute(query)
        fetched_data: list = cur.fetchone()

    if not fetched_data:
        return None

    return model(*fetched_data)


def check_record(model: Union[BaseModel, Type[BaseModel]], pk: str) -> bool:
    query: str = f"""SELECT 1 FROM "{model.__tablename__}" WHERE id = %s"""

    with get_db_cursor() as cur:
        try:
            cur.execute(query, (pk,))
            result = cur.fetchone()
            return result is not None
        except:
            traceback.print_exc()
            return False
