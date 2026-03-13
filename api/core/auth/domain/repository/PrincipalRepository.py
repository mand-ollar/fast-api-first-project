from abc import ABC, abstractmethod

from ulid import ULID

from core.auth.domain.entity import Principal


class PrincipalRepository(ABC):
    @abstractmethod
    def get_by_principal(self, principal: str) -> Principal:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: ULID) -> Principal:
        raise NotImplementedError

    @abstractmethod
    def exists(self, principal: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, principal: Principal) -> Principal:
        raise NotImplementedError

    @abstractmethod
    def update(self, principal: Principal) -> Principal:
        raise NotImplementedError
