from pydantic import BaseModel, ConfigDict
from ulid import ULID  # type: ignore


class UpdateTagCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ULID
    name: str | None = None
