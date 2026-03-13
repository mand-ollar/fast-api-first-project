from pydantic import BaseModel


class PatchTagRequest(BaseModel):
    name: str | None = None
