from sqlmodel import SQLModel

class Token(SQLModel):
    access_token: str
    token_type: str

class UserLogin(SQLModel):
    email: str
    password: str

class UserRegister(SQLModel):
    email: str
    password: str

class Message(SQLModel):
    message: str