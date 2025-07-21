import typer
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


@app.command()
def test():
    pass


if __name__ == "__main__":
    app()
