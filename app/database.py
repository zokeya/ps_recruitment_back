from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
