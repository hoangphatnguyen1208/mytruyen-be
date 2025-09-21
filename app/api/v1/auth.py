from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

from app.crud import user
from app.core.config import settings
from app.core.security import create_access_token

from app.schema.auth import Token

from app.api.deps import SessionDep


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login/access-token")
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = user.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            subject=str(user.id), expires_delta=access_token_expires
        ),
        token_type="bearer"
    )