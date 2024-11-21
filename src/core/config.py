from __future__ import annotations

from datetime import timedelta
from os import getenv
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
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://cs-casino.netlify.app",
        "https://cs-casino-2aa0bc784bd4.herokuapp.com",
    ]

    # DB Params #
    DB_NAME:str = "database.db"


    DEBUG: bool = True

    # JWT Params #
    SECRET_KEY: str = getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_LIFETIME: timedelta = timedelta(days=30)


settings = Settings()
