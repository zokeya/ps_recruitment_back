import os
from pydantic import BaseModel, Field, ValidationError
from pydantic.fields import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False, env_file="../.env", env_file_encoding='utf-8')
    extra: ClassVar[str] = "allow"

    database_url: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 1

    smtp_server: str
    smtp_port: int
    sender_email: str
    sender_password: str

    server_url: str

    # database_url: str = os.getenv("DATABASE_URL")
    # database_name: str = os.getenv("DATABASE_NAME")
    # secret_key: str = os.getenv("SECRET_KEY")
    # algorithm: str = os.getenv("ALGORITHM")
    # access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1))


def get_settings():
    try:
        return Settings()
    except ValidationError as e:
        print(f"Validation error in settings: {e}")
        raise


settings = get_settings()
