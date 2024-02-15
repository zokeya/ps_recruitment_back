from pydantic import BaseModel
from typing import List


class TokenData(BaseModel):
    username: str
    useremail: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    user_role_id: int


class UserLogin(BaseModel):
    email: str
    password: str


class UserLoginResetModel(BaseModel):
    oldpassword: str
    newpassword: str


class UsernameResetModel(BaseModel):
    username: str


class Message(BaseModel):
    message: str


class Image(BaseModel):
    url: str
    name: str


# tags_create = List[str]
class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    tax: float
    tags: List[str]
    image: Image


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[ItemCreate] | None = None
