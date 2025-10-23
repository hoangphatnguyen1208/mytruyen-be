from fastapi import APIRouter

from app.api.v1 import auth, book, genre, chapter, tag, arq

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(book.router)
api_router.include_router(genre.router)
api_router.include_router(chapter.router)
api_router.include_router(tag.router)
api_router.include_router(arq.router)
