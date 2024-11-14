from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_DIR: Path = Path(__file__).resolve().parent.parent
    STATIC_DIR: Path = APP_DIR.joinpath("view/static")
    TEMPLATES_DIR: Path = APP_DIR.joinpath("view/templates")

    ALLOWED_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "https://yourdomain.com",
        "https://yourwebapp.net",
    ]

    # DB Params #
    DB_NAME:str = "database.db"


    DEBUG: bool = True

    # JWT Params
    #
    # SECRET_KEY: str
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_LIFETIME: timedelta = timedelta(days=30)

    # class Config:
    #     env_file = "./.env"
    #     extra = "ignore"


settings = Settings()
