from datetime import datetime

from pydantic import BaseModel
from ulid import ULID  # type: ignore

from app.note.domain.entity import Tag
from app.note.domain.enum import NoteStatus
from app.note.domain.valueobject import Content


class PatchNoteResponse(BaseModel):
    title: str
    content: Content
    updated_at: datetime
    updated_by: ULID
    tags: list[Tag]
    status: NoteStatus
