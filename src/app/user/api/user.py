from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.app.user.model import User
from src.app.user.schemas import UserRegisterSchema, TokenSchema

router = APIRouter()

register_usecase=...
user_login_usecase=...


@router.post("/register")
async def register(data: UserRegisterSchema):
    result = register_usecase.apply(
        username=data.username,
        password=data.password,
    )

    if result.case == "success":
        return "Success"

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=result.message,
    )


@router.post("/login", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenSchema:
    result = user_login_usecase.apply(
        username=form_data.username,
        password=form_data.password,
    )
    if result.case == "success":
        return TokenSchema(access_token=result.state.access_token, token_type="bearer")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=result.message,
        headers={"authorization": "Bearer"},
    )


@router.get("/me", response_model=User)
def get_me(request: Request) -> User:
    return request.user
