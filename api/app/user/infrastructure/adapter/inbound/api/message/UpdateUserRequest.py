from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    username: str | None = None
    password: str | None = None
