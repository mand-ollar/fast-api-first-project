from datetime import datetime

from pydantic import BaseModel


class PatchTagResponse(BaseModel):
    name: str
    updated_at: datetime
