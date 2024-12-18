from __future__ import annotations

from typing import List

from fastapi import APIRouter, Request, HTTPException, status

from src.app.cases.manager import case_manager
from src.app.cases.models.case import Case
from src.app.cases.models.case_items import CaseWithItems
from src.app.cases.models.item import Item

router = APIRouter()


@router.get("/cases")
async def get_cases() -> List[Case]:
    return case_manager.get_all()


@router.get("/cases/{case_id}")
async def get_case(case_id: int) -> CaseWithItems:
    return case_manager.get_case(case_id)


@router.get("/open-case")
async def get_open_case(request: Request) -> Item:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
    )