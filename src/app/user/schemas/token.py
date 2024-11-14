from dataclasses import dataclass


@dataclass
class TokenSchema:
    access_token: str
    token_type: str
