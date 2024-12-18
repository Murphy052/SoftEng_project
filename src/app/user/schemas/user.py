from dataclasses import dataclass
from typing import List

from src.app.cases.models.item import Item


@dataclass
class UserSchema:
    username: str
    inventory: List[Item]
