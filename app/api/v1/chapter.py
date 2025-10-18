import uuid
from fastapi import APIRouter

from app.crud import chapter as crud_chapter
from app.schema.chapter import ChapterCreate, ChapterRegister, ChapterPublic, ChapterUpdate
from app.schema.chapter import ChapterContentCreate, ChapterContentRegister, ChapterContentPublic, ChapterContentUpdate
from app.api.deps import CurrentAdmin, SessionDep

from app.utilities.exceptions.http.exc_400 import (
    http_exc_400_chapter_bad_request,
    http_exc_400_chapter_content_bad_request
)
from app.utilities.exceptions.http.exc_404 import (
    http_404_exc_chapter_not_found_request,
    http_404_exc_chapter_content_not_found_request
)

router = APIRouter(prefix="/chapter", tags=["chapter"])

@router.get("/{book_id}", response_model=list[ChapterPublic])
async def get_chapter(session: SessionDep, book_id: uuid.UUID):
    print(f"Fetching chapters for book_id={book_id}")
    chapters = await crud_chapter.get_chapters_by_book_id(session, book_id)
    return chapters

@router.post("/{book_id}", response_model=ChapterPublic)
async def create_chapter(session: SessionDep, book_id: uuid.UUID, chapter_data: ChapterRegister, current_admin: CurrentAdmin):
    existing_chapter = await crud_chapter.get_chapter_by_book_id_and_chapter_index(
        session, book_id, chapter_data.index
    )
    if existing_chapter:
        raise http_exc_400_chapter_bad_request(slug=chapter_data.index)
    chapter_in = ChapterCreate.model_validate(chapter_data, update={"book_id": book_id, "author_id": current_admin.id})
    chapter = await crud_chapter.create_chapter(session, chapter_in)
    return chapter

@router.patch("/{chapter_id}", response_model=ChapterPublic)
async def update_chapter(session: SessionDep, chapter_id: uuid.UUID, chapter_data: ChapterUpdate):
    existing_chapter = await crud_chapter.get_chapter_by_id(session, chapter_id)
    if not existing_chapter:
        raise http_404_exc_chapter_not_found_request(chapter_id=chapter_id)
    updated_chapter = await crud_chapter.update_chapter(session, chapter_id, chapter_data)
    return updated_chapter

@router.get("/content/{chapter_id}", response_model=ChapterContentPublic)
async def get_chapter_content(session: SessionDep, chapter_id: uuid.UUID):
    chapter = await crud_chapter.get_chapter_by_id(session, chapter_id)
    if not chapter:
        raise http_404_exc_chapter_not_found_request(chapter_id=f"{chapter_id}")
    chapter_content = await crud_chapter.get_chapter_content_by_chapter_id(session, chapter_id)
    if not chapter_content:
        raise http_404_exc_chapter_content_not_found_request(chapter_id=f"{chapter_id}")
    return chapter_content

@router.post("/content/{chapter_id}", response_model=ChapterContentPublic)
async def create_chapter_content(session: SessionDep, chapter_id: uuid.UUID, chapter_content_data: ChapterContentRegister, current_admin: CurrentAdmin):
    chapter = await crud_chapter.get_chapter_by_id(session, chapter_id)
    if not chapter:
        raise http_404_exc_chapter_not_found_request(chapter_id=f"{chapter_id}")
    chapter_content_existing = await crud_chapter.get_chapter_content_by_chapter_id(session, chapter_id)
    if chapter_content_existing:
        raise http_exc_400_chapter_content_bad_request(slug=f"{chapter_id}")
    chapter_content_in = ChapterContentCreate.model_validate(
        chapter_content_data,
        update={"chapter_id": chapter.id}
    )
    chapter_content = await crud_chapter.create_chapter_content(session, chapter_content_in)
    return chapter_content

@router.patch("/content/{chapter_id}", response_model=ChapterContentPublic)
async def update_chapter_content(session: SessionDep, chapter_id: uuid.UUID, chapter_content_data: ChapterContentUpdate, current_admin: CurrentAdmin):
    existing_content = await crud_chapter.get_chapter_content_by_chapter_id(session, chapter_id)
    if not existing_content:
        raise http_404_exc_chapter_not_found_request(chapter_id=f"{chapter_id}")
    chapter_content_in = ChapterContentUpdate.model_validate(chapter_content_data)
    updated_content = await crud_chapter.update_chapter_content(session, chapter_id, chapter_content_in)
    return updated_content

