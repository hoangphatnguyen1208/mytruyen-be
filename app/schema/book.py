from sqlmodel import SQLModel
from pydantic import ConfigDict
from app.schema.user import UserPublic
from app.schema.genre import GenrePublic
from app.schema.author import AuthorPublic

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
    status_id: int
    chapter_per_week: int
    published: bool
    synopsis: str
    note: str
    
class BookRegister(BookBase):
    author_id: uuid.UUID | None = None
    genre_ids: list[int]
    tag_ids: list[int]
    poster: Poster

class BookCreate(BookBase):
    author_id: uuid.UUID | None = None
    creator_id: uuid.UUID
    genre_ids: list[int]
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
    
    author: AuthorPublic | None
    creator: UserPublic
    genres: list[GenrePublic] 

class BookUpdate(SQLModel):
    name: str | None = None
    slug: str | None = None
    kind: int | None = None
    sex: int | None = None
    status_id: int | None = None
    chapter_per_week: int | None = None
    published: bool | None = None
    synopsis: str | None = None
    note: str | None = None
    genre_ids: list[uuid.UUID] | None = None
    tag_ids: list[uuid.UUID] | None = None
    poster: Poster | None = None



