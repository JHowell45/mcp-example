from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.dependencies.config import get_settings

settings = get_settings()
engine = create_engine(str(settings.DATABASE_URI))


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
