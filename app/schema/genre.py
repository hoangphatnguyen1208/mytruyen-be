from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class GenreBase(SQLModel):
    name: str
    slug: str
    description: str | None = Field(default=None)

class GenreCreate(GenreBase):
    pass

class GenreRegister(GenreBase):
    pass

class GenreUpdate(SQLModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None

class GenrePublic(GenreBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
