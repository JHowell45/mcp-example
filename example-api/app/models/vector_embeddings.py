from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from pydantic import computed_field
from sqlmodel import Field, Relationship, SQLModel

from .traits import DateTimestamps

if TYPE_CHECKING:
    from app.models.films import Film


class EmbeddingBase(SQLModel): ...


class Embedding(EmbeddingBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)
    embedding: list[float] = Field(sa_type=Vector(), repr=False)

    film: "Film" = Relationship(back_populates="embedding")

    @computed_field
    @property
    def embedding_size(self) -> int:
        return len(self.embedding)


class FilmEmbeddingPublic(EmbeddingBase):
    id: int
    embedding_size: int
