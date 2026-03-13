from ulid import ULID  # type: ignore

from app.user.domain.repository import UserRepository


class DeleteUserUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo: UserRepository = user_repo

    def __call__(self, user_id: ULID) -> None:
        self.user_repo.delete_by_id(user_id)
