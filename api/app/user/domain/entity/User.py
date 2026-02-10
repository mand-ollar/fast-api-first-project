from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    email: str
    password: str
    memo: str | None
    created_at: datetime
    updated_at: datetime
