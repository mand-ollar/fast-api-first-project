from pydantic import BaseModel


class PatchUserRequest(BaseModel):
    username: str | None = None
    password: str | None = None
