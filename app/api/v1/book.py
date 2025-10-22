from fastapi import APIRouter
from app.api.deps import SessionDep, CurrentAdmin

from app.crud import book as crud_book
from app.schema.auth import Message
from app.schema.book import BookCreate, BookPublic, BookUpdate, BookRegister

from app.utilities.exceptions.http.exc_400 import http_400_exc_bad_book_request
from app.utilities.exceptions.http.exc_404 import http_404_exc_book_not_found_request
from app.utilities.exceptions.http.exc_403 import http_403_exc_forbidden_request

router = APIRouter(prefix="/books", tags=["book"])

@router.post("", response_model=BookPublic)
async def create_book(session: SessionDep, current_admin: CurrentAdmin, book_register: BookRegister):
    existing_book = await crud_book.get_book_by_slug(session, book_register.slug)
    if existing_book:
        raise http_400_exc_bad_book_request(slug=book_register.slug)
    book_in = BookCreate.model_validate(book_register, update={"author_id": str(current_admin.id), "poster": book_register.poster.model_dump()})
    db_book = await crud_book.create_book(session, book_in)
    return db_book

@router.get("", response_model=list[BookPublic])
async def get_books(session: SessionDep) -> list[BookPublic]:
    db_books = await crud_book.get_books(session)
    return db_books

@router.get("/{slug}", response_model=BookPublic)
async def get_book_by_slug(slug: str, session: SessionDep):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        raise http_404_exc_book_not_found_request(string=slug)
    return db_book

@router.patch("/{slug}", response_model=BookPublic)
async def update_book(slug: str, session: SessionDep, current_admin: CurrentAdmin, book: BookUpdate):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        raise http_404_exc_book_not_found_request(string=slug)
    if db_book.author_id != current_admin.id:
        raise http_403_exc_forbidden_request()
    updated_book = await crud_book.update_book(session, db_book.id, book)
    return updated_book

@router.delete("/{slug}", response_model=Message)
async def delete_book(slug: str, session: SessionDep, current_admin: CurrentAdmin):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        raise http_404_exc_book_not_found_request(string=slug)
    if db_book.author_id != current_admin.id:
        raise http_403_exc_forbidden_request()
    await crud_book.delete_book(session, db_book.id)
    return {"message": "Book deleted successfully"}

