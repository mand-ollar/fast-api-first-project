from pydantic import BaseModel, ConfigDict, Field
from ulid import ULID

from core.auth.domain.enum import Role
from core.auth.domain.service import PasswordHasher


class Principal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ULID = Field(description="Unique domain identifier")
    user_id: ULID = Field(description="Unique user domain identifier")
    principal: str = Field(description="Login principal, e.g. username or email")
    password_hashed: str = Field(description="Stored password hash")
    role: Role = Field(description="User role")

    def verify_password(self, plain: str, hasher: PasswordHasher) -> bool:
        return hasher.verify(plain=plain, hashed=self.password_hashed)
