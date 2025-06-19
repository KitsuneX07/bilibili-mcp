from bilibili_api import favorite_list, video
from loguru import logger

from app import mcp
from app.utils.credential import CredentialManager
from app.favorite_list.favorite_list import get_favorite_list_id_by_title


@mcp.tool()
async def create_video_favorite_list(title: str, introduction: str = "", private: bool = True) -> dict:
    """Creates a new video favorite list.

    Args:
        title (str): The title of the favorite list.
        introduction (str, optional): The introduction or description of the favorite list. Defaults to "".
        private (bool, optional): Whether the favorite list is private. Defaults to True.

    Returns:
        str: A message indicating the success or failure of the operation.
    """
    cre = CredentialManager.get_instance()
    try:
        resp = await favorite_list.create_video_favorite_list(title=title, introduction=introduction, private=private, credential=cre)
        logger.info(f"Created favorite list : {resp}")
        return f"Favorite list {title} created successfully."

    except Exception as e:
        logger.error(f"Failed to create favorite list: {e}")
        return f"Failed to create favorite list: {e}"


@mcp.tool()
async def delete_video_favorite_list(favorite_list_name: str) -> dict:
    """Deletes a video favorite list by its name.

    Args:
        favorite_list_name (str): The name of the favorite list to delete.

    Returns:
        str: A message indicating the success or failure of the operation.
    """
    cre = CredentialManager.get_instance()
    try:
        mid = await get_favorite_list_id_by_title(favorite_list_name)
        if mid is None:
            return f"Favorite list {favorite_list_name} not found."

        resp = await favorite_list.delete_video_favorite_list(media_ids=[mid], credential=cre)
        logger.info(f"Deleted favorite list with ID {mid}: {resp}")

        return f"Favorite list(s) {favorite_list_name} deleted successfully."

    except Exception as e:
        logger.error(f"Failed to delete favorite list with ID {favorite_list_name}: {e}")
        return f"Failed to delete favorite list with ID {favorite_list_name}: {e}"


@mcp.tool()
async def set_video_favorite(bvid: str, favorite_list_name: str) -> dict:
    """Adds a video to a specified favorite list.

    Args:
        bvid (str): The BVID of the video to add.
        favorite_list_name (str): The name of the favorite list to add the video to.

    Returns:
        str: A message indicating the success or failure of the operation.
    """
    cre = CredentialManager.get_instance()
    try:
        mid = await get_favorite_list_id_by_title(favorite_list_name)
        if mid is None:
            return f"Favorite list {favorite_list_name} not found."

        v = video.Video(bvid=bvid, credential=cre)
        logger.debug(f"Adding video {bvid} to favorite list {favorite_list_name} with ID {mid}")
        resp = await v.set_favorite(add_media_ids=[mid])
        logger.info(f"Added video {bvid} to favorite list {favorite_list_name}: {resp}")
        return f"Video {bvid} added to favorite list {favorite_list_name} successfully."

    except Exception as e:
        logger.error(f"Failed to add video {bvid} to favorite list {favorite_list_name}: {e}")
        return f"Failed to add video {bvid} to favorite list {favorite_list_name}: {e}"


@mcp.tool()
async def unset_video_favorite(bvid: str, favorite_list_name: str) -> dict:
    """Removes a video from a specified favorite list.

    Args:
        bvid (str): The BVID of the video to remove.
        favorite_list_name (str): The name of the favorite list to remove the video from.

    Returns:
        str: A message indicating the success or failure of the operation.
    """
    cre = CredentialManager.get_instance()
    try:
        mid = await get_favorite_list_id_by_title(favorite_list_name)
        if mid is None:
            return f"Favorite list {favorite_list_name} not found."

        v = video.Video(bvid=bvid, credential=cre)
        logger.debug(f"Removing video {bvid} from favorite list {favorite_list_name} with ID {mid}")
        resp = await v.set_favorite(del_media_ids=[mid])
        logger.info(f"Removed video {bvid} from favorite list {favorite_list_name}: {resp}")
        return f"Video {bvid} removed from favorite list {favorite_list_name} successfully."

    except Exception as e:
        logger.error(f"Failed to remove video {bvid} from favorite list {favorite_list_name}: {e}")
        return f"Failed to remove video {bvid} from favorite list {favorite_list_name}: {e}"
