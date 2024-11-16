from dataclasses import dataclass


@dataclass
class TokenResponseSchema:
    access_token: str
    token_type: str
