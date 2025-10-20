from sqlalchemy.ext.asyncio import create_async_engine 
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as crud_user
from app.models import user_role as UserRole
from app.schema.user import UserCreate
from app.core.config import settings

async_engine = create_async_engine(
    settings.POSTGRES_URL
)

async def init_db(session: AsyncSession):
    existing = await crud_user.get_user_by_email(session, settings.FIRST_ADMIN_EMAIL)
    if not existing:
        admin_in = UserCreate(
            email=settings.FIRST_ADMIN_EMAIL,
            password=settings.FIRST_ADMIN_PASSWORD,
            role=UserRole.ADMIN
        )
        await crud_user.create_user(session, admin_in)
        print(f"Created initial admin user with email: {settings.FIRST_ADMIN_EMAIL}")