from abc import ABC, abstractmethod

from core.auth.domain.valueobject import Credentials


class CredentialsRepository(ABC):
    @abstractmethod
    def save(self, creds: Credentials) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self, creds: Credentials) -> bool:
        raise NotImplementedError

    @abstractmethod
    def revoke(self, creds: Credentials) -> None:
        raise NotImplementedError
