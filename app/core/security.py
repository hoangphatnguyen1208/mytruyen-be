import jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta
from typing import Optional

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

def create_access_token(subject: Optional[str], expires_delta: timedelta) -> str:
    expires = datetime.now() + expires_delta
    to_encode = {"exp": expires, "sub": subject} 
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

