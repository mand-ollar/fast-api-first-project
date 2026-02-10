from pydantic import BaseModel, ConfigDict
from ulid import ULID  # type: ignore


class UpdateUserCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id: ULID
    new_username: str | None
    new_password: str | None
