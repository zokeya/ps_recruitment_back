from pydantic import BaseModel,EmailStr, validator
from typing import List


class TokenData(BaseModel):
    username: str
    useremail: str | None = None


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    user_role_id: int

    @validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email cannot be empty")
        return value

    @validator("name")
    def validate_name(cls, value):
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @validator("password")
    def validate_password(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")
        return value

    @validator("user_role_id")
    def validate_user_role_id(cls, value):
        if value is None:
            raise ValueError("user_role_id cannot be None")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserCreate


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email cannot be empty")
        return value

    @validator("password")
    def validate_password(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")
        return value


class UserLoginResetModel(BaseModel):
    oldpassword: str
    newpassword: str


class UsernameResetModel(BaseModel):
    username: EmailStr

    @validator("username")
    def validate_name(cls, value):
        if not value:
            raise ValueError("Reset email cannot be empty")
        return value


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
