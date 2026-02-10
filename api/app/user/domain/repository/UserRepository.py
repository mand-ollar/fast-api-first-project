from abc import ABC, abstractmethod

from ulid import ULID  # type: ignore

from app.user.domain.entity import User


class UserRepository(ABC):
    @abstractmethod
    def get(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: ULID) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError
