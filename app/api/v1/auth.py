from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

from app.crud import user
from app.core.config import settings
from app.core.security import create_access_token

from app.schema.auth import Token

from app.api.deps import SessionDep

from app.utilities.exceptions.http.exc_400 import http_exc_400_credentials_bad_signin_request


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login/access-token")
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = user.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise http_exc_400_credentials_bad_signin_request()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            subject=str(user.id), expires_delta=access_token_expires
        ),
        token_type="bearer"
    )