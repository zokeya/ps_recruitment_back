from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
import json

from app import schemas, models
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify_login(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_pwd_from_email(email: str):
    username, domain = email.split("@")
    first_name = username[0].upper()
    last_name = username.split(".")[1].lower()
    generated_password = first_name[0] + last_name + "@gsl"
    return generated_password


def generate_reset_token(email: str) -> str:
    to_encode = {"sub": email, "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def save_reset_token(db: Session, user_id: int, reset_token: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.reset_token = reset_token
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def run_sql_query(query: str, db: Session):
    try:
        result = db.execute(text(query))
        return result.fetchall()
    finally:
        db.close()


# Example query
def get_items(db: Session):
    sql_query = "SELECT * FROM items;"
    result = run_sql_query(sql_query, db)
    return result


def create_item(db: Session, name: str, description: str, price: float, tax: float, tags: List[str], image: dict):
    db_item = models.Item(
        name=name,
        description=description,
        price=price,
        tax=tax,
        tags=json.dumps(tags),
        image=json.dumps(image)  # Convert the image dictionary to JSON
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# def create_item(db: Session, name: str, description: str, price: float, tax: float, tags: List[str], image: dict):
#     image_url = image.get("url", "")
#     image_name = image.get("name", "")
#     db_item = Item(name=name, description=description, price=price, tax=tax, tags=json.dumps(tags), image=f"{image_url},{image_name}")
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# def create_new_user(db: Session, user: schemas.UserCreate):
#     password_gen = generate_pwd_from_email(user.email)
#
#     hashed_password = hash(password_gen)
#     db_user = models.User(
#         name=user.name,
#         email=user.email,
#         password=hashed_password,
#         user_role_id=user.user_role_id
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#
#     return db_user

def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        user_role_id=user.user_role_id
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_reset_token(db: Session, reset_token: str):
    return db.query(models.User).filter(models.User.reset_token == reset_token).first()