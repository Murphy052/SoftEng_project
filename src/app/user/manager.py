from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from pypika import Query
from pypika.queries import QueryBuilder

from src.app.user.models import User, UserCreate
from src.db import get_db_cursor, get_db
from src.db.exceptions import RecordDoesNotExist
from src.db.manager import BaseManager

if TYPE_CHECKING:
    from src.db.database import Database


class UserManager(BaseManager[User]):
    def __init__(self):
        super().__init__(User)

    def create_user(
            self,
            user: UserCreate,
            db = get_db()
    ) -> User:
        q: QueryBuilder = (
            Query()
            .into(self.table)
            .columns('id', 'username', 'password')
            .insert((str(uuid.uuid4()), user.username, user.password))
        )

        table_fields: str = ', '.join(self._fields)
        query: str = q.get_sql() + f" RETURNING {table_fields};"
        print(query)

        with get_db_cursor(db) as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

        if not result:
            raise RecordDoesNotExist

        return User(*result)


    def get_user(
            self,
            username: str,
            db: Database = get_db(),
    ):
        q: QueryBuilder = (
            Query()
            .from_(self.table)
            .select(*self._fields)
            .where(self.table.username == username)
        )

        query = q.get_sql()

        with get_db_cursor(db) as cur:
            cur.execute(query)
            result = cur.fetchone()

        if not result:
            raise RecordDoesNotExist

        return User(*result)


user_manager = UserManager()