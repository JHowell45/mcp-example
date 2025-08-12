import json
from ast import literal_eval
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from pandas import DataFrame, read_csv
from pydantic import BaseModel, Field, computed_field
from requests import get
from rich import print
from rich.progress import Progress
from sqlalchemy import delete
from sqlmodel import Session, col, func, select

from app.dependencies.db import engine
from app.models.films import (
    Film,
    FilmCollection,
    Genre,
    ProductionCompany,
    ProductionCountry,
    SpokenLanguage,
)
from app.models.vector_embeddings import Embedding, embedding_model

DATASET_URL: str = (
    "https://www.kaggle.com/api/v1/datasets/download/rounakbanik/the-movies-dataset"
)

SAVE_DIRECTORY: Path = Path("/app/datasets/")
FILENAME: str = "movies-dataset.zip"

SAVE_PATH: Path = SAVE_DIRECTORY / FILENAME

MOVIES_METADATA: Path = SAVE_DIRECTORY / "movies_metadata.csv"


def clean_data(unclean: DataFrame) -> DataFrame:
    df = unclean.replace({np.nan: None})
    df = df.drop_duplicates(["Series_Title"])
    return df


def reset_table(session: Session, reset: bool) -> bool:
    if count := session.exec(select(func.count(col(Film.id)))).one():
        print(count)
        if count > 0:
            if reset:
                print("Deleting all film data...")
                session.exec(delete(Film))
                session.commit()
                print("All Firm Data deleted!")
            else:
                print("Data already exists!")
                return True
    return False


def import_pipeline(filepath: Path, reset: bool):
    df: DataFrame = clean_data(read_csv(filepath))
    print(df)
    with Progress() as progress:
        with Session(engine) as session:
            if reset_table(session, reset):
                return
            pbar = progress.add_task("Importing Film CSV Data...", total=df.shape[0])
            for row in df.iterrows():
                data = FilmData(**row[1].to_dict())
                director = session.exec(
                    select(FilmDirector).where(FilmDirector.name == data.director)
                ).first()
                if director is None:
                    director = FilmDirector(name=data.director)

                created_film = Film(
                    name=data.title,
                    overview=data.overview,
                    release_year=data.release_year,
                    runtime_minutes=data.runtime_minutes,
                    imdb_rating=data.imdb_rating,
                    meta_score=data.meta_score,
                    director=director,
                )
                created_film.embedding = Embedding(
                    embedding=embedding_model.encode(created_film.embedding_text)
                )
                session.add(created_film)
                session.commit()
                progress.update(pbar, advance=1)


def download_datasets(chunk_size: int) -> None:
    if SAVE_PATH.exists():
        print("Zip file already exist!")
        return
    results = get(DATASET_URL, stream=True)
    with Progress() as progress:
        pbar = progress.add_task(
            "Downloading the movies dataset", total=len(results.content)
        )
        with open(SAVE_PATH, "wb") as file:
            for chunk in results.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                progress.update(pbar, advance=chunk_size)


def unzip_dataset() -> None:
    print("Extracting Dataset zip contents...")
    with ZipFile(SAVE_PATH, "r") as zip:
        zip.extractall(SAVE_DIRECTORY)
    print("Finished dataset zip file extraction!")


class SubMetaDataBase(BaseModel):
    name: str


class GenreMetaData(SubMetaDataBase): ...


class CollectionMetaData(SubMetaDataBase): ...


class ProductionCompanyMetaData(SubMetaDataBase): ...


class ProductionCountryMetaData(BaseModel):
    iso: str = Field(alias="iso_3166_1")
    name: str


class SpokenLanguageMetaData(BaseModel):
    iso: str = Field(alias="iso_639_1")
    name: str


class MovieMetaData(BaseModel):
    imdb_id: str
    title: str
    tagline: str | None
    overview: str
    popularity: float = Field(ge=0, le=100)
    budget: int
    revenue: int
    genres_data: str = Field(alias="genres", repr=False)
    collection_data: str | None = Field(alias="belongs_to_collection", repr=False)
    production_companies_data: str = Field(alias="production_companies", repr=False)
    production_countries_data: str = Field(alias="production_countries", repr=False)
    spoken_languages_data: str = Field(alias="spoken_languages", repr=False)
    release_date: datetime
    runtime: int
    status: str
    vote_avg: float = Field(alias="vote_average", ge=0, le=10)
    vote_count: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def genres(self) -> list[GenreMetaData]:
        return [
            GenreMetaData.model_validate(genre)
            for genre in json.loads(self.genres_data.replace("'", '"'))
        ]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def collection(self) -> CollectionMetaData | None:
        if not self.collection_data:
            return None
        return CollectionMetaData.model_validate(d)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def production_companies(self) -> list[ProductionCompanyMetaData]:
        return [
            ProductionCompanyMetaData.model_validate(company)
            for company in literal_eval(self.production_companies_data)
        ]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def production_countries(self) -> list[ProductionCountryMetaData]:
        return [
            ProductionCountryMetaData.model_validate(country)
            for country in literal_eval(self.production_countries_data)
        ]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def spoken_languages(self) -> list[SpokenLanguageMetaData]:
        return [
            SpokenLanguageMetaData.model_validate(language)
            for language in literal_eval(self.spoken_languages_data)
        ]


def clean_dataset(filepath: Path) -> DataFrame:
    df = read_csv(filepath)
    df.replace({np.nan: None}, inplace=True)
    df.dropna(subset=["overview"], inplace=True)
    return df


def create_db_model(data: MovieMetaData) -> Film:
    return Film(
        imdb_id=data.imdb_id,
        title=data.title,
        tagline=data.tagline,
        overview=data.overview,
        popularity=data.popularity,
        budget=data.budget,
        revenue=data.revenue,
        genres=[Genre.model_validate(genre) for genre in data.genres],
        production_companies=[
            ProductionCompany.model_validate(pc) for pc in data.production_companies
        ],
        production_countries=[
            ProductionCountry.model_validate(pc) for pc in data.production_countries
        ],
        spoken_languages=[
            SpokenLanguage.model_validate(sl) for sl in data.spoken_languages
        ],
        collection=FilmCollection.model_validate(data.collection)
        if data.collection
        else None,
    )


def import_dataset_metadata(reset: bool, save_size: int) -> None:
    current_size: int = 0
    df = clean_dataset(MOVIES_METADATA)
    print(df)
    print(df.columns)
    with Progress() as progress:
        pbar = progress.add_task("Importing movies metadata", total=len(df))
        with Session(engine) as session:
            if reset_table(session, reset):
                return
            for _, data in df.iterrows():
                print(data)
                parsed_data: MovieMetaData = MovieMetaData.model_validate(
                    data.to_dict()
                )
                print(parsed_data)

                # db_model = create_db_model(parsed_data)
                # print(db_model)
                # session.add(db_model)
                # current_size += 1
                # if current_size >= save_size:
                #     session.commit()
                #     current_size = 0
                progress.update(pbar, update=1)


def pipeline(reset: bool, chunk_size: int, save_size: int) -> None:
    download_datasets(chunk_size)
    unzip_dataset()
    import_dataset_metadata(reset, save_size)
