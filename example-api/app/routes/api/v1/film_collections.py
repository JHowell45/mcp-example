from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import select

from app.dependencies.db import SessionDep
from app.models.films import FilmCollection
from app.routes.api.route_tags import RouteTags

router = APIRouter(prefix="/films-collections", tags=[RouteTags.FILMS_COLLECTIONS])


@router.get("/")
def all_film_collections(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return session.exec(select(FilmCollection).offset(offset).limit(limit)).all()
