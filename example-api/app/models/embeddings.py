from typing import TYPE_CHECKING, Any

from pgvector.sqlalchemy import Vector
from pydantic import computed_field
from sentence_transformers import SentenceTransformer
from sqlmodel import Field, Relationship, SQLModel  # noqa

from .traits import DateTimestamps

if TYPE_CHECKING:
    from app.models.films import Film

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
EMBEDDING_SIZE: int = 384


class FilmEmbedding(DateTimestamps, table=True):
    __tablename__ = "films_embeddings"

    id: int | None = Field(default=None, primary_key=True)
    embedding: Any = Field(sa_type=Vector(EMBEDDING_SIZE))

    film_id: int = Field(foreign_key="films.id", ondelete="CASCADE")
    film: "Film" = Relationship(back_populates="embeddings")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def embedding_size(self) -> int:
        return len(self.embedding)
