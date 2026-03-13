from datetime import datetime

from ulid import ULID  # type: ignore

from app.note.domain.entity import Note
from app.note.domain.enum import NoteStatus
from app.note.domain.exception import NoteNotDraft
from app.note.domain.repository import NoteRepository


class CreateNoteUseCase:
    def __init__(self, note_repo: NoteRepository) -> None:
        self.note_repo: NoteRepository = note_repo

    def __call__(self, note_draft_id: ULID, title: str) -> Note:
        note_draft: Note = self.note_repo.get_by_id(id=note_draft_id)
        if note_draft.status != NoteStatus.DRAFT:
            raise NoteNotDraft

        now: datetime = datetime.now()

        note: Note = note_draft.model_copy(
            update={
                "title": title,
                "created_at": now,
                "updated_at": now,
                "status": NoteStatus.PUBLISHED,
            }
        )
        self.note_repo.update(note=note)

        return note
