from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import select

from app.dependencies.db import SessionDep
from app.models.films import Film, FilmCreate, FilmPublic

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/", response_model=list[FilmPublic])
def all_films(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return session.exec(select(Film).offset(offset).limit(limit)).all()


@router.post("/", response_model=FilmPublic)
def create_film(session: SessionDep, request: FilmCreate):
    if db_film := Film.model_validate(request):
        session.add(db_film)
        session.commit()
        session.refresh(db_film)
        return db_film
