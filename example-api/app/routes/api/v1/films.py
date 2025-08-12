from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from sqlmodel import select

from app.dependencies.db import SessionDep
from app.models.films import Film
from app.routes.route_tags import RouteTags

from .responses.films import FilmEmbeddingTextPublic, FilmPublic

router = APIRouter(prefix="/films", tags=[RouteTags.FILMS])


@router.get("/", response_model=list[FilmPublic])
def all_films(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return session.exec(select(Film).offset(offset).limit(limit)).all()


@router.get("/embedding-texts", response_model=list[FilmEmbeddingTextPublic])
def all_films_embedding(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return session.exec(select(Film).offset(offset).limit(limit)).all()


@router.get("/{film_id}", response_model=FilmPublic)
def get_film(film_id: int, session: SessionDep) -> Film:
    if db_model := session.get(Film, film_id):
        return db_model
    raise HTTPException(status_code=404, detail="Item not found")
