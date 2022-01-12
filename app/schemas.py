from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import EmailStr


class Post(BaseModel):
    title: str
    body: str
    publish: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

