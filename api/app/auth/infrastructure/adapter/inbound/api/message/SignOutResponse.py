from pydantic import BaseModel


class SignOutResponse(BaseModel):
    username: str
