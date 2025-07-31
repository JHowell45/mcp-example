from typing import TYPE_CHECKING, Any

from pgvector.sqlalchemy import Vector
from pydantic import computed_field
from sentence_transformers import SentenceTransformer
from sqlmodel import Field, Relationship, SQLModel

from .traits import DateTimestamps

if TYPE_CHECKING:
    from app.models.films import Film

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


class EmbeddingBase(SQLModel): ...


class Embedding(EmbeddingBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)
    embedding: Any = Field(sa_type=Vector(), repr=False)

    film_id: int = Field(foreign_key="film.id")
    film: "Film" = Relationship(back_populates="embedding")

    @computed_field
    @property
    def embedding_size(self) -> int:
        return len(self.embedding)


class FilmEmbeddingPublic(EmbeddingBase):
    id: int
    embedding_size: int
