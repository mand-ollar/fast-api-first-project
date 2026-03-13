from abc import ABC, abstractmethod

from ulid import ULID  # type: ignore

from app.note.domain.entity import Tag


class TagRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: ULID) -> Tag:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Tag:
        raise NotImplementedError

    @abstractmethod
    def save(self, tag: Tag) -> Tag:
        raise NotImplementedError

    @abstractmethod
    def delete(self, tag: Tag) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, tag: Tag) -> Tag:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Tag]:
        raise NotImplementedError
