from pydantic import EmailStr, SecretStr, computed_field
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlmodel import Column, Field, SQLModel, String

from app.dependencies.auth.users import hash_secret
from app.dependencies.config import get_settings

from .traits import DateTimestamps


class UserBase(SQLModel):
    email: EmailStr = Field(nullable=False)


class User(UserBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(
        min_length=20,
        max_length=128,
        exclude=True,
        sa_column=Column(
            StringEncryptedType(
                String, get_settings().ENCRYPTION_KEY, AesEngine, "pkcs5"
            ),
            nullable=False,
        ),
    )


class UserCreate(UserBase):
    password: SecretStr

    @computed_field  # type: ignore[prop-decorator]
    @property
    def hashed_password(self) -> str:
        return hash_secret(self.password.get_secret_value())
