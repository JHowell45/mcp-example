from datetime import datetime, timezone

from sqlalchemy.sql import func
from sqlmodel import DateTime, Field, SQLModel


class DateTimestamps(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime,
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime,
        sa_column_kwargs={
            "onupdate": func.now(),
            "server_default": func.now(),
        },
        nullable=False,
    )
