from src.app.cases.managers.item import item_manager
from src.app.cases.models.case import Case
from src.app.cases.models.case_items import CaseWithItems
from src.db.manager import BaseManager


class CaseManager(BaseManager[Case]):
    def __init__(self):
        super().__init__(Case)

    @staticmethod
    def get_case(case_id: int) -> CaseWithItems:
        items = item_manager.get_case_items(case_id)
        case = case_manager.get_by_id(case_id)
        return CaseWithItems(case.id, case.name, case.image, items)

case_manager = CaseManager()
