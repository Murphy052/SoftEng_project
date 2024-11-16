from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from src.app.user.crypto import verify_password, create_access_token, hash_password
from src.app.user.manager import user_manager
from src.app.user.models import User, UserCreate
from src.app.user.schemas import UserRegisterSchema, TokenResponseSchema
from src.db.exceptions import RecordDoesNotExist

router = APIRouter()


@router.post("/register")
async def register(data: UserRegisterSchema):
    hashed_password = hash_password(data.password)
    try:
        user_manager.create_user(UserCreate(username=data.username, password=hashed_password,))
        return "Successfully registered", status.HTTP_201_CREATED
    except ValueError as e:
        err_detail = e.args[0]
    except RecordDoesNotExist:
        err_detail = "Error while creating User"

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=err_detail,
    )


@router.post("/login", response_model=TokenResponseSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponseSchema:
    try:
        user: User = user_manager.get_user(username=form_data.username)
    except RecordDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with username {form_data.username} does not exist",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password",
        )

    return TokenResponseSchema(
        access_token=create_access_token(user.username),
        token_type="bearer"
    )


@router.get("/me", response_model=User)
def get_me(request: Request) -> User:
    return request.user
