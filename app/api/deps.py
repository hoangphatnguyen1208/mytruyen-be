from fastapi import Depends, HTTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlmodel import Session, 

from app.core.config import settings
from app.core.db import engine

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token")

def get_db():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(token: TokenDep, session: SessionDep):
    