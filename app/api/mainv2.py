from fastapi import APIRouter

from app.api.v2 import chapter

api_router = APIRouter()

api_router.include_router(chapter.router)

