from datetime import datetime

from pydantic import BaseModel


class FilmCollectionFilmPublic(BaseModel):
    id: int
    imdb_id: str | None
    title: str
    tagline: str | None
    popularity: float
    budget: int
    revenue: int


class FilmCollectionPublic(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    films: list[FilmCollectionFilmPublic]
