from pydantic import BaseModel
from ulid import ULID

from core.auth.domain.enum import CredentialType


class Credentials(BaseModel):
    user_id: ULID
    type: CredentialType
    raw_value: str
