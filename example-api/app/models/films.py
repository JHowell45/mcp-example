from sqlmodel import Field, SQLModel

from .traits import DateTimestamps


class SharedBase(SQLModel):
    name: str


class FilmGenreBase(SharedBase): ...


class FilmGenre(FilmGenreBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)


class FilmBase(SharedBase):
    description: str | None = Field(default=None, nullable=True)
    rating: int | None = Field(default=None, ge=0, le=5, nullable=True)


class Film(FilmBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)
