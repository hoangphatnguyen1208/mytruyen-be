from fastapi import APIRouter, Response
from app.api.deps import SessionDep, CurrentAdmin

from app.crud import book as crud_book, genre as crud_genre
from app.schema.book import BookCreate, BookPublic, BookUpdate, BookRegister
from app.schema.response import BookResponse, BooksResponse, Response

from app.utilities.exceptions.http.exc_400 import http_400_exc_bad_book_request
from app.utilities.exceptions.http.exc_404 import http_404_exc_book_not_found_request
from app.utilities.exceptions.http.exc_403 import http_403_exc_forbidden_request

router = APIRouter(tags=["book"])

@router.post("/book", response_model=BookResponse)
async def create_book(session: SessionDep, current_admin: CurrentAdmin, book_register: BookRegister):
    existing_book = await crud_book.get_book_by_slug(session, book_register.slug)
    if existing_book:
        raise http_400_exc_bad_book_request(slug=book_register.slug)
    book_in = BookCreate.model_validate(book_register, update={"author_id": str(current_admin.id)})
    db_book = await crud_book.create_book(session, book_in)
    book_out = await crud_book.get_book_by_id(session, db_book.id)
    return BookResponse(success=True, message="Book created successfully", data=book_out)

@router.get("/books", response_model=BooksResponse)
async def get_books(session: SessionDep) -> BooksResponse:
    db_books = await crud_book.get_books(session)
    return BooksResponse(success=True, message="Books retrieved successfully", data=db_books)

@router.get("/book/{slug}")
async def get_book_by_slug(slug: str, session: SessionDep):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        return http_404_exc_book_not_found_request(string=slug)
    return Response(success=True, message="Book retrieved successfully", data=db_book)

@router.patch("/book/{slug}", response_model=BookPublic)
async def update_book(slug: str, session: SessionDep, current_admin: CurrentAdmin, book: BookUpdate):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        raise http_404_exc_book_not_found_request(slug=slug)
    if db_book.author_id != current_admin.id:
        raise http_403_exc_forbidden_request()
    print(book)
    updated_book = await crud_book.update_book(session, db_book.id, book)
    return updated_book

@router.delete("/book/{slug}", response_model=Response)
async def delete_book(slug: str, session: SessionDep, current_admin: CurrentAdmin):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        raise http_404_exc_book_not_found_request(string=slug)
    if db_book.author_id != current_admin.id:
        raise http_403_exc_forbidden_request()
    success = await crud_book.delete_book(session, db_book.id)
    if success:
        return Response(success=True, message="Book deleted successfully")
    return Response(success=False, message="Failed to delete book")