import os

from bilibili_api import favorite_list
from loguru import logger

from app import mcp
from app.utils.credential import CredentialManager


@mcp.tool()
async def create_video_favorite_list(title: str, introduction: str = "", private: bool = True) -> dict:
	"""
	Creates a new video favorite list for the authenticated user.

	This tool allows the creation of a personalized collection of videos,
	which can be configured with a title, an optional introduction, and
	a privacy setting.

	:param title: The title of the new favorite list.
	:type title: str
	:param introduction: An optional introduction or description for the favorite list. Defaults to an empty string.
	:type introduction: str, optional
	:param private: A boolean indicating whether the favorite list should be private. Defaults to True.
	:type private: bool, optional
	:returns: A dictionary containing the response from the Bilibili API, typically including details of the newly created favorite list.
	:rtype: dict
	"""
	cre = CredentialManager.get_instance()
	resp = await favorite_list.create_video_favorite_list(title=title, introduction=introduction, private=private, credential=cre)
	logger.info(f"Created favorite list : {resp}")
	return resp


@mcp.tool()
async def get_my_video_favorite_list() -> dict:
	"""
	Retrieves the video favorite lists for the currently authenticated user.
	"""
	cre = CredentialManager.get_instance()
	uid = os.getenv("DEDEUSERID")
	if uid is None:
		# Handle case where DEDEUSERID is not set for authenticated user
		raise ValueError("Authenticated user ID (DEDEUSERID) not found.")
	resp = await favorite_list.get_video_favorite_list(uid=uid, credential=cre)
	logger.info(f"Retrieved favorite list for 'me': {resp}")
	return resp


@mcp.tool()
async def get_specific_video_favorite_list(uid: int) -> dict:
	"""
	Retrieves video favorite lists for a specified user ID.
	:param uid: The user ID (UID) for whom to retrieve the favorite lists.
	:type uid: int
	:returns: A dictionary containing the response from the Bilibili API.
	:rtype: dict
	"""
	cre = CredentialManager.get_instance()
	resp = await favorite_list.get_video_favorite_list(uid=uid, credential=cre)
	logger.info(f"Retrieved favorite list for UID {uid}: {resp}")
	return resp


@mcp.tool()
async def delete_video_favorite_list_by_id(list_ids: list[int]) -> dict:
	"""
	Deletes video favorite lists by their IDs.

	:param list_ids: A list of IDs of the favorite lists to be deleted.
	:type list_ids: list[int]
	:returns: A dictionary containing the response from the Bilibili API.
	:rtype: dict
	"""
	cre = CredentialManager.get_instance()
	resp = await favorite_list.delete_video_favorite_list(media_ids=list_ids, credential=cre)
	logger.info(f"Deleted favorite lists with IDs {list_ids}: {resp}")
	return resp


@mcp.tool()
async def delete_video_favorite_list_by_name(names: list[str] = None) -> dict:
	"""
	Deletes video favorite lists by their names.

	:param names: A list of names of the favorite lists to be deleted. If None, all favorite lists will be deleted.
	:type names: list[str], optional
	:returns: A dictionary containing the response from the Bilibili API.
	:rtype: dict
	"""
	cre = CredentialManager.get_instance()
	favorite_lists = await favorite_list.get_video_favorite_list(uid=os.getenv("DEDEUSERID"), credential=cre)
	fl_to_del = []
	for fl in favorite_lists.get("list", []):
		if names is None or fl.get("title") in names:
			fl_to_del.append(fl.get("id"))

	if fl_to_del:
		logger.info(f"Deleting favorite lists with IDs: {fl_to_del}")
		resp = await favorite_list.delete_video_favorite_list(media_ids=fl_to_del, credential=cre)
		logger.info(f"Deleted favorite lists with names {names}: {resp}")
		return resp

	return "No favorite lists to delete." if names else f"No favorite lists found with names {names}."
