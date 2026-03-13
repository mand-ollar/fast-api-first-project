from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # type: ignore

from app.note.domain.entity import Note, Tag
from app.note.domain.enum import NoteStatus
from app.note.domain.valueobject import Content


class BaseNoteResponse(BaseModel):
    id: ULID
    title: str
    content: Content
    created_at: datetime
    updated_at: datetime
    created_by: ULID
    updated_by: ULID
    tags: list[Tag]
    status: NoteStatus

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_model(cls, note: Note) -> Self:
        return cls(
            id=note.id,
            title=note.title,
            content=note.content,
            created_at=note.created_at,
            updated_at=note.updated_at,
            created_by=note.created_by,
            updated_by=note.updated_by,
            tags=note.tags,
            status=note.status,
        )
