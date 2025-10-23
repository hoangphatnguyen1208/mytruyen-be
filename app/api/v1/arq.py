from fastapi import APIRouter
from app.api.deps import CurrentAdmin, RedisDep



router = APIRouter(prefix="/arq", tags=["arq"])

@router.post("/crawl-genres")
async def crawl_genres(current_admin: CurrentAdmin, redis: RedisDep):
    await redis.enqueue_job("crawl_genres")
    return {"detail": "Crawl genres job enqueued"}