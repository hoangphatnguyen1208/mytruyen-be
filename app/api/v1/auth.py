from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta


from app.core.config import settings
from app.core.security import create_access_token
from app.api.deps import SessionDep

from app.schema.auth import Message, Token, UserLogin, UserRegister
from app.schema.response import Response

from app.crud import (
    user as user_crud,
)

from app.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_bad_email_request
)


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login/access-token", response_model=Token)
async def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await user_crud.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise http_exc_400_credentials_bad_signin_request()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = Token(
        access_token=create_access_token(
            subject=str(user.id), expires_delta=access_token_expires
        ),
        token_type="bearer"
    )
    return token

@router.post("/login", response_model=Response[Token])
async def login(session: SessionDep, user_login: UserLogin) -> Response[Token]:
    user = await user_crud.authenticate(session, user_login.email, user_login.password)
    if not user:
        raise http_exc_400_credentials_bad_signin_request()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = Token(
        access_token=create_access_token(
            subject=str(user.id), expires_delta=access_token_expires
        ),
        token_type="bearer"
    )
    return Response(status_code=200, success=True, message="Login successful", data=token)

@router.post("/register", response_model=Response[Message])
async def register(session: SessionDep, user_register: UserRegister) -> Response[Message]:
    existing_user = await user_crud.get_user_by_email(session, user_register.email)
    if existing_user:
        raise http_exc_400_bad_email_request(email=user_register.email)
    user = await user_crud.create_user(session, user_register)
    return Response(status_code=201, success=True, message="User registered successfully", data=Message(message="User registered successfully"))

@router.get("/test", response_model=Response[dict])
async def test() -> Response[dict]:
    return Response(status_code=200, success=True, message="Test endpoint", data={"message": "Test endpoint"})
