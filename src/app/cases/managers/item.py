from typing import List

from src.app.cases.models.item import Item
from src.db import get_db_cursor, get_db
from src.db.database import Database
from src.db.manager import BaseManager


class ItemManager(BaseManager[Item]):
    def __init__(self):
        super().__init__(Item)

    def get_case_items(
            self,
            case_id: int,
            db: Database = get_db()
    ) -> List[Item]:
        query = f"""
        SELECT 
            items.id AS item_id,
            items.name AS item_name,
            items.rarity,
            items.image
        FROM 
            case_items
        JOIN 
            items ON case_items.item_id = items.id
        JOIN 
            cases ON case_items.case_id = cases.id
        WHERE 
            cases.id = {case_id}
        """

        with get_db_cursor(db) as cursor:
            cursor.execute(query)
            raw_data = cursor.fetchall()

        if raw_data is None:
            return []

        result: List[Item] = list(map(lambda row: self._model(*row), raw_data))
        return result



item_manager = ItemManager()
