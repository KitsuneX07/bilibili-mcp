from bilibili_api import search
import pprint
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


async def test():
	resp = await search.search_by_type(keyword="村民交易所", search_type=search.SearchObjectType.VIDEO, page=1, page_size=2)
	resp = SearchVideoResponse.model_validate(resp)
	pprint.pprint(resp.model_dump())


if __name__ == "__main__":
	import asyncio

	asyncio.run(test())
