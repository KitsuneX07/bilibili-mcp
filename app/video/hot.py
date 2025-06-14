from bilibili_api import hot
from loguru import logger
from app import mcp
from app.models.video import HotVideoResponse


@mcp.tool()
async def get_hot_videos(num_videos: int = 10) -> dict:
	"""Retrieves a list of hot videos from Bilibili.

	Args:
		num_videos (int, optional): The number of hot videos to retrieve.
			Defaults to 10.

	Returns:
		dict: A dictionary containing the hot video information.
			The structure is validated against HotVideoResponse model.

	Side Effects:
		Logs the number of retrieved videos and their details using loguru.
	"""
	resp = await hot.get_hot_videos(pn=1, ps=num_videos)
	result = HotVideoResponse.model_validate(resp).model_dump()
	logger.info(f"Retrieved {num_videos} hot videos: {result}")
	return result
