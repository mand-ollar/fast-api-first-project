from typing import Literal

from pydantic import BaseModel


class VerifyTokenResponse(BaseModel):
    username: str
    token_type: Literal["bearer"] = "bearer"
