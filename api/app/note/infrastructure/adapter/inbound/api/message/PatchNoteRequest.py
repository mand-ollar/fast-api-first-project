from pydantic import BaseModel
from ulid import ULID  # type: ignore

from app.note.domain.enum import NoteStatus
from app.note.domain.valueobject import Content


class PatchNoteRequest(BaseModel):
    user_id: ULID
    title: str | None = None
    content: Content | None = None
    tag_ids: list[ULID] | None = None
    status: NoteStatus | None = None
