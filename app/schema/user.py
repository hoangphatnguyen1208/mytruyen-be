from sqlmodel import SQLModel
from pydantic import EmailStr
from app.models import user_role as UserRole

import uuid

class UserBase(SQLModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True

class UserRegister(SQLModel):
    email: EmailStr
    password: str

class UserCreate(SQLModel):
    email: str
    password: str
    role: UserRole = UserRole.USER

class UserPublic(UserBase):
    id: uuid.UUID