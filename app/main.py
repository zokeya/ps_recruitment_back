from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import uvicorn

from app.database import engine, get_db
from app import models
from app.utils import get_items, create_item
from app.config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item_route(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        item_data = item.dict()
        item_created = create_item(db, **item_data)
        return {"message": "Item created successfully", "item": item_created}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers/")
async def create_offer(offer: Offer, db: Session = Depends(get_db)):
    return offer


@app.get('/')
def home(db: Session = Depends(get_db)):
    items = get_items(db)
    return {"data": items}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
