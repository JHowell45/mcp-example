from datetime import datetime

from sqlmodel import Field, SQLModel

from .traits import DateTimestamps


class SharedBase(SQLModel):
    name: str


class FilmGenreBase(SharedBase): ...


class FilmGenre(FilmGenreBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)


class FilmDirectorBase(SharedBase): ...


class FilmDirector(FilmDirectorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class FilmBase(SharedBase):
    overview: str | None = Field()
    release_year: int = Field(ge=1920)
    certificate: str = Field()
    runtime_minutes: int = Field(gt=0)
    imdb_rating: float = Field(ge=0, le=10)
    meta_score: int = Field(ge=0, le=100)


class Film(FilmBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)


class FilmPublic(FilmBase):
    id: int
    created_at: datetime
    updated_at: datetime


class FilmCreate(FilmBase): ...
