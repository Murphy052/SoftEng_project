from __future__ import annotations

from functools import wraps

from fastapi import HTTPException, Request, status
from starlette.authentication import UnauthenticatedUser, AuthenticationBackend, AuthenticationError
import jwt
from jwt.exceptions import InvalidTokenError

from src.app.user.manager import user_manager
from src.core import settings


class BearerTokenAuthBackend(AuthenticationBackend):
    """
    This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
    a tuple
    """
    async def authenticate(self, request):
        # This function is inherited from the base class and called by some other class
        auth = request.cookies.get("authorization") or request.headers.get("authorization")
        if auth is None:
            return

        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except (ValueError, UnicodeDecodeError, InvalidTokenError) as exc:
            raise AuthenticationError('Invalid JWT Token.')

        username: str = decoded.get("sub")

        user = user_manager.get_user(username=username)
        if user is None:
            raise AuthenticationError('Invalid JWT Token.')

        if not user.is_active:
            raise AuthenticationError('User is not active')

        return auth, user


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=400)

        user = request.user

        if isinstance(user, UnauthenticatedUser):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not verified or active"
            )

        return await func(*args, **kwargs)

    return wrapper