from pydantic import BaseModel


class EmbeddingFilmPublic(BaseModel):
    id: int
    imdb_id: str | None
    title: str
    embedding_text: str


class EmbeddingPublic(BaseModel):
    id: int
    film: EmbeddingFilmPublic
