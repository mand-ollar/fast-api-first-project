from pydantic import BaseModel


class CreateTagResponse(BaseModel):
    name: str
