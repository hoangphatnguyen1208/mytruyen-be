from sqlmodel import SQLModel, Field, Relationship
import uuid
from sqlalchemy import func
from datetime import datetime

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    full_name: str | None = Field(default=None)
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

class Book(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, nullable=False)
    slug: str = Field(index=True, unique=True, nullable=False)
    kind: int = Field(index=True, nullable=False)
    sex: int = Field(index=True, nullable=False)
    status: int = Field(index=True, nullable=False)
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})
    
class Chapter(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="book.id", nullable=False)
    name: str = Field(index=True, nullable=False)
    index: int = Field(nullable=False)
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

class ChapterContent(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True)
    chapter_id: uuid.UUID = Field(foreign_key="chapter.id", nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})