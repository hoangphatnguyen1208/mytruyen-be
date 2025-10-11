from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.models import Book, Genre, GenreBook
from app.schema.book import BookCreate, BookUpdate, BookPublic

async def create_book(session: AsyncSession, book_create: BookCreate) -> Book:
    db_book = Book.model_validate(book_create)
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book

async def get_books(session: AsyncSession) -> list[Book]:
    statement = select(Book).options(selectinload(Book.genres), selectinload(Book.author))
    books = await session.exec(statement)
    return books.all()

async def get_book_by_id(session: AsyncSession, book_id: str) -> Book | None:
    book = await session.exec(select(Book).where(Book.id == book_id).options(selectinload(Book.genres), selectinload(Book.author)))
    return book.first()

async def get_book_by_slug(session: AsyncSession, slug: str) -> Book | None:
    statement = select(Book).where(Book.slug == slug).options(selectinload(Book.genres), selectinload(Book.author))
    books = await session.exec(statement)
    return books.first()

async def update_book(session: AsyncSession, book_id: str, book: BookUpdate) -> Book:
    book_data = book.model_dump()
    book_data = {k: v for k, v in book_data.items() if k in book.model_fields_set}
    current_book = await get_book_by_id(session, book_id)
    current_book.sqlmodel_update(book_data)
    if 'genre_ids' in book_data:
        genres = await session.exec(select(Genre).where(Genre.id.in_(book_data['genre_ids'])))
        current_book.genres = genres.all()
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