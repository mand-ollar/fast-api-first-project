from pydantic import BaseModel
from ulid import ULID  # type: ignore


class CreateNoteRequest(BaseModel):
    note_draft_id: ULID
    title: str
