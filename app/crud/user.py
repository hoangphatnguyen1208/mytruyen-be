import uuid
from app.schema import user
from sqlmodel import Session, select

from app.models import User

from app.schema.user import UserCreate

from app.core.security import get_password_hash, verify_password

def authenticate(session: Session, email: str, password: str) -> User | None:
    user_db = session.exec(select(User).where(User.email == email)).first()
    if not user_db:
        return None
    if not verify_password(password, user_db.hashed_password):
        return None
    return user_db

def create_user(session: Session, user_create: UserCreate):

    user = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_id(session: Session, user_id: uuid.UUID) -> User | None:
    return session.get(User, user_id)