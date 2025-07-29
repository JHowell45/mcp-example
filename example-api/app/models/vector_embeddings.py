from sqlmodel import Field, SQLModel


class EmbeddingBase(SQLModel): ...


class Embedding(EmbeddingBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
