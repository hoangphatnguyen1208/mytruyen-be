from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud import user as crud_user
from app.models import user_role as UserRole
from app.schema.user import UserCreate
from app.core.config import settings

async_engine = create_async_engine(
    settings.POSTGRES_URL,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db(session: AsyncSession):
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(SQLModel.metadata.create_all)
    existing = await crud_user.get_user_by_email(session, settings.FIRST_ADMIN_EMAIL)
    if not existing:
        admin_in = UserCreate(
            email=settings.FIRST_ADMIN_EMAIL,
            password=settings.FIRST_ADMIN_PASSWORD,
            role=UserRole.ADMIN
        )
        await crud_user.create_user(session, admin_in)
        print(f"Created initial admin user with email: {settings.FIRST_ADMIN_EMAIL}")

