from pgvector.sqlalchemy import Vector
from sqlmodel import Field, SQLModel

from .traits import DateTimestamps


class EmbeddingBase(SQLModel): ...


class Embedding(EmbeddingBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)
    embedding: list[float] = Field(sa_type=Vector())
