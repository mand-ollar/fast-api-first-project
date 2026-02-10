from app.user.domain.entity import User
from app.user.domain.repository.UserRepository import UserRepository


class GetUsersUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo: UserRepository = user_repo

    def __call__(self) -> list[User]:
        return self.user_repo.get()
