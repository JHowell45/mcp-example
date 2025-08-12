from rich import print
from rich.progress import Progress
from sqlalchemy import func
from sqlmodel import Session, delete, select

from app.dependencies.db import engine
from app.models.embeddings import FilmEmbedding, embedding_model
from app.models.films import Film


def pipeline(reset: bool, limit: int) -> None:
    with Progress() as progress:
        with Session(engine) as session:
            total_count: int = session.scalar(func.count(Film.id))
            if reset:
                print("Deleting the embeddings from the table...")
                session.exec(delete(FilmEmbedding))
                session.commit()
                print("Deleted all of the embeddings!")
            pbar = progress.add_task(
                "Creating embeddings for the film data", total=total_count
            )
            offset: int = 0
            while results := session.exec(
                select(Film).offset(offset).limit(limit)
            ).all():
                count: int = len(results)
                offset += count
                for model in results:
                    vector = embedding_model.encode(model.embedding_text)
                    db_model: FilmEmbedding = FilmEmbedding(
                        embedding=vector, film=model
                    )
                    print(db_model)
                    session.add(db_model)
                session.commit()
                progress.update(pbar, advance=count)
