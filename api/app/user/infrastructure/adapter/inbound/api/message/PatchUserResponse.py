from pydantic import BaseModel


class PatchUserResponse(BaseModel):
    username: str
    password: str
