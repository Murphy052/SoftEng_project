import sqlite3
from abc import abstractmethod
from contextlib import contextmanager
from typing import Protocol, TypeVar, Optional

from src.core import settings, logger

_Connection = TypeVar('_Connection')
_Cursor = TypeVar('_Cursor')


class Database(Protocol):
    @abstractmethod
    def connect(self, conn_str) -> None:
        ...

    @abstractmethod
    def get_conn(self) -> _Connection:
        ...

    @abstractmethod
    def get_cursor(self) -> _Cursor:
        ...


class SqliteDatabase(Database):
    """
    Singleton Sqlite Database class
    """
    _instance: Optional[object] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            return object.__new__(cls)
        else:
            return cls._instance

    def __init__(self, conn_str: str = settings.DB_NAME) -> None:
        self._connection: Optional[sqlite3.Connection] = None
        self.connect(conn_str)

    def connect(self, conn_str: str) -> None:
        if self._connection is None:
            self._connection = sqlite3.connect(conn_str)

    def get_conn(self) -> sqlite3.Connection:
        return self._connection

    def get_cursor(self) -> sqlite3.Cursor:
        return self.get_conn().cursor()


@contextmanager
def get_db_cursor(db: Database):
    db_conn: _Connection = db.get_conn()
    db_cursor: _Cursor = db.get_cursor()

    try:
        yield db_cursor
        db_conn.commit()
    except sqlite3.Error as e:
        db_conn.rollback()
        raise e
    finally:
        db_cursor.close()

def get_db():
    return SqliteDatabase()
