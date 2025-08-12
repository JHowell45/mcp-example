from fastapi import APIRouter
from pydantic import BaseModel, computed_field
from sqlmodel import select

from app.dependencies.db import SessionDep
from app.models.embeddings import FilmEmbedding, embedding_model
from app.routes.route_tags import RouteTags

from .responses.embeddings import EmbeddingPublic

router = APIRouter(prefix="/vector", tags=[RouteTags.VECTOR])


class VectorSearchRequest(BaseModel):
    query: str
    limit: int = 10

    @computed_field
    @property
    def query_embedding(self) -> list[float]:
        return embedding_model.encode(self.query)


@router.post("/search", response_model=list[EmbeddingPublic])
def vector_search(
    session: SessionDep, request: VectorSearchRequest
) -> list[FilmEmbedding]:
    # return session.exec(
    #     select(FilmEmbedding).order_by(
    #         FilmEmbedding.embedding.l2_distance(request.query_embedding)
    #     )
    # ).limit(request.limit)
    return session.exec(
        select(FilmEmbedding)
        .order_by(FilmEmbedding.embedding.l2_distance(request.query_embedding))
        .limit(request.limit)
    ).all()
