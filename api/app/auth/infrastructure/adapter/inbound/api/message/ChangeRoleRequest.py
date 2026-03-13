from pydantic import BaseModel

from core.auth.domain.enum import Role


class ChangeRoleRequest(BaseModel):
    role: Role
