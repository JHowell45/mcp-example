from typing import TYPE_CHECKING, Self

from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer
from sqlmodel import Field, Relationship, SQLModel

from .traits import DateTimestamps

if TYPE_CHECKING:
    from app.models.films import Film


class EmbeddingBase(SQLModel): ...


class Embedding(EmbeddingBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)
    embedding: list[float] = Field(sa_type=Vector())

    film: "Film" = Relationship(back_populates="embedding")

    @classmethod
    def from_text(cls, text: str) -> Self:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls(embedding=model.encode(text))


class FilmEmbeddingPublic(EmbeddingBase):
    id: int
    embedding: list[float]
