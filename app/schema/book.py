from sqlmodel import SQLModel
from app.models import book_status as BookStatus

from datetime import datetime
import uuid
class BookBase(SQLModel):
    name: str
    slug: str
    kind: int
    sex: int
    status: BookStatus
    chapter_per_week: int
    published: bool
    synopsis: str 

class BookRegister(BookBase):
    pass

class BookCreate(BookBase):
    author_id: uuid.UUID

class BookPublic(BookBase):
    id: uuid.UUID
    author_id: uuid.UUID
    latest_chapter: str | None
    view_count: int
    chapter_count: int
    word_count: int
    comment_count: int
    review_count: int
    average_rating: float
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None

class BookUpdate(BookBase):
    name: str | None
    slug: str | None
    kind: int | None
    sex: int | None
    status: BookStatus | None
    chapter_per_week: int | None
    published: bool | None
    synopsis: str | None



