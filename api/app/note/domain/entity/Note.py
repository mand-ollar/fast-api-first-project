from datetime import datetime

from pydantic import BaseModel, ConfigDict
from ulid import ULID

from app.note.domain.enum import NoteStatus
from app.note.domain.valueobject import Content

from .Tag import Tag


class Note(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ULID
    title: str
    content: Content
    created_at: datetime
    updated_at: datetime
    created_by: ULID
    updated_by: ULID
    tags: list[Tag]
    status: NoteStatus
