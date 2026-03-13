from pydantic import BaseModel, ConfigDict

from app.note.domain.entity import Tag


class GetTagsResponse(BaseModel):
    tags: list[Tag]

    model_config = ConfigDict(arbitrary_types_allowed=True)
