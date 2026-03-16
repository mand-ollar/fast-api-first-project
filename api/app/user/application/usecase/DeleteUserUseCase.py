from ulid import ULID  # type: ignore

from app.user.domain.repository import UserRepository
from core.auth.domain.repository import CredentialsRepository, PrincipalRepository


class DeleteUserUseCase:
    def __init__(
        self, user_repo: UserRepository, credentials_repo: CredentialsRepository, principal_repo: PrincipalRepository
    ) -> None:
        self.user_repo: UserRepository = user_repo
        self.credentials_repo: CredentialsRepository = credentials_repo
        self.principal_repo: PrincipalRepository = principal_repo

    def __call__(self, user_id: ULID) -> None:
        self.user_repo.delete_by_id(user_id)
        self.credentials_repo.delete_by_user_id(user_id)
        self.principal_repo.delete_by_user_id(user_id)
