import numpy as np
import typer
from pandas import read_csv
from pydantic import BaseModel, Field
from rich import print
from rich.progress import Progress
from sqlmodel import Session, select

from app.dependencies.db import engine
from app.models.films import Film, FilmDirector
from app.models.users import User

app = typer.Typer()


@app.command(help="Create an admin user.")
def create_superuser(email: str, password: str):
    with Session(engine) as session:
        new_user: User = User(email=email, hashed_password=password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print(new_user)


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


@app.command(help="Imports the film data from the provided CSV")
def import_films() -> None:
    df = read_csv("/app/datasets/imdb_top_1000.csv")
    print(df)
    with Progress() as progress:
        pbar = progress.add_task("Importing Film CSV Data...", total=df.shape[0])
        with Session(engine) as session:
            for row in df.iterrows():
                row = row[1].replace({np.nan: None})
                data = FilmData(**row.to_dict())
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


if __name__ == "__main__":
    app()
