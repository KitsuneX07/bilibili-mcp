import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
from bilibili_api import comment

from app.utils.credential import CredentialManager
from app.video.video import get_aid_by_bvid
from app.models.video import VideoCommentResponse
import json
import pprint

cre = CredentialManager().get_instance()


async def get_video_comments(bvid: str, page_index: int = 1, time_order: bool = False):
	aid = await get_aid_by_bvid(bvid)
	resp = await comment.get_comments(oid=aid, type_=comment.CommentResourceType.VIDEO, page_index=page_index, order=comment.OrderType.TIME if time_order else comment.OrderType.LIKE, credential=cre)
	resp = VideoCommentResponse.model_validate(resp)
	pprint.pprint(resp.model_dump())
	with open(".cache/video_comments.json", "w", encoding="utf-8") as f:
		json.dump(resp.model_dump(), f, ensure_ascii=False, indent=4)


async def send_comment():
	raise NotImplementedError


async def reply_comment():
	raise NotImplementedError


if __name__ == "__main__":
	import asyncio

	asyncio.run(get_video_comments("BV1j1421Q7Wj", page_index=1, time_order=False))
	# asyncio.run(send_comment())
	# asyncio.run(reply_comment())
