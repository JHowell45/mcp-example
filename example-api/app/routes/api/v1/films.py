from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import select

from app.dependencies.db import SessionDep
from app.models.films import Film

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/")
def all_films(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return session.exec(select(Film).offset(offset).limit(limit)).all()
