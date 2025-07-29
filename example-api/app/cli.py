import typer
from pandas import read_csv
from rich import print
from sqlmodel import Session

from app.dependencies.db import engine
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


@app.command(help="Imports the film data from the provided CSV")
def import_films():
    df = read_csv("/app/datasets/imdb_top_1000.csv")
    print(df)


if __name__ == "__main__":
    app()
