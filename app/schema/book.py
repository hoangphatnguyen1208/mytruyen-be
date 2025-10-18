from sqlmodel import SQLModel
from pydantic import ConfigDict
from app.models import book_status as BookStatus
from app.schema.user import UserPublic
from app.schema.genre import GenrePublic

from datetime import datetime
import uuid

class Poster(SQLModel):
    poster_default: str
    poster_600: str
    poster_300: str
    poster_150: str
class BookBase(SQLModel):
    name: str
    slug: str
    kind: int
    sex: int
    status: BookStatus
    chapter_per_week: int
    published: bool
    synopsis: str
    note: str
    

class BookRegister(BookBase):
    genre_ids: list[uuid.UUID]
    poster: Poster

class BookCreate(BookBase):
    author_id: uuid.UUID
    genre_ids: list[uuid.UUID]
    poster: dict

class BookPublic(BookBase):
    id: uuid.UUID
    latest_chapter: str | None
    view_count: int
    chapter_count: int
    word_count: int
    comment_count: int
    review_count: int
    average_rating: float
    bookmark_count: int
    poster: Poster
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None
    
    author: UserPublic
    genres: list[GenrePublic] 

class BookUpdate(SQLModel):
    name: str | None = None
    slug: str | None = None
    kind: int | None = None
    sex: int | None = None
    status: BookStatus | None = None
    chapter_per_week: int | None = None
    published: bool | None = None
    synopsis: str | None = None
    note: str | None = None
    genre_ids: list[uuid.UUID] | None = None



