from dataclasses import field, dataclass

from src.db.models import BaseModel


@dataclass
class User(BaseModel):
    username: str
    password: str
    is_active: bool = field(default=True)
    is_superuser: bool = field(default=False)
