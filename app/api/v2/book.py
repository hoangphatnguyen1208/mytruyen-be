from fastapi import APIRouter, status
from app.api.deps import SessionDep, CurrentAdmin

from app.crud import book as crud_book
from app.schema.auth import Message
from app.schema.book import BookCreate, BookPublic, BookUpdate, BookRegister
from app.schema.response import Response, ResponseList

from app.utilities.exceptions.http.exc_400 import http_exc_400_bad_book_request
from app.utilities.exceptions.http.exc_404 import http_exc_404_book_not_found_request
from app.utilities.exceptions.http.exc_403 import http_exc_403_forbidden_request

router = APIRouter(prefix="/books", tags=["book"])

@router.get("/{book_id}", response_model=Response[BookPublic])
async def get_book_by_id(book_id: str, session: SessionDep):
    db_book = await crud_book.get_book_by_id(session, book_id)
    if not db_book:
        raise http_exc_404_book_not_found_request(string=book_id)
    return Response(status_code=200, success=True, message="Book retrieved successfully", data=db_book)

@router.patch("/{book_id}", response_model=Response[BookPublic])
async def update_book(book_id: str, session: SessionDep, current_admin: CurrentAdmin, book: BookUpdate):
    db_book = await crud_book.get_book_by_id(session, book_id)
    if not db_book:
        raise http_exc_404_book_not_found_request(string=book_id)
    if db_book.author_id != current_admin.id:
        raise http_exc_403_forbidden_request()
    updated_book = await crud_book.update_book(session, db_book.id, book)
    return Response(status_code=200, success=True, message="Book updated successfully", data=updated_book)

@router.delete("/{book_id}", response_model=Response[None])
async def delete_book(book_id: str, session: SessionDep, current_admin: CurrentAdmin):
    db_book = await crud_book.get_book_by_id(session, book_id)
    if not db_book:
        raise http_exc_404_book_not_found_request(string=book_id)
    if db_book.author_id != current_admin.id:
        raise http_exc_403_forbidden_request()
    await crud_book.delete_book(session, db_book.id)
    return Response(status_code=200, success=True, message="Book deleted successfully", data=None)



