from datetime import datetime

from pydantic import computed_field
from sqlmodel import Field, Relationship, SQLModel

from .traits import DateTimestamps
from .vector_embeddings import Embedding, FilmEmbeddingPublic


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


class FilmDirector(FilmDirectorBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)

    films: list["Film"] = Relationship(back_populates="director")


class FilmDirectorPublic(FilmDirectorBase, PublicBase): ...


class FilmDirectorCreate(FilmDirectorBase): ...


class FilmBase(SharedBase):
    overview: str | None = Field()
    release_year: int = Field(ge=1920)
    runtime_minutes: int = Field(gt=0)
    imdb_rating: float = Field(ge=0, le=10)
    meta_score: int | None = Field(ge=0, le=100)


class Film(FilmBase, DateTimestamps, table=True):
    id: int | None = Field(default=None, primary_key=True)

    director_id: int = Field(foreign_key="filmdirector.id")
    director: FilmDirector = Relationship(back_populates="films")

    embedding_id: int | None = Field(default=None, foreign_key="embedding.id")
    embedding: Embedding | None = Relationship(back_populates="film")

    @computed_field(repr=True)
    @property
    def embedding_text(self) -> str:
        return f"The name of this film is '{self.name}' and it was released in {self.release_year} It is about {self.overview}. The film is {self.runtime_minutes} minutes long and has an IMDB rating of {self.imdb_rating} and a meta score of {self.meta_score}."


class FilmPublic(FilmBase, PublicBase):
    director: FilmDirectorPublic
    embedding_text: str
    embedding: FilmEmbeddingPublic | None


class FilmCreate(FilmBase):
    director: FilmDirectorCreate
