from datetime import datetime

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # type: ignore


class User(BaseModel):
    id: ULID
    username: str
    email: str
    password: str
    memo: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)
