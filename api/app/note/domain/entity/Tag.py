from datetime import datetime

from pydantic import BaseModel
from ulid import ULID  # type: ignore


class Tag(BaseModel):
    id: ULID
    name: str
    created_at: datetime
    updated_at: datetime
