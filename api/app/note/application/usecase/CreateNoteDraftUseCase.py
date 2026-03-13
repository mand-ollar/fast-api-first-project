from datetime import datetime

from ulid import ULID  # type: ignore

from app.note.domain.entity import Note
from app.note.domain.enum import NoteStatus
from app.note.domain.repository import NoteRepository, TagRepository
from app.note.domain.valueobject import Content


class CreateNoteDraftUseCase:
    def __init__(self, note_repo: NoteRepository, tag_repo: TagRepository) -> None:
        self.note_repo: NoteRepository = note_repo
        self.tag_repo: TagRepository = tag_repo
        self.ulid: ULID = ULID()

    def __call__(self, user_id: ULID) -> Note:
        now: datetime = datetime.now()

        note: Note = Note(
            id=self.ulid,
            title="",
            content=Content(text=""),
            created_at=now,
            updated_at=now,
            created_by=user_id,
            updated_by=user_id,
            tags=[],
            status=NoteStatus.DRAFT,
        )
        self.note_repo.save(note=note)

        return note
