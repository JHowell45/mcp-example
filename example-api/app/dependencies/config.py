from typing import Annotated

from fastapi import Depends
from pydantic import Field, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # General:
    ENCRYPTION_KEY: str = Field(alias="API_ENCRYPTION_KEY")

    # Database:
    DB_HOST: str = Field(alias="API_DB_HOST")
    DB_PORT: int = Field(alias="API_DB_PORT")
    DB_USER: str = Field(alias="API_DB_USER")
    DB_PASSWORD: str = Field(alias="API_DB_PASSWORD")
    DB_NAME: str = Field(alias="API_DB_NAME")
    DB_ENABLE_SSL: bool = Field(alias="API_DB_ENABLE_SSL", default=False)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URI(self) -> PostgresDsn:
        path: str = self.DB_NAME
        if self.DB_ENABLE_SSL:
            path += "?sslmode=require"
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=path,
        )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
