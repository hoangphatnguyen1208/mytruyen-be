from sqlmodel import SQLModel
from app.schema.book import BookPublic


class Pagination(SQLModel):
    current: int
    next: int | None = None
    previous: int | None = None
    last: int
    limit: int
    total: int

class Response(SQLModel):
    status_code: int = 200
    success: bool
    message: str

class BookResponse(Response):
    data: BookPublic | None = None

class BooksResponse(Response):
    data: list[BookPublic] | None = None
    pagination: Pagination | None = None

