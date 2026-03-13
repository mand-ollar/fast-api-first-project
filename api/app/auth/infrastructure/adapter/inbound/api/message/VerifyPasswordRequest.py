from pydantic import BaseModel


class VerifyPasswordRequest(BaseModel):
    principal_str: str
    password: str
