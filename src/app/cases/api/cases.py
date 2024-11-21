from __future__ import annotations

from typing import List

from fastapi import APIRouter

from src.app.cases.managers import case_manager
from src.app.cases.models.case import Case
from src.app.cases.models.case_items import CaseWithItems

router = APIRouter()


@router.get("/cases")
async def get_cases() -> List[Case]:
    return case_manager.get_all()


@router.get("/cases/{case_id}")
async def get_case(case_id: int) -> CaseWithItems:
    return case_manager.get_case(case_id)
