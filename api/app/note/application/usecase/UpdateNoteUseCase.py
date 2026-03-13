from app.note.application.command import UpdateNoteCommand
from app.note.domain.entity import Note
from app.note.domain.enum import NoteStatus
from app.note.domain.exception import InvalidDraftTransition
from app.note.domain.repository import NoteRepository, TagRepository


class UpdateNoteUseCase:
    def __init__(self, note_repo: NoteRepository, tag_repo: TagRepository) -> None:
        self.note_repo: NoteRepository = note_repo
        self.tag_repo: TagRepository = tag_repo

    def __call__(self, cmd: UpdateNoteCommand) -> Note:
        if cmd.status == NoteStatus.DRAFT:
            raise InvalidDraftTransition("Cannot update to draft note")

        note: Note = self.note_repo.get_by_id(id=cmd.id)

        has_changes: bool = False
        if cmd.title is not None and note.title != cmd.title:
            note.title = cmd.title
            has_changes = True

        if cmd.content is not None and note.content != cmd.content:
            note.content = cmd.content
            has_changes = True

        if cmd.tag_ids is not None and [tag.id for tag in note.tags] != cmd.tag_ids:
            note.tags = [self.tag_repo.get_by_id(id=tag_id) for tag_id in cmd.tag_ids]
            has_changes = True

        if cmd.status is not None and note.status != cmd.status:
            note.status = cmd.status
            has_changes = True

        if has_changes:
            note = self.note_repo.update(note=note)

        return note
