from fastapi import APIRouter
from app.api.deps import CurrentAdmin, RedisDep

router = APIRouter(prefix="/arq", tags=["arq"])

@router.post("/crawl-genres")
async def crawl_genres(current_admin: CurrentAdmin, redis: RedisDep):
    await redis.enqueue_job("crawl_genres")
    return {"detail": "Crawl genres job enqueued"}

@router.post("/crawl-tags")
async def crawl_tags(current_admin: CurrentAdmin, redis: RedisDep):
    await redis.enqueue_job("crawl_tags")
    return {"detail": "Crawl tags job enqueued"}

@router.post("/crawl-book-statuses")
async def crawl_book_statuses(current_admin: CurrentAdmin, redis: RedisDep):
    await redis.enqueue_job("crawl_book_statuses")
    return {"detail": "Crawl book statuses job enqueued"}

@router.post("/crawl-books")
async def crawl_books(current_admin: CurrentAdmin, redis: RedisDep, limit: int = 20):
    await redis.enqueue_job("crawl_all_books", limit=limit)
    return {"detail": "Crawl books job enqueued"}