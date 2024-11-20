import sqlite3
import uuid
from dataclasses import dataclass

from src.db.database import SqliteDatabase
from src.db import get_db, get_db_cursor
from src.db.exceptions import RecordDoesNotExist
from src.db.manager import BaseManager
from src.db.shortcuts import check_record, create_record_from_model
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


def setup_db():
    """Create test table before tests."""
    query = "CREATE TABLE IF NOT EXISTS test_model (id TEXT PRIMARY KEY, test_field TEXT);"
    with get_db_cursor(get_db()) as cursor:
        cursor.execute(query)


def teardown_db():
    """Drop test table after tests."""
    query = "DROP TABLE IF EXISTS test_model;"
    with get_db_cursor(get_db()) as cursor:
        cursor.execute(query)


def test_db_model():
    """Test the BaseModel functionality."""
    uid = uuid.uuid4()
    test_record = TestModel(uid, "test")

    assert uid == test_record.id, "ID mismatch in BaseModel."
    assert test_record.__tablename__ == "test_model", "Incorrect table name in BaseModel."
    assert test_record.test_field == "test", "Field value mismatch in BaseModel."


def test_db_connection():
    """Test database connection utilities."""
    db = get_db()
    conn = db.get_conn()
    cursor = db.get_cursor()

    assert isinstance(conn, sqlite3.Connection), "DB connection is not of type sqlite3.Connection."
    assert isinstance(cursor, sqlite3.Cursor), "DB cursor is not of type sqlite3.Cursor."


def test_table_creation():
    """Test if the table is created successfully."""
    setup_db()
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='test_model';"
    with get_db_cursor(get_db()) as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    assert result is not None, "Table 'test_model' was not created."
    teardown_db()


def test_manager_crud_operations():
    """Test CRUD operations via the manager."""
    setup_db()
    uid = str(uuid.uuid4())

    # Create
    test_record = TestModel(id=uid, test_field="test")
    create_record_from_model(test_record)
    assert check_record(TestModel, test_record.id), "Record was not created."

    # Read
    fetched_record = _test_manager.get_by_id(test_record.id)
    assert fetched_record.id == test_record.id, "Fetched record ID mismatch."
    assert fetched_record.test_field == test_record.test_field, "Fetched record field mismatch."

    # Update
    updated_record = _test_manager.update(pk=test_record.id, test_field="updated_test")
    assert updated_record.id == test_record.id, "Updated record ID mismatch."
    assert updated_record.test_field == "updated_test", "Record was not updated correctly."

    # Delete
    _test_manager.delete(test_record.id)
    assert not check_record(TestModel, test_record.id), "Record was not deleted."

    teardown_db()


def test_error_handling():
    """Test error handling scenarios."""
    setup_db()

    # Test fetching non-existent record
    try:
        _test_manager.get_by_id(str(uuid.uuid4()))
        assert False, "Fetching non-existent record did not raise RecordDoesNotExist."
    except RecordDoesNotExist:
        pass  # Expected behavior

    # Test updating non-existent record
    try:
        _test_manager.update(pk=str(uuid.uuid4()), test_field="should_fail")
        assert False, "Updating non-existent record did not raise an exception."
    except Exception as e:
        assert isinstance(e, RecordDoesNotExist), "Unexpected exception type."

    teardown_db()


def test_boundary_cases():
    """Test edge cases for CRUD operations."""
    setup_db()

    # Empty table fetch
    try:
        _test_manager.get_all()
        assert False, "Fetching from an empty table did not raise an exception."
    except Exception as e:
        assert str(e) == "No record found", "Unexpected error message for empty fetch."

    teardown_db()
