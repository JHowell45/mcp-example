from sqlmodel import Field, Relationship

from .traits import DateTimestamps


class FilmGenreLink(DateTimestamps, table=True):
    genre_id: int = Field(foreign_key="genres.id", primary_key=True)
    film_id: int = Field(foreign_key="films.id", primary_key=True)


class FilmProductionCompanyLink(DateTimestamps, table=True):
    production_company_id: int = Field(
        foreign_key="production_companies.id", primary_key=True
    )
    film_id: int = Field(foreign_key="films.id", primary_key=True)


class FilmProductionCountryLink(DateTimestamps, table=True):
    production_country_id: int = Field(
        foreign_key="production_countries.id", primary_key=True
    )
    film_id: int = Field(foreign_key="films.id", primary_key=True)


class Genre(DateTimestamps, table=True):
    __tablename__ = "genres"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    films: list["Film"] = Relationship(
        back_populates="genres", link_model=FilmGenreLink
    )


class ProductionCompany(DateTimestamps, table=True):
    __tablename__ = "production_companies"

    id: int | None = Field(default=None, primary_key=True)

    films: list["Film"] = Relationship(
        back_populates="production_companies", link_model=FilmGenreLink
    )


class ProductionCountry(DateTimestamps, table=True):
    __tablename__ = "production_countries"

    id: int | None = Field(default=None, primary_key=True)
    iso: str = Field(unique=True)
    name: str = Field(unique=True)

    films: list["Film"] = Relationship(
        back_populates="production_countries", link_model=FilmGenreLink
    )


class SpokenLanguage(DateTimestamps, table=True):
    __tablename__ = "spoken_languages"

    id: int | None = Field(default=None, primary_key=True)
    iso: str = Field(unique=True)
    name: str = Field(unique=True)

    films: list["Film"] = Relationship(
        back_populates="spoken_language", link_model=FilmGenreLink
    )


class FilmCollection(DateTimestamps, table=True):
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

    collection_id: int = Field(
        foreign_key=f"{FilmCollection.__tablename__}.id", ondelete="CASCADE"
    )
    collection: FilmCollection = Relationship(back_populates="films")

    spoken_language_id: int = Field(
        foreign_key=f"{SpokenLanguage.__tablename__}.id", ondelete="CASCADE"
    )
    spoken_language: SpokenLanguage = Relationship(back_populates="films")

    genres: list[Genre] = Relationship(back_populates="films", link_model=FilmGenreLink)
    production_companies: list[ProductionCompany] = Relationship(
        back_populates="films", link_model=FilmProductionCompanyLink
    )
    production_countries: list[ProductionCountry] = Relationship(
        back_populates="films", link_model=FilmProductionCountryLink
    )
