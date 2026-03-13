from app.note.domain.entity import Tag
from app.note.domain.repository import TagRepository


class ListTagsUseCase:
    def __init__(self, tag_repo: TagRepository) -> None:
        self.tag_repo: TagRepository = tag_repo

    def __call__(self) -> list[Tag]:
        return self.tag_repo.get_all()
