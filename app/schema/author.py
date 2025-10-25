from sqlmodel import SQLModel
from datetime import datetime

class AuthorBase(SQLModel):
    name: str
    local_name: str | None = None
    avatar: str | None = None

class AuthorCreate(AuthorBase):
    pass

class AuthorPublic(AuthorBase):
    id: str
    created_at: datetime
    updated_at: datetime