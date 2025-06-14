from bilibili_api import video
from typing import List
from app import mcp
from app.utils.credential import CredentialManager
from app.models.video import VideoInfo
from bilibili_api import video

cre = CredentialManager.get_instance()


async def get_aid_by_bvid(bvid: str) -> int:
	v = video.Video(bvid=bvid, credential=cre)
	return v.get_aid()


async def get_bvid_by_aid(aid: int) -> str:
	v = video.Video(aid=aid, credential=cre)
	return v.get_bvid()


async def get_cid(bvid: str, page_index: int = 0) -> int:
	v = video.Video(bvid=bvid, credential=cre)
	return v.get_cid(page_index=page_index)


async def set_video_favorite(bvid: str, add_media_ids: List[int] = [], del_media_ids: List[int] = []) -> dict:
	v = video.Video(bvid=bvid, credential=cre)
	return await v.set_favorite(add_media_ids=add_media_ids, del_media_ids=del_media_ids)


@mcp.tool()
async def get_video_info(bvid: str) -> dict:
	"""Retrieves detailed information about a Bilibili video.

	Args:
		bvid (str): The Bilibili video ID (BV ID).

	Returns:
		dict: A dictionary containing various details about the video.
	"""
	v = video.Video(bvid=bvid, credential=cre)
	resp = await v.get_info()
	return VideoInfo.model_validate(resp).model_dump()


@mcp.tool()
async def get_video_download_url(bvid: str, page_index: int = 0) -> dict:
	"""Retrieves the download URL for a specific Bilibili video.

	Args:
		bvid (str): The Bilibili video ID (BV ID).
		page_index (int, optional): The index of the video page (for multi-part videos). Defaults to 0.

	Returns:
		dict: A dictionary containing the detected download URLs and related information.
	"""
	v = video.Video(bvid=bvid, credential=cre)
	dl = video.VideoDownloadURLDataDetecter(await v.get_download_url(page_index=page_index))
	return dl.detect_all()


@mcp.tool()
async def pay_video_coin(bvid: str, num: int = 1, like: bool = False) -> dict:
	"""Pays coins to a Bilibili video.

	Args:
		bvid (str): The Bilibili video ID (BV ID).
		num (int, optional): The number of coins to pay (1 or 2). Defaults to 1.
		like (bool, optional): Whether to like the video after paying coins. Defaults to False.

	Returns:
		dict: A dictionary containing the result of the coin payment operation.
	"""
	v = video.Video(bvid=bvid, credential=cre)
	return await v.pay_coin(num=num, like=like)


@mcp.tool()
async def triple_video(bvid: str) -> dict:
	"""Performs a "triple" action (like, coin, favorite) on a Bilibili video.

	Args:
		bvid (str): The Bilibili video ID (BV ID).

	Returns:
		dict: A dictionary containing the result of the triple operation.
	"""
	v = video.Video(bvid=bvid, credential=cre)
	return await v.triple()


@mcp.tool()
async def add_video_to_toview(bvid: str) -> dict:
	"""Adds a Bilibili video to the "Watch Later" list.

	Args:
		bvid (str): The Bilibili video ID (BV ID).

	Returns:
		dict: A dictionary containing the result of the add to "Watch Later" operation.
	"""
	v = video.Video(bvid=bvid, credential=cre)
	await v.add_to_toview()


@mcp.tool()
async def delete_video_from_toview(bvid: str) -> dict:
	"""Deletes a Bilibili video from the "Watch Later" list.

	Args:
		bvid (str): The Bilibili video ID (BV ID).

	Returns:
		dict: A dictionary containing the result of the delete from "Watch Later" operation.
	"""
	v = video.Video(bvid=bvid, credential=cre)
	await v.delete_from_toview()


@mcp.tool()
async def like_video(bvid: str, like: bool = True) -> dict:
	"""Likes or unlikes a Bilibili video.

	Args:
		bvid (str): The Bilibili video ID (BV ID).
		like (bool, optional): True to like the video, False to unlike. Defaults to True.

	Returns:
		dict: A dictionary containing the result of the like/unlike operation.
	"""
	v = video.Video(bvid=bvid, credential=cre)
	return await v.like(like=like)
