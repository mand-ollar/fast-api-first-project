from app.note.application.command import UpdateTagCommand
from app.note.domain.entity import Tag
from app.note.domain.repository import TagRepository


class UpdateTagUseCase:
    def __init__(self, tag_repo: TagRepository) -> None:
        self.tag_repo: TagRepository = tag_repo

    def __call__(self, cmd: UpdateTagCommand) -> Tag:
        tag: Tag = self.tag_repo.get_by_id(id=cmd.id)

        has_changes: bool = False

        if cmd.name is not None and tag.name != cmd.name:
            tag.name = cmd.name
            has_changes = True

        if has_changes:
            tag = self.tag_repo.update(tag=tag)

        return tag
