from sqlmodel import Field, SQLModel

from .traits import DateTimestamps


class FilmGenreBase(SQLModel):
    name: str


class FilmGenre(FilmGenreBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class FilmBase(SQLModel):
    name: str


class Film(FilmBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)
