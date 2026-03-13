from pydantic import BaseModel
from ulid import ULID  # type: ignore


class CreateNoteDraftRequest(BaseModel):
    created_by: ULID
