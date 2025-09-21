from sqlalchemy.ext.asyncio import create_async_engine 

from app.core.config import settings

async_engine = create_async_engine(
    settings.POSTGRE_URL
)