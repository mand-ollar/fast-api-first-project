from app.user.application.command import UpdateUserCommand
from app.user.domain.entity import User
from app.user.domain.repository import UserRepository
from core.util import BcryptPasswordHasher


class UpdateUserUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo: UserRepository = user_repo
        self.password_hasher: BcryptPasswordHasher = BcryptPasswordHasher()

    def __call__(self, cmd: UpdateUserCommand) -> User:
        user: User = self.user_repo.get_by_id(id=cmd.user_id)

        has_changes: bool = False

        if cmd.new_username is not None and user.username != cmd.new_username:
            user.username = cmd.new_username
            has_changes = True

        if cmd.new_password is not None and user.password != (
            new_password := self.password_hasher.hash(cmd.new_password)
        ):
            user.password = new_password
            has_changes = True

        if has_changes:
            self.user_repo.save(user=user)

        return user
