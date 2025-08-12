from pydantic import computed_field
from sqlalchemy import BigInteger, Column
from sqlmodel import Field, Relationship, SQLModel

from app.models.embeddings import FilmEmbedding

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


class FilmSpokenLanguageLink(DateTimestamps, table=True):
    spoken_language_id: int = Field(foreign_key="spoken_languages.id", primary_key=True)
    film_id: int = Field(foreign_key="films.id", primary_key=True)


class FilmRelationshipBase(SQLModel):
    name: str = Field(unique=True)


class Genre(FilmRelationshipBase, DateTimestamps, table=True):
    __tablename__ = "genres"

    id: int | None = Field(default=None, primary_key=True)

    films: list["Film"] = Relationship(
        back_populates="genres", link_model=FilmGenreLink
    )


class ProductionCompany(FilmRelationshipBase, DateTimestamps, table=True):
    __tablename__ = "production_companies"

    id: int | None = Field(default=None, primary_key=True)

    films: list["Film"] = Relationship(
        back_populates="production_companies", link_model=FilmProductionCompanyLink
    )


class ProductionCountry(FilmRelationshipBase, DateTimestamps, table=True):
    __tablename__ = "production_countries"

    id: int | None = Field(default=None, primary_key=True)
    iso: str = Field(unique=True)

    films: list["Film"] = Relationship(
        back_populates="production_countries", link_model=FilmProductionCountryLink
    )


class SpokenLanguage(FilmRelationshipBase, DateTimestamps, table=True):
    __tablename__ = "spoken_languages"

    id: int | None = Field(default=None, primary_key=True)
    iso: str = Field(unique=True)

    films: list["Film"] = Relationship(
        back_populates="spoken_languages", link_model=FilmSpokenLanguageLink
    )


class FilmCollection(FilmRelationshipBase, DateTimestamps, table=True):
    __tablename__ = "collections"
    id: int | None = Field(default=None, primary_key=True)

    films: list["Film"] = Relationship(back_populates="collection", cascade_delete=True)


class Film(DateTimestamps, table=True):
    __tablename__ = "films"

    id: int | None = Field(default=None, primary_key=True)
    imdb_id: str | None = Field(nullable=True)
    title: str
    tagline: str | None = Field(default=None)
    overview: str
    popularity: float = Field(ge=0)
    budget: int = Field(sa_column=Column(BigInteger()))
    revenue: int = Field(sa_column=Column(BigInteger()))

    collection_id: int | None = Field(
        default=None,
        foreign_key=f"{FilmCollection.__tablename__}.id",
        ondelete="CASCADE",
    )
    collection: FilmCollection = Relationship(back_populates="films")

    genres: list[Genre] = Relationship(back_populates="films", link_model=FilmGenreLink)
    production_companies: list[ProductionCompany] = Relationship(
        back_populates="films", link_model=FilmProductionCompanyLink
    )
    production_countries: list[ProductionCountry] = Relationship(
        back_populates="films", link_model=FilmProductionCountryLink
    )
    spoken_languages: list[SpokenLanguage] = Relationship(
        back_populates="films", link_model=FilmSpokenLanguageLink
    )

    embeddings: list[FilmEmbedding] = Relationship(
        back_populates="film", cascade_delete=True
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def embedding_text(self) -> str:
        text: str = f"The films title is '{self.title}'."
        if self.tagline:
            text += f" The film's tagline is: {self.tagline}."
        text += f" {self.overview}. The film has a popularity score of: {self.popularity}. The film's budget was {self.budget} and the revenue generated was {self.revenue}."
        if self.collection:
            text += f" This film is part of the {self.collection.name} collection."
        if self.genres:
            text += f" This film's genres are: {', '.join([model.name for model in self.genres])}."
        if self.production_companies:
            text += f" This film was produced by: {', '.join([model.name for model in self.production_companies])}."
        if self.production_countries:
            text += f" This film was produced in the following coutries: {', '.join([model.name for model in self.production_countries])}."
        if self.spoken_languages:
            text += f" The following languages can be heard in this film: {', '.join([model.name for model in self.spoken_languages])}"
        return text
