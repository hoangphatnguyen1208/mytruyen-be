from fastapi import APIRouter
from app.api.deps import SessionDep, CurrentAdmin

from app.crud import book as crud_book
from app.schema.book import BookCreate, BookPublic, BookUpdate, BookRegister

from app.utilities.exceptions.http.exc_400 import http_400_exc_bad_book_slug_request

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookPublic)
async def create_book(session: SessionDep, current_admin: CurrentAdmin, book_register: BookRegister):
    existing_book = await crud_book.get_book_by_slug(session, book_register.slug)
    if existing_book:
        raise await http_400_exc_bad_book_slug_request(slug=book_register.slug)
    book_in = BookCreate.model_validate(book_register, update={"author_id": str(current_admin.id)})
    db_book = await crud_book.create_book(session, book_in)
    return db_book

@router.get("/{slug}", response_model=BookPublic)
async def get_book_by_slug(slug: str, session: SessionDep):
    db_book = await crud_book.get_book_by_slug(session, slug)
    return db_book

@router.put("/{slug}", response_model=BookPublic)
async def update_book(slug: str, session: SessionDep, current_admin: CurrentAdmin, book: BookUpdate):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        return None
    if db_book.author_id != current_admin.id:
        return None
    updated_book = await crud_book.update_book(session, db_book.id, book)
    return updated_book

@router.delete("/{slug}", response_model=dict)
async def delete_book(slug: str, session: SessionDep, current_admin: CurrentAdmin):
    db_book = await crud_book.get_book_by_slug(session, slug)
    if not db_book:
        return {"success": False, "message": "Book not found"}
    if db_book.author_id != current_admin.id:
        return {"success": False, "message": "Not authorized to delete this book"}
    success = await crud_book.delete_book(session, db_book.id)
    if success:
        return {"success": True, "message": "Book deleted successfully"}
    return {"success": False, "message": "Failed to delete book"}