from pydantic import BaseModel

from core.auth.domain.enum import Role


class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str
    memo: str | None = None
    role: Role = Role.USER
