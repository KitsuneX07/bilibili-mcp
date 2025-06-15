from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional


class SearchVideoInfo(BaseModel):
    author: str
    mid: int
    arcurl: str
    aid: int
    bvid: str
    title: str
    description: str
    tag: str
    duration: str

    model_config = ConfigDict(extra="ignore")


class SearchVideoResponse(BaseModel):
    result: List[SearchVideoInfo]

    model_config = ConfigDict(extra="ignore")


class VideoOwnerInfo(BaseModel):
    mid: int
    name: str

    model_config = ConfigDict(extra="ignore")


class VideoPageInfo(BaseModel):
    cid: int
    part: str

    model_config = ConfigDict(extra="ignore")


class VideoInfo(BaseModel):
    bvid: str
    aid: int
    videos: int
    tname: str
    tname_v2: str
    title: str
    desc: str
    owner: VideoOwnerInfo
    pages: List[VideoPageInfo]

    model_config = ConfigDict(extra="ignore")


class HotVideoRcmdReason(BaseModel):
    content: str

    model_config = ConfigDict(extra="ignore")


class HotVideoInfo(BaseModel):
    aid: int
    bvid: str
    title: str
    desc: str
    owner: VideoOwnerInfo
    short_link_v2: str
    rcmd_reason: HotVideoRcmdReason

    model_config = ConfigDict(extra="ignore")


class HotVideoResponse(BaseModel):
    list: List[HotVideoInfo]

    model_config = ConfigDict(extra="ignore")


class VideoCommentContent(BaseModel):
    message: str

    model_config = ConfigDict(extra="ignore")


class VideoCommentInfo(BaseModel):
    oid: int
    type: int
    root: int
    parent: int
    like: int
    content: VideoCommentContent
    replies: Optional[List["VideoCommentInfo"]] = None

    model_config = ConfigDict(extra="ignore")


class VideoCommentResponse(BaseModel):
    replies: List[VideoCommentInfo] = []

    model_config = ConfigDict(extra="ignore")
