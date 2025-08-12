from rich.progress import Progress
from sqlmodel import Session

from app.dependencies.db import engine


def pipeline(reset: bool) -> None:
    with Progress() as progress:
        with Session(engine) as session:
            pass
