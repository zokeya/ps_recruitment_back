from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import schemas, database, utils, oauth2, mailer

router = APIRouter(
    tags=["Auth"]
)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/signup", response_model=schemas.Token)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(database.get_db)
):
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = utils.create_user(db=db, user=user)
    access_token = oauth2.create_access_token(data={"username": new_user.email})

    return {"access_token": access_token, "token_type": "bearer", "user": new_user}


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = utils.get_user_by_email(db, user_credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not utils.verify_login(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    # access_token = oauth2.create_access_token(data={"user_id" : user.id})
    access_token = oauth2.create_access_token(data={"username": user.email})

    return {"access_token": access_token, "token_type": "bearer", "user":user}


@router.put("/forgot_pwd/", response_model=schemas.Message)
def reset_password_request(
        user_credentials: schemas.UsernameResetModel,
        db: Session = Depends(database.get_db)
):
    # Check if the user with the specified email exists
    user = utils.get_user_by_email(db, email=user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the specified email does not exist",
        )

    # Generate a unique token or link (you can use a library like PyJWT for tokens)
    reset_token = utils.generate_reset_token(user.email)

    # Save the reset token in the database
    utils.save_reset_token(db, user.id, reset_token)

    # Send the reset link to the user's email
    mailer.send_password_reset_email(user.email, reset_token)

    return {"message": "Password reset link sent to your email"}


@router.put("/reset-password/", response_model=schemas.Token)
def reset_password(
        reset_token: str,
        new_password: str,
        db: Session = Depends(database.get_db)
):
    user = utils.get_user_by_reset_token(db, reset_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired reset token",
        )

    # Update the user's password
    hashed_password = utils.hash(new_password)
    user.password = hashed_password
    user.reset_token = None
    db.commit()

    # Generate a new access token for the user
    access_token = oauth2.create_access_token(data={"username": user.email})

    return {"access_token": access_token, "token_type": "bearer", "user": user}
