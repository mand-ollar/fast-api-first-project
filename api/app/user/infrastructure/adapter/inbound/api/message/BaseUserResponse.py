from typing import Self

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # type: ignore

from app.user.domain.entity import User


class BaseUserResponse(BaseModel):
    id: ULID
    username: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_model(cls, user: User) -> Self:
        return cls(
            id=user.id,
            username=user.username,
        )
