from ulid import ULID

from app.user.domain.entity import User
from app.user.domain.repository import UserRepository
from core.auth.domain.service import AuthenticationService


class SignOutUseCase:
    def __init__(self, auth_service: AuthenticationService, user_repo: UserRepository) -> None:
        self.auth_service: AuthenticationService = auth_service
        self.user_repo: UserRepository = user_repo

    def __call__(
        self,
        raw_short_lived_confidential: str,
        raw_long_lived_confidential: str | None = None,
    ) -> User:
        user_id: ULID = self.auth_service.verify(raw_short_lived_confidential)
        self.auth_service.revoke(raw_short_lived_confidential)

        if raw_long_lived_confidential:
            self.auth_service.revoke(raw_long_lived_confidential)

        user: User = self.user_repo.get_by_id(id=user_id)

        return user
