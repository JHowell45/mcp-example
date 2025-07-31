from app.models.films import FilmBase, FilmDirectorPublic, PublicBase
from app.models.vector_embeddings import EmbeddingBase


class EmbeddingFilmPublic(FilmBase, PublicBase):
    director: FilmDirectorPublic


class EmbeddingPublic(EmbeddingBase):
    id: int
    embedding_size: int
    film: EmbeddingFilmPublic
