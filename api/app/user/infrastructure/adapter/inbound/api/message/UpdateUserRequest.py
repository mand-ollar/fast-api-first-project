from pydantic import BaseModel
from ulid import ULID  # type: ignore

from app.user.application.command import UpdateUserCommand
from app.user.application.usecase import UpdateUserUseCase
from app.user.domain.entity import User


class UpdateUserRequest(BaseModel):
    username: str | None = None
    password: str | None = None

    def update(self, user_id: ULID, usecase: UpdateUserUseCase) -> User:
        return usecase(cmd=UpdateUserCommand(user_id=user_id, new_username=self.username, new_password=self.password))
