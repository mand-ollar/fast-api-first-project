from pydantic import BaseModel


class UpdateUserResponse(BaseModel):
    username: str
    password: str
