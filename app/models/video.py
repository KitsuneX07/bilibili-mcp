from pydantic import BaseModel, ConfigDict
from typing import List


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
	aid: str
	videos: int
	tname: str
	tname_v2: str
	title: str
	desc: str
	owner: VideoOwnerInfo
	pages: List[VideoPageInfo]

	model_config = ConfigDict(extra="ignore")
