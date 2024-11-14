import sqlite3
import uuid
from dataclasses import dataclass
from uuid import uuid4

from src.db.database import SqliteDatabase
from src.db import get_db, get_db_cursor
from src.db.manager import BaseManager
from src.db.manager.shortcuts import check_record, create_record_from_model
from src.db.models import BaseModel


db = SqliteDatabase(':memory:')

@dataclass(frozen=True)
class TestModel(BaseModel):
    __tablename__ = "test_model"

    test_field: str


class TestManager(BaseManager[TestModel]):
    def __init__(self):
        super().__init__(TestModel)

_test_manager = TestManager()


def test_db_model():
    uid = uuid.uuid4()
    test_record = TestModel(uid,"test")

    assert uid == test_record.id
    assert test_record.__tablename__ == "test_model"
    assert test_record.test_field == "test"


def test_db_connection():
    db = get_db()
    conn = db.get_conn()
    cursor = db.get_cursor()

    assert isinstance(conn, sqlite3.Connection)
    assert isinstance(cursor, sqlite3.Cursor)


def test_init():
    query: str = "CREATE TABLE IF NOT EXISTS test_model (id TEXT PRIMARY KEY, test_field TEXT);"
    with get_db_cursor(get_db()) as cursor:
        cursor.execute(query, )
        result = cursor.fetchall()
    assert result == []


def test_manager():
    print(TestModel.get_fields())
    test_record: TestModel = TestModel(id=str(uuid4()), test_field="test")
    assert False == check_record(TestModel, test_record.id)

    create_record_from_model(test_record)
    assert True == check_record(TestModel, test_record.id)

    test_record_copy: TestModel = _test_manager.get_by_id(test_record.id)
    assert test_record_copy.id == test_record.id

    test_record_updated: TestModel = _test_manager.update(pk = test_record.id, test_field = "test1")
    assert test_record_updated != test_record and test_record_updated.test_field == "test1"

    _test_manager.delete(test_record.id)
    assert False == check_record(TestModel, test_record.id)