from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

from src.core import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")
