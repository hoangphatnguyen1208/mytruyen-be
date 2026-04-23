import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Any, TypeAlias
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid
from httpx import AsyncClient
from meilisearch import Client as MeiliSearchClient

from app.utilities.exceptions.http.exc_403 import http_exc_403_forbidden_request
from app.utilities.exceptions.http.exc_404 import http_exc_404_id_not_found_request

from app.core.config import settings
from app.core.db import async_session_factory
from app.core import security
from app.models import User, user_role as UserRole

from app.crud import user as crud_user

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token")

async def get_db():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()

SessionDep: TypeAlias = Annotated[AsyncSession, Depends(get_db)]
TokenDep: TypeAlias = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(session: SessionDep, token: TokenDep):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        id = payload.get("id")
    except jwt.PyJWTError:
        raise http_exc_403_forbidden_request()
    if not id:
        raise http_exc_403_forbidden_request()
    id = uuid.UUID(id)
    user = await crud_user.get_user_by_id(session, id)
    if not user:
        raise http_exc_404_id_not_found_request(id=str(id))
    return user

CurrentUser: TypeAlias = Annotated[User, Depends(get_current_user)]

def get_current_admin(current_user: CurrentUser) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

CurrentAdmin: TypeAlias = Annotated[User, Depends(get_current_admin)]


async def get_redis(request: Request):
    return request.app.state.redis_pool

RedisDep: TypeAlias = Annotated[Any, Depends(get_redis)]

async def get_client():
    async with AsyncClient() as client:
        yield client

ClientDep: TypeAlias = Annotated[AsyncClient, Depends(get_client)]

async def get_meilisearch_client(request: Request):
    return request.app.state.meili_client

MeiliSearchClientDep: TypeAlias = Annotated[MeiliSearchClient, Depends(get_meilisearch_client)]