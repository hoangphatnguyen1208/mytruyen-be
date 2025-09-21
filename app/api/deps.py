import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession

from app.utilities.exceptions.http.exc_403 import http_403_exc_forbidden_request
from app.utilities.exceptions.http.exc_404 import http_404_exc_id_not_found_request

from app.core.config import settings
from app.core.db import async_engine
from app.core import security

from app.crud import user as crud_user

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token")

async def get_db():
    async with AsyncSession(async_engine) as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        id = payload.get("sub")
    except jwt.PyJWTError:
        raise http_403_exc_forbidden_request()
    user = crud_user.get_user_by_id(session, id)
    if not user:
        raise http_404_exc_id_not_found_request(id=id)
    return user
