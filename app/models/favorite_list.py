from pydantic import BaseModel, ConfigDict
from typing import List


class FavoriteListInfo(BaseModel):
    id: int
    title: str
    media_count: int

    model_config = ConfigDict(extra="ignore")


class FavoriteListResponse(BaseModel):
    count: int
    list: List[FavoriteListInfo]

    model_config = ConfigDict(extra="ignore")
