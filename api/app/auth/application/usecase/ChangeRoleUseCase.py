from ulid import ULID  # type: ignore

from app.user.domain.entity import User
from app.user.domain.repository import UserRepository
from core.auth.domain.entity import Principal
from core.auth.domain.enum import Role
from core.auth.domain.repository import PrincipalRepository


class ChangeRoleUseCase:
    def __init__(self, principal_repo: PrincipalRepository, user_repo: UserRepository) -> None:
        self.principal_repo: PrincipalRepository = principal_repo
        self.user_repo: UserRepository = user_repo

    def __call__(self, user_id: ULID, role: Role) -> tuple[User, Principal]:
        user: User = self.user_repo.get_by_id(id=user_id)
        user.role = role
        user = self.user_repo.update(user=user)

        principal: Principal = self.principal_repo.get_by_user_id(user_id=user_id)
        principal.role = role
        principal = self.principal_repo.update(principal=principal)

        return user, principal
