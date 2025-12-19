from sqlmodel import SQLModel
from pydantic import BaseModel
from app.schema.book import BookPublic
from typing import Any, TypeVar, Generic

class Pagination(SQLModel):
    current: int
    next: int | None = None
    previous: int | None = None
    last: int
    limit: int
    total: int

T = TypeVar("T")

class ResponseList(BaseModel, Generic[T]):
    status_code: int
    success: bool
    message: str
    data: list[T] | None = None

class Response(BaseModel, Generic[T]):
    status_code: int
    success: bool
    message: str
    data: T | None = None

