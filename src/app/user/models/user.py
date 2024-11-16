from dataclasses import field, dataclass

from src.db.models import BaseModel


@dataclass(frozen=True)
class User(BaseModel):
    __tablename__ = 'user'

    username: str
    password: str
