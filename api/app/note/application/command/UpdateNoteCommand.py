from pydantic import BaseModel, ConfigDict
from ulid import ULID  # type: ignore

from app.note.domain.enum import NoteStatus
from app.note.domain.valueobject import Content


class UpdateNoteCommand(BaseModel):
    id: ULID
    user_id: ULID
    title: str | None = None
    content: Content | None = None
    tag_ids: list[ULID] | None = None
    status: NoteStatus | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
