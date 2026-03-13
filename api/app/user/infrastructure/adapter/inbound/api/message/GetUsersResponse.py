from pydantic import BaseModel

from .GetUserResponse import GetUserResponse


class GetUsersResponse(BaseModel):
    total_cnt: int
    page: int
    users: list[GetUserResponse]
