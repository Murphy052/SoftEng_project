from dataclasses import dataclass


@dataclass
class UserRegisterSchema:
    username: str
    password: str
