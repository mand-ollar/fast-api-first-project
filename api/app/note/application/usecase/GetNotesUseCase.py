from app.note.domain.entity import Note
from app.note.domain.repository import NoteRepository


class GetNotesUseCase:
    def __init__(self, note_repo: NoteRepository) -> None:
        self.note_repo: NoteRepository = note_repo

    def __call__(self, page: int, items_per_page: int) -> tuple[int, list[Note]]:
        return self.note_repo.get(page=page, items_per_page=items_per_page)
