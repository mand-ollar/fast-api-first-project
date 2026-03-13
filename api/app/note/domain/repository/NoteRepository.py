from abc import ABC, abstractmethod

from ulid import ULID

from app.note.domain.entity import Note


class NoteRepository(ABC):
    @abstractmethod
    def get(self, page: int, items_per_page: int) -> tuple[int, list[Note]]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: ULID) -> Note:
        raise NotImplementedError

    @abstractmethod
    def save(self, note: Note) -> Note:
        raise NotImplementedError

    @abstractmethod
    def update(self, note: Note) -> Note:
        raise NotImplementedError

    @abstractmethod
    def delete(self, note: Note) -> None:
        raise NotImplementedError
