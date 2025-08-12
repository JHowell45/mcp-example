from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import select

from app.dependencies.db import SessionDep
from app.models.films import FilmCollection
from app.routes.route_tags import RouteTags

from .responses.film_collections import FilmCollectionPublic

router = APIRouter(prefix="/films-collections", tags=[RouteTags.FILMS_COLLECTIONS])


@router.get("/", response_model=list[FilmCollectionPublic])
def all_film_collections(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[FilmCollection]:
    return session.exec(select(FilmCollection).offset(offset).limit(limit)).all()
