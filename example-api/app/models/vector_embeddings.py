from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlmodel import Field, Relationship, SQLModel

from .traits import DateTimestamps

if TYPE_CHECKING:
    from app.models.films import Film


class EmbeddingBase(SQLModel): ...


class Embedding(EmbeddingBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)
    embedding: list[float] = Field(sa_type=Vector())

    film: "Film" = Relationship(back_populates="embedding")


class FilmEmbeddingPublic(EmbeddingBase):
    id: int
    embedding: list[float]
