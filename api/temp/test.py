from datetime import datetime

from sqlalchemy import JSON, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID  # type: ignore

from app.note.domain.entity import Tag
from app.note.domain.enum import NoteStatus
from core.db.db import Base


class NoteAlchemyEntity(Base):
    __tablename__: str = "Note"

    id: Mapped[str] = mapped_column(String(26), primary_key=True, default=lambda: str(ULID()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    created_by: Mapped[ULID] = mapped_column(String(26), nullable=False)
    updated_by: Mapped[ULID] = mapped_column(String(26), nullable=False)
    tags: Mapped[list[Tag]] = mapped_column(JSON, nullable=False, default=[])
    status: Mapped[NoteStatus] = mapped_column(String(255), nullable=False, default=NoteStatus.DRAFT)


if __name__ == "__main__":
    note: NoteAlchemyEntity = NoteAlchemyEntity(
        id="123",
        title="test",
        content="test",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        created_by="123",
        updated_by="123",
        tags=[],
        status=NoteStatus.DRAFT,
    )
    print(getattr(note, "ide"))
