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

@router.post("", response_model=Response[BookPublic], status_code=status.HTTP_201_CREATED)
async def create_book(session: SessionDep, current_admin: CurrentAdmin, book_register: BookRegister):
    existing_book = await crud_book.get_book_by_slug(session, book_register.slug)
    if existing_book:
        raise http_exc_400_bad_book_request(slug=book_register.slug)
    book_in = BookCreate.model_validate(book_register, update={"creator_id": str(current_admin.id)})
    db_book = await crud_book.create_book(session, book_in)
    return Response(status_code=201, success=True, message="Book created successfully", data=db_book)

@router.get("", response_model=ResponseList[BookPublic])
async def get_books(
    session: SessionDep,
    page: int = 1,
    limit: int = 10,
    sort: str | None = None,
) -> ResponseList[BookPublic]:
    skip = (page - 1) * limit
    db_books = await crud_book.get_books(
        session=session,
        skip=skip,
        limit=limit,
        sort=sort,
    )
    return ResponseList(status_code=200, success=True, message="Books retrieved successfully", data=db_books)

@router.get("/id/{book_id}", response_model=Response[BookPublic])
async def get_book_by_id(book_id: str, session: SessionDep):
    db_book = await crud_book.get_book_by_id(session, book_id)
    if not db_book:
        raise http_exc_404_book_not_found_request(string=book_id)
    return Response(status_code=200, success=True, message="Book retrieved successfully", data=db_book)

@router.patch("/id/{book_id}", response_model=Response[BookPublic])
async def update_book(book_id: str, session: SessionDep, current_admin: CurrentAdmin, book: BookUpdate):
    db_book = await crud_book.get_book_by_id(session, book_id)
    if not db_book:
        raise http_exc_404_book_not_found_request(string=book_id)
    if db_book.author_id != current_admin.id:
        raise http_exc_403_forbidden_request()
    updated_book = await crud_book.update_book(session, db_book.id, book)
    return Response(status_code=200, success=True, message="Book updated successfully", data=updated_book)

@router.delete("/id/{book_id}", response_model=Response[None])
async def delete_book(book_id: str, session: SessionDep, current_admin: CurrentAdmin):
    db_book = await crud_book.get_book_by_id(session, book_id)
    if not db_book:
        raise http_exc_404_book_not_found_request(string=book_id)
    if db_book.author_id != current_admin.id:
        raise http_exc_403_forbidden_request()
    await crud_book.delete_book(session, db_book.id)
    return Response(status_code=200, success=True, message="Book deleted successfully", data=None)

@router.get("/slug/{slug}", response_model=Response[BookPublic])
async def get_book_by_slug(slug: str, session: SessionDep):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        raise http_exc_404_book_not_found_request(string=slug)
    return Response(status_code=200, success=True, message="Book retrieved successfully", data=db_book)

@router.patch("/slug/{slug}", response_model=Response[BookPublic])
async def update_book(slug: str, session: SessionDep, current_admin: CurrentAdmin, book: BookUpdate):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        raise http_exc_404_book_not_found_request(string=slug)
    if db_book.author_id != current_admin.id:
        raise http_exc_403_forbidden_request()
    updated_book = await crud_book.update_book(session, db_book.id, book)
    return Response(status_code=200, success=True, message="Book updated successfully", data=updated_book)

@router.delete("/slug/{slug}", response_model=Response[None])
async def delete_book(slug: str, session: SessionDep, current_admin: CurrentAdmin):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        raise http_exc_404_book_not_found_request(string=slug)
    if db_book.author_id != current_admin.id:
        raise http_exc_403_forbidden_request()
    await crud_book.delete_book(session, db_book.id)
    return Response(status_code=200, success=True, message="Book deleted successfully", data=None)



