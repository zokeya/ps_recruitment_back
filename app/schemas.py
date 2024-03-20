from datetime import datetime

from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional


class TokenData(BaseModel):
    username: str
    useremail: str | None = None


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


class UserCreate(UserLogin):
    name: str
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


class Qualification(BaseModel):
    qualification_type: str
    qualification_name: str
    institution: str
    completion_date: datetime


class Skill(BaseModel):
    skill_name: str
    experience_years: int
    proficiency_level: str


class ApplicantBase(BaseModel):
    first_name: str
    other_names: str
    phone_number: str
    address: str
    qualifications: Optional[List[Qualification]] = None
    skills: Optional[List[Skill]] = None


class Applicant(ApplicantBase):
    user: UserLogin

