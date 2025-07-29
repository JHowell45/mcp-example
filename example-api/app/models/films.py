from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from .traits import DateTimestamps


class PublicBase(SQLModel):
    id: int
    created_at: datetime
    updated_at: datetime


class SharedBase(SQLModel):
    name: str = Field(unique=True)


class FilmGenreBase(SharedBase): ...


class FilmGenre(FilmGenreBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)


class FilmGenrePublic(FilmGenreBase, PublicBase): ...


class FilmDirectorBase(SharedBase): ...


class FilmDirector(FilmDirectorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    films: list["Film"] = Relationship(back_populates="director")


class FilmDirectorPublic(FilmDirectorBase, PublicBase): ...


class FilmDirectorCreate(FilmDirectorBase): ...


class FilmBase(SharedBase):
    overview: str | None = Field()
    release_year: int = Field(ge=1920)
    runtime_minutes: int = Field(gt=0)
    imdb_rating: float = Field(ge=0, le=10)
    meta_score: int = Field(ge=0, le=100)


class Film(FilmBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)

    director_id: int = Field(foreign_key="filmdirector.id")
    director: FilmDirector = Relationship(back_populates="films")


class FilmPublic(FilmBase, PublicBase):
    director: FilmDirectorPublic


class FilmCreate(FilmBase):
    director: FilmDirectorCreate
