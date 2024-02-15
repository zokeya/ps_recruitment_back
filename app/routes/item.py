from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database, utils

router = APIRouter(
    tags=["Item"]
)


@router.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item_route(item: schemas.ItemCreate, db: Session = Depends(database.get_db)):
    try:
        item_data = item.dict()
        item_created = utils.create_item(db, **item_data)
        return {"message": "Item created successfully", "item": item_created}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/items/{item_id}")
async def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(database.get_db)):
    results = {"item_id": item_id, "item": item}
    return results


@router.post("/offers/")
async def create_offer(offer: schemas.Offer, db: Session = Depends(database.get_db)):
    return offer
