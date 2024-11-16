import re
from dataclasses import dataclass


@dataclass(frozen=True)
class UserCreate:
    username: str
    password: str

    def __post_init__(self):
        self.validate_username(self.username)

    @staticmethod
    def validate_username(field):
        if field is None or field == "":
            raise ValueError("Username cannot be empty")
        if len(field) > 255:
            raise ValueError("Username must be less than 255 characters")
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        if not re.match(pattern, field):
            raise ValueError("Username must contain only letters, numbers and underscore")
        # if user_manager.is_username_used(field):
        #     raise ValueError("Username already exists")