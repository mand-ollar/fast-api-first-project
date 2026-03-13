from pydantic import BaseModel, ConfigDict

from .GetNoteResponse import GetNoteResponse


class GetNotesResponse(BaseModel):
    total_cnt: int
    page: int
    notes: list[GetNoteResponse]

    model_config = ConfigDict(arbitrary_types_allowed=True)
