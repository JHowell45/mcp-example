from pydantic import BaseModel


class FilmRelationshipBase(BaseModel):
    id: int
    name: str


class FilmCollectionPublic(FilmRelationshipBase): ...


class FilmGenrePublic(FilmRelationshipBase): ...


class FilmProductionCompanyPublic(FilmRelationshipBase): ...


class FilmProductionCountryPublic(FilmRelationshipBase): ...


class FilmSpokenLanguagePublic(FilmRelationshipBase): ...


class FilmPublic(BaseModel):
    id: int
    imdb_id: str | None
    title: str
    tagline: str | None
    overview: str
    popularity: float
    budget: int
    revenue: int
    collection: FilmCollectionPublic | None
    genres: list[FilmGenrePublic]
    production_companies: list[FilmProductionCompanyPublic]
    production_countries: list[FilmProductionCountryPublic]
    spoken_languages: list[FilmSpokenLanguagePublic]

    embedding_text: str
