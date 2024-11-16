from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from src.core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(
        password: str
) -> str:
    return pwd_context.hash(password)


def verify_password(
        plain_password,
        hashed_password,
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        username: str,
        lifetime: timedelta = settings.ACCESS_TOKEN_LIFETIME,
) -> str:
    expire = datetime.utcnow() + lifetime
    to_encode = {
        "sub": username,
        "exp": expire,
    }
    access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return access_token