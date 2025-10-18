from sqlmodel import SQLModel, Field, Relationship
import uuid
from sqlalchemy import Column, func, MetaData
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import JSONB


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
SQLModel.metadata = metadata

class user_role(str, Enum):
    __enum_name__ = "user_role"
    USER = "user"
    ADMIN = "admin"


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    full_name: str | None = Field(default=None)
    role: user_role = Field(default=user_role.USER,nullable=False)
    created_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

    books: list["Book"] = Relationship(back_populates="author")

class book_status(str, Enum):
    __enum_name__ = "book_status"
    ONGOING = "Còn tiếp"
    COMPLETED = "Hoàn thành"
    PAUSED = "Tạm dừng"

class GenreBook(SQLModel, table=True):
    __tablename__ = "genre_book"
    genre_id: uuid.UUID = Field(foreign_key="genre.id", nullable=False, primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="book.id", nullable=False, primary_key=True)

class Book(SQLModel, table=True):
    __tablename__ = "book"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    author_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    name: str = Field(index=True, nullable=False)
    slug: str = Field(index=True, unique=True, nullable=False)
    kind: int = Field(index=True, nullable=False)
    sex: int = Field(index=True, nullable=False)
    status: book_status = Field(index=True, nullable=False)
    chapter_per_week: int = Field(default=0, nullable=False)
    published: bool = Field(default=False, nullable=False)
    latest_chapter: uuid.UUID | None = Field(default=None)
    synopsis: str = Field(nullable=False)
    view_count: int = Field(default=0, nullable=False)
    chapter_count: int = Field(default=0, nullable=False)
    word_count: int = Field(default=0, nullable=False)
    comment_count: int = Field(default=0, nullable=False)
    review_count: int = Field(default=0, nullable=False)
    average_rating: float = Field(default=0.0, nullable=False)
    bookmark_count: int = Field(default=0, nullable=False)
    poster: dict = Field(sa_column=Column(JSONB))
    note: str = Field(nullable=False)
    created_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})
    published_at: datetime | None = Field(default=None)

    genres: list["Genre"] = Relationship(back_populates="books", link_model=GenreBook, sa_relationship_kwargs={"lazy": "selectin"})
    author: User = Relationship(back_populates="books", sa_relationship_kwargs={"lazy": "selectin"})

class Genre(SQLModel, table=True):
    __tablename__ = "genre"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    slug: str = Field(index=True, unique=True, nullable=False)
    description: str | None = Field(default=None)
    created_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

    books: list[Book] = Relationship(back_populates="genres", link_model=GenreBook)


class Chapter(SQLModel, table=True):
    __tablename__ = "chapter"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    author_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    book_id: uuid.UUID = Field(foreign_key="book.id", nullable=False)
    name: str = Field(index=True, nullable=False)
    index: int = Field(nullable=False, unique=True)
    word_count: int = Field(default=0, nullable=False)
    view_count: int = Field(default=0, nullable=False)
    comment_count: int = Field(default=0, nullable=False)
    published: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})
    published_at: datetime | None = Field(default=None)

    chapter_content: "ChapterContent" = Relationship(back_populates="chapter")
    comments: list["Comment"] = Relationship(back_populates="chapter")

class ChapterContent(SQLModel, table=True):
    __tablename__ = "chapter_content"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    chapter_id: uuid.UUID = Field(foreign_key="chapter.id", nullable=False, unique=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})
    
    chapter: "Chapter" = Relationship(back_populates="chapter_content")

class Comment(SQLModel, table=True):
    __tablename__ = "comment"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    chapter_id: uuid.UUID = Field(foreign_key="chapter.id", nullable=False)
    parent_id: uuid.UUID | None = Field(default=None, foreign_key="comment.id")
    content: str = Field(nullable=False)
    created_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})
    
    chapter: "Chapter" = Relationship(back_populates="comments")

class Review(SQLModel, table=True):
    __tablename__ = "review"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    book_id: uuid.UUID = Field(foreign_key="book.id", nullable=False)
    rating: int = Field(nullable=False)
    content: str | None = Field(default=None)
    created_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})