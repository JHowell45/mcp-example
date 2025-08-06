from pathlib import Path
from zipfile import ZipFile

import numpy as np
from pandas import DataFrame, read_csv
from pydantic import BaseModel, Field
from requests import get
from rich import print
from rich.progress import Progress
from sqlalchemy import delete
from sqlmodel import Session, col, func, select

from app.dependencies.db import engine
from app.models.films import Film, FilmDirector
from app.models.vector_embeddings import Embedding, embedding_model

DATASET_URL: str = (
    "https://www.kaggle.com/api/v1/datasets/download/rounakbanik/the-movies-dataset"
)

SAVE_DIRECTORY: Path = Path("/app/datasets/")
FILENAME: str = "movies-dataset.zip"

SAVE_PATH: Path = SAVE_DIRECTORY / FILENAME

MOVIES_METADATA: Path = SAVE_DIRECTORY / "movies_metadata.csv"


class FilmData(BaseModel):
    title: str = Field(alias="Series_Title")
    overview: str = Field(alias="Overview")
    release_year: int = Field(alias="Released_Year")
    imdb_rating: float = Field(alias="IMDB_Rating", ge=0, le=10)
    meta_score: int | None = Field(alias="Meta_score", ge=0, le=100)
    director: str = Field(alias="Director")

    runtime_pre: str = Field(alias="Runtime", repr=False)
    runtime_minutes: int | None = None
    genre_data: str = Field(alias="Genre", repr=False)
    genres: list[str] = Field(default_factory=list)

    def model_post_init(self, _) -> None:
        self.runtime_minutes: int = int(self.runtime_pre.split(" ")[0])
        self.genres: list[str] = [genre.strip() for genre in self.genre_data.split(",")]


def clean_data(unclean: DataFrame) -> DataFrame:
    df = unclean.replace({np.nan: None})
    df = df.drop_duplicates(["Series_Title"])
    return df


def import_pipeline(filepath: Path, reset: bool):
    df: DataFrame = clean_data(read_csv(filepath))
    print(df)
    with Progress() as progress:
        with Session(engine) as session:
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


def import_dataset_metadata() -> None:
    df = read_csv(MOVIES_METADATA)
    print(df)


def pipeline(chunk_size: int = 100) -> None:
    download_datasets(chunk_size)
    unzip_dataset()
    import_dataset_metadata()
