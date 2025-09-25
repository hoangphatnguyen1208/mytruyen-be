from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models import Book
from app.schema.book import BookCreate, BookUpdate

async def create_book(session: AsyncSession, book_create: BookCreate) -> Book:
    db_book = Book.model_validate(book_create)
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book

async def get_book_by_id(session: AsyncSession, book_id: str) -> Book | None:
    book = await session.get(Book, book_id)
    return book

async def get_book_by_slug(session: AsyncSession, slug: str) -> Book | None:
    statement = select(Book).where(Book.slug == slug)
    books = await session.exec(statement)
    return books.first()

async def update_book(session: AsyncSession, book_id: str, book: BookUpdate) -> Book | None:
    book_data = book.dict(exclude_unset=True)
    current_book = await get_book_by_id(session, book_id)
    if not current_book:
        return None
    current_book.sqlmodel_update(book_data)
    session.add(current_book)
    await session.commit()
    await session.refresh(current_book)
    return current_book

async def delete_book(session: AsyncSession, book_id: str) -> bool:
    book = await get_book_by_id(session, book_id)
    if not book:
        return False
    await session.delete(book)
    await session.commit()
    return True