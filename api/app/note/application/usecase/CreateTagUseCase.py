from datetime import datetime

from ulid import ULID  # type: ignore

from app.note.domain.entity import Tag
from app.note.domain.repository import TagRepository


class CreateTagUseCase:
    def __init__(self, tag_repo: TagRepository) -> None:
        self.tag_repo: TagRepository = tag_repo
        self.ulid: ULID = ULID()

    def __call__(self, name: str) -> Tag:
        now: datetime = datetime.now()

        tag: Tag = self.tag_repo.save(tag=Tag(id=self.ulid, name=name, created_at=now, updated_at=now))

        return tag
