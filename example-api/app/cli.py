import typer
from rich import print
from sqlmodel import Session
from typer import Option

from app.dependencies.db import engine
from app.models.users import User
from app.pipelines.import_film_data import pipeline

app = typer.Typer()


@app.command(help="Create an admin user.")
def create_superuser(email: str, password: str):
    with Session(engine) as session:
        new_user: User = User(email=email, hashed_password=password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print(new_user)


@app.command(help="Imports the film data from the provided CSV")
def import_films(reset: bool = Option(default=False)) -> None:
    pipeline()


if __name__ == "__main__":
    app()
