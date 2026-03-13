from ulid import ULID  # type: ignore

from app.note.domain.entity import Note
from app.note.domain.repository import NoteRepository


class DeleteNoteUseCase:
    def __init__(self, note_repo: NoteRepository) -> None:
        self.note_repo: NoteRepository = note_repo

    def __call__(self, note_id: ULID) -> None:
        note: Note = self.note_repo.get_by_id(id=note_id)
        self.note_repo.delete(note=note)
