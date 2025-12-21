from fastapi import APIRouter

from app.api.v2 import chapter, book

api_router = APIRouter()

api_router.include_router(chapter.router)
api_router.include_router(book.router)

