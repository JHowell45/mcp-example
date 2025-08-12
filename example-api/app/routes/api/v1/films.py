from typing import Annotated

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel, Field
from sqlmodel import select

from app.dependencies.db import SessionDep
from app.models.embeddings import Embedding, embedding_model
from app.models.films import Film
from app.routes.api.v1.responses.embeddings import EmbeddingPublic

from .responses.films import FilmPublic

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/", response_model=list[FilmPublic])
def all_films(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return session.exec(select(Film).offset(offset).limit(limit)).all()


@router.post("/")
def create_film(session: SessionDep, request: Request):
    if db_film := Film.model_validate(request):
        session.add(db_film)
        session.commit()
        session.refresh(db_film)
        return db_film


class FilmVectorSearchRequest(BaseModel):
    query: str
    limit: int = Field(default=5)


@router.post("/vector/search", response_model=list[EmbeddingPublic])
def film_vector_search(session: SessionDep, request: FilmVectorSearchRequest):
    query_embedding = embedding_model.encode(request.query)
    return session.exec(
        select(Embedding)
        .order_by(Embedding.embedding.l2_distance(query_embedding))
        .limit(request.limit)
    )
