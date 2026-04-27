from os import getenv

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=getenv("ENV_FILE", ".env"))


settings = Settings()
