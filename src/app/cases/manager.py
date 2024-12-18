import random
from typing import List

from src.app.cases.models.case import Case
from src.app.cases.models.case_items import CaseWithItems
from src.app.cases.models.item import Item
from src.app.user.models import User
from src.db.database import Database, get_db, get_db_cursor
from src.db.manager import BaseManager


class CaseManager(BaseManager[Case]):
    def __init__(self):
        super().__init__(Case)

    @classmethod
    def get_case_items(
            cls,
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

        result: List[Item] = list(map(lambda row: Item(*row), raw_data))
        return result


    def get_case(
            self,
            case_id: int
    ) -> CaseWithItems:
        items = self.get_case_items(case_id)
        case = self.get_by_id(case_id)
        return CaseWithItems(case.id, case.name, case.image, items)

    def open_case(
            self,
            case_id: int,
            user: User,
    ) -> Item:
        items = self.get_case_items(case_id)

        random_item = random.choice(items)

        return random_item


case_manager = CaseManager()
