from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from config import settings
from typing import Annotated
from sqlalchemy.orm import Session

from app import schemas, database, models

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class TokenVerificationError(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate" : "Bearer"}
        )


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=1)

    to_encode.update({"exp":expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return  encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("username")

        if username is None:
            raise credentials_exception

        token_data = schemas.TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception

async def get_current_user(token: Annotated[str: Depends(oauth2_scheme)], db: Session = Depends(database.get_db())):
    credentials_exception = TokenVerificationError()
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.email == token_data.username).first()
    return user


async def get_current_admin_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    credentials_exception = TokenVerificationError(detail="You are not authorized to perform this action")

    token_data = verify_access_token(token, credentials_exception)
    admin_user = (
        db.query(models.User)
        .filter(models.User.email == token_data.username, models.User.user_role_id == 1)
        .first()
    )

    if not admin_user:
        raise credentials_exception

    return admin_user
