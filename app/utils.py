from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from passlib.context import CryptContext
import json

from app.models import Item, User

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
    db_item = Item(
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

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
