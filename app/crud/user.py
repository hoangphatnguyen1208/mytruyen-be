import uuid
from app.schema import user
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User

from app.schema.user import UserCreate

from app.core.security import get_password_hash, verify_password

async def authenticate(session: AsyncSession, email: str, password: str) -> User:
    users = await session.exec(select(User).where(User.email == email))
    user_db = users.first()
    if not user_db:
        return None
    if not verify_password(password, user_db.hashed_password):
        return None
    return user_db

async def create_user(session: AsyncSession, user_create: UserCreate):
    user = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_id(session: AsyncSession, user_id: uuid.UUID) -> User:
    user_db =  await session.get(User, user_id)
    return user_db

async def get_user_by_email(session: AsyncSession, email: str) -> User:
    users = await session.exec(select(User).where(User.email == email))
    return users.first()