import typer
from pandas import read_csv
from pydantic import BaseModel, Field
from rich import print
from sqlmodel import Session

from app.dependencies.db import engine
from app.models.films import Film
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
    certificate: str = Field(alias="Certificate")
    imdb_rating: float = Field(alias="IMDB_Rating", ge=0, le=10)
    meta_score: int = Field(alias="Meta_score", ge=0, le=100)
    director: str = Field(alias="Director")

    runtime_pre: str = Field(alias="Runtime", repr=False)
    genre_data: str = Field(alias="Genre", repr=False)

    def model_post_init(self, _) -> None:
        self.runtime_minutes: int = int(self.runtime_pre.split(" ")[0])
        self.genres: list[str] = self.genre_data.split(",")


@app.command(help="Imports the film data from the provided CSV")
def import_films():
    df = read_csv("/app/datasets/imdb_top_1000.csv")
    print(df)
    with Session(engine) as session:
        for row in df.iterrows():
            print(row)
            print(FilmData(**row.to_dict()))
            film: Film | None = None


if __name__ == "__main__":
    app()
