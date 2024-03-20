from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from app.database import engine, get_db
from app import models
from app.utils import get_items, create_item
from app.routes import item, auth, applicant

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Auth"])
app.include_router(item.router, tags=["Item"])
app.include_router(applicant.router, tags=["Applicant"])



@app.get('/')
def home(db: Session = Depends(get_db)):
    items = get_items(db)
    return {"data": items}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
