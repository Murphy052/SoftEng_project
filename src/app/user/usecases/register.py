import re

from contractsPY import Usecase, if_fails
from passlib.context import CryptContext

from src.app.user.manager import user_manager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@if_fails(message="Username is invalid or used by someone")
def validate_username(state):
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    if not re.match(pattern, state.username):
        return False

    user = user_manager.get_user(state.username)

    return False if user else True


@if_fails(message="Cannot create user")
def create_user(state):
    hashed_password = pwd_context.hash(state.password)
    state.user = user_manager.create_user(
        username=state.username,
        password=hashed_password,
    )
    return True if state.user else False


register_usecase = Usecase()
register_usecase.contract = [
    validate_username,
    create_user,
]