import uuid
from sqlmodel import SQLModel
from datetime import datetime

class ChapterBase(SQLModel):
    book_id: uuid.UUID
    index: int
    name: str
    published: bool

class ChapterRegister(ChapterBase):
    pass

class ChapterCreate(ChapterBase):
    author_id: uuid.UUID

class ChapterUpdate(ChapterBase):
    book_id: uuid.UUID | None = None
    index: int | None = None
    name: str | None = None
    published: bool | None = None

class ChapterPublic(ChapterBase):
    id: uuid.UUID
    published_at: datetime | None
    word_count: int
    view_count: int
    comment_count: int
    created_at: datetime
    updated_at: datetime

class ChapterContentBase(SQLModel):
    content: str

class ChapterContentCreate(ChapterContentBase):
    chapter_id: uuid.UUID

class ChapterContentRegister(ChapterContentBase):
    pass

class ChapterContentUpdate(ChapterContentBase):
    content: str | None = None
    chapter_id: uuid.UUID | None = None

class ChapterContentPublic(ChapterContentBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
