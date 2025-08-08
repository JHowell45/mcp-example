from sqlmodel import Field, Relationship, SQLModel

from .traits import DateTimestamps


class FilmGenreLink(SQLModel, table=True):
    genre_id: int = Field(foreign_key="genres.id", primary_key=True)
    film_id: int = Field(foreign_key="films.id", primary_key=True)


class Genre(SQLModel, table=True):
    __tablename__ = "genres"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    films: list["Film"] = Relationship(
        back_populates="genres", link_model=FilmGenreLink
    )


class ProductionCompany(SQLModel, table=True):
    __tablename__ = "production_companies"

    id: int | None = Field(default=None, primary_key=True)


class ProductionCountry(SQLModel, table=True):
    __tablename__ = "production_countries"

    id: int | None = Field(default=None, primary_key=True)
    iso: str = Field(unique=True)
    name: str = Field(unique=True)


class SpokenLanguage(SQLModel, table=True):
    __tablename__ = "spoken_languages"

    id: int | None = Field(default=None, primary_key=True)
    iso: str = Field(unique=True)
    name: str = Field(unique=True)


class FilmCollection(SQLModel, table=True):
    __tablename__ = "collections"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    films: list["Film"] = Relationship(back_populates="collection", cascade_delete=True)


class Film(DateTimestamps, table=True):
    __tablename__ = "films"

    id: int | None = Field(default=None, primary_key=True)
    imdb_id: str
    title: str
    tagline: str | None = Field(default=None)
    overview: str
    popularity: float = Field(ge=0, le=100)
    budget: int
    revenue: int

    collection_id: int | None = Field(default=None, foreign_key="", ondelete="CASCADE")
    collection: FilmCollection = Relationship(back_populates="films")

    genres: list[Genre] = Relationship(back_populates="films", link_model=FilmGenreLink)
