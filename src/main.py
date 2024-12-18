from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from src.app.user.middleware import BearerTokenAuthBackend
from src.app.user.api import user_router
from src.app.cases.api import case_router
from src.db.database import SqliteDatabase
from src.db.init_db import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SqliteDatabase("database.db")
    # initialize_database(db)
    yield
    db.get_conn().close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="src/view/static"), name="static")
app.include_router(user_router)
app.include_router(case_router)
