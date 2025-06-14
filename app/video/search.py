from bilibili_api import search
from loguru import logger
from app import mcp
from app.models.video import SearchVideoResponse
from bilibili_api import search


@mcp.tool()
async def search_video(keyword: str, num_results: int = 10, descending: bool = True, order_type: search.OrderVideo = search.OrderVideo.TOTALRANK):
	"""Searches for videos on Bilibili based on a keyword.

	This function uses the Bilibili API to search for videos. It supports
	customizing the number of results, sorting order, and order type.

	Args:
	    keyword (str): The keyword to search for.
	    num_results (int, optional): The maximum number of results to return.
	        Defaults to 10.
	    descending (bool, optional): Whether to sort the results in descending
	        order. Defaults to True.
	    order_type (search.OrderVideo, optional): The type of order to apply to
	        the search results. This is an enumeration with the following possible values:
	        - search.OrderVideo.TOTALRANK: Sort by comprehensive ranking.
	        - search.OrderVideo.CLICK: Sort by most clicks.
	        - search.OrderVideo.PUBDATE: Sort by latest release date.
	        - search.OrderVideo.DM: Sort by most danmaku (bullet comments).
	        - search.OrderVideo.STOW: Sort by most favorites.
	        - search.OrderVideo.SCORES: Sort by most comments.
	        Defaults to search.OrderVideo.TOTALRANK.

	Returns:
	    dict: A dictionary containing the search results, validated against
	        the SearchVideoResponse model. The structure includes a list of
	        SearchVideoInfo objects.
	"""
	resp = await search.search_by_type(keyword=keyword, search_type=search.SearchObjectType.VIDEO, page=1, page_size=num_results, order_type=order_type, order_sort=0 if descending else 1)
	result = SearchVideoResponse.model_validate(resp).model_dump()
	logger.info(f"Search results for '{keyword}': {result}")
	return result
