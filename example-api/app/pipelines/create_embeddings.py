from rich.progress import Progress
from sqlalchemy import func
from sqlmodel import Session, select

from app.dependencies.db import engine
from app.models.embeddings import FilmEmbedding, embedding_model
from app.models.films import Film


def pipeline(reset: bool, limit: int) -> None:
    with Progress() as progress:
        with Session(engine) as session:
            pbar = progress.add_task(
                "Creating embeddings for the film data",
                total=session.exec(func.count(Film.id)).one(),
            )
            offset: int = 0
            while results := session.exec(
                select(Film).offset(offset).limit(limit)
            ).all():
                count: int = len(results)
                offset += count
                for model in results:
                    vector = embedding_model.encode(model.embedding_text)
                    session.add(FilmEmbedding(embedding=vector, film=model))
                session.commit()
                progress.update(pbar, advance=count)
