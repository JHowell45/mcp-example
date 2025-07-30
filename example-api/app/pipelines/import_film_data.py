from pathlib import Path

import numpy as np
from pandas import DataFrame, read_csv
from pydantic import BaseModel, Field
from rich import print
from rich.progress import Progress
from sqlmodel import Session, select

from app.dependencies.db import engine
from app.models.films import Film, FilmDirector


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


def import_pipeline(filepath: Path):
    df: DataFrame = clean_data(read_csv(filepath))
    print(df)
    with Progress() as progress:
        pbar = progress.add_task("Importing Film CSV Data...", total=df.shape[0])
        with Session(engine) as session:
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
                session.add(created_film)
                session.commit()
                progress.update(pbar, advance=1)
