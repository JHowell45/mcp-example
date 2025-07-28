from sqlmodel import Field, SQLModel

from .traits import DateTimestamps


class SharedBase(SQLModel):
    name: str


class FilmGenreBase(SharedBase): ...


class FilmGenre(FilmGenreBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class FilmBase(SharedBase): ...


class Film(FilmBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)
