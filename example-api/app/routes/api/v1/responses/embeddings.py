from app.models.vector_embeddings import EmbeddingBase


class EmbeddingPublic(EmbeddingBase):
    id: int
    embedding_size: int
