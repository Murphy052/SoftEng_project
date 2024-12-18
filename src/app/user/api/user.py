from __future__ import annotations

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.app.user.crypto import verify_password, create_access_token
from src.app.user.manager import user_manager
from src.app.user.middleware import auth_required
from src.app.user.models import User, UserCreate
from src.app.user.schemas import UserRegisterSchema, TokenResponseSchema
from src.app.user.schemas.user import UserSchema
from src.db.exceptions import RecordDoesNotExist

router = APIRouter()


@router.post("/register")
async def register(data: UserRegisterSchema):
    try:
        user_manager.create_user(
            UserCreate(
                username=data.username,
                password=data.password,
            )
        )
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


@router.get("/me", response_model=UserSchema)
@auth_required
async def get_me(request: Request) -> UserSchema:
    return UserSchema(
        username=request.user.username,
        inventory=user_manager.get_inventory(request.user.id),
    )
