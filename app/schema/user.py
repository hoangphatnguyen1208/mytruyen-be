from sqlmodel import SQLModel
from pydantic import EmailStr

import uuid

class UserBase(SQLModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserRegister(SQLModel):
    email: EmailStr
    password: str

class UserPublic(UserBase):
    id: uuid.UUID