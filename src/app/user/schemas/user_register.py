from pydantic import BaseModel, field_validator

from src.app.user.crypto import hash_password


class UserRegisterSchema(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        return hash_password(v)
