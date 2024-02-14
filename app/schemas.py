from pydantic import BaseModel


class TokenData(BaseModel):
    username: str
    useremail: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str