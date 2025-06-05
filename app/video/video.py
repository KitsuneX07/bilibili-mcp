from bilibili_api import video
from app.utils import CredentialManager
from app import mcp
from typing import Optional
from loguru import logger


@mcp.tool()
async def like_video(bvid: Optional[str] = None, aid: Optional[int] = None, like: bool = True) -> None:
    """Manages liking or unliking a Bilibili video.

    Set 'like' to True to like the video, False to unlike it.
    This action modifies the user's like status for the video.
    Either bvid or aid must be provided.

    Args:
        bvid (Optional[str]): The BV ID of the video to like or unlike.
        aid (Optional[int]): The AV ID of the video to like or unlike.
        like (bool): Set to True to like the video, False to unlike it. Defaults to True.
    """
    if bvid is None and aid is None:
        logger.error("Error: Either bvid or aid must be provided.")
        return

    credential = CredentialManager.get_instance()
    if bvid:
        v = video.Video(bvid=bvid, credential=credential)
        video_identifier = bvid
    else:
        v = video.Video(aid=aid, credential=credential)
        video_identifier = aid

    try:
        await v.like(like)
        if like:
            logger.success(f"Successfully liked video: {video_identifier}")
        else:
            logger.success(f"Successfully unliked video: {video_identifier}")
        return    
    except Exception as e:
        logger.error(f"Operation failed for {video_identifier}: {e}")
        return

@mcp.tool()
async def get_video_info(bvid: Optional[str] = None, aid: Optional[int] = None) -> dict:
    """Retrieves detailed and basic information for a specified Bilibili video.

    This tool fetches both general video information and more comprehensive details.
    Either bvid or aid must be provided.

    Args:
        bvid (Optional[str]): The BV ID of the video.
        aid (Optional[int]): The AV ID of the video.

    Returns:
        dict: A dictionary containing two keys:
              'info' for basic video information (e.g., title, author),
              and 'detail' for more comprehensive video details.
    """
    if bvid is None and aid is None:
        logger.error("Error: Either bvid or aid must be provided.")
        return {}

    if bvid:
        v = video.Video(bvid=bvid)
        video_identifier = bvid
    else:
        v = video.Video(aid=aid)
        video_identifier = aid

    info = await v.get_info()
    detail = await v.get_detail()
    logger.info(f"Basic information of video {video_identifier}: {info}")
    logger.info(f"Detailed information of video {video_identifier}: {detail}")
    return {"info": info, "detail": detail}


@mcp.tool()
async def add_to_toview(bvid: Optional[str] = None, aid: Optional[int] = None) -> None:
    """Adds a Bilibili video to the user's "Watch Later" list.

    This action modifies the user's "Watch Later" list.
    Either bvid or aid must be provided.

    Args:
        bvid (Optional[str]): The BV ID of the video to add to the "Watch Later" list.
        aid (Optional[int]): The AV ID of the video to add to the "Watch Later" list.
    """
    if bvid is None and aid is None:
        logger.error("Error: Either bvid or aid must be provided.")
        return

    credential = CredentialManager.get_instance()
    if bvid:
        v = video.Video(bvid=bvid, credential=credential)
        video_identifier = bvid
    else:
        v = video.Video(aid=aid, credential=credential)
        video_identifier = aid

    try:
        await v.add_to_toview()
        logger.success(f"Successfully added video {video_identifier} to \"Watch Later\" list.")
        return
    except Exception as e:
        logger.success(f"Failed to add {video_identifier}: {e}")
        return


@mcp.tool()
async def delete_from_toview(bvid: Optional[str] = None, aid: Optional[int] = None) -> None:
    """Removes a Bilibili video from the user's "Watch Later" list.

    This action modifies the user's "Watch Later" list.
    Either bvid or aid must be provided.

    Args:
        bvid (Optional[str]): The BV ID of the video to remove from the "Watch Later" list.
        aid (Optional[int]): The AV ID of the video to remove from the "Watch Later" list.
    """
    if bvid is None and aid is None:
        logger.success("Error: Either bvid or aid must be provided.")
        return

    credential = CredentialManager.get_instance()
    if bvid:
        v = video.Video(bvid=bvid, credential=credential)
        video_identifier = bvid
    else:
        v = video.Video(aid=aid, credential=credential)
        video_identifier = aid

    try:
        await v.delete_from_toview()
        logger.success(f"Successfully removed video {video_identifier} from \"Watch Later\" list.")
    except Exception as e:
        logger.error(f"Failed to remove {video_identifier}: {e}")


@mcp.tool()
async def get_video_download_url(
    bvid: Optional[str] = None, aid: Optional[int] = None, cid: Optional[int] = None, page_index: Optional[int] = None
) -> Optional[dict]:
    """Retrieves the download URL for a Bilibili video.

    For multi-part videos, either 'cid' or 'page_index' must be provided to specify the part.
    If neither is provided for a multi-part video, it might default to the first part or fail.
    Either bvid or aid must be provided.

    Args:
        bvid (Optional[str]): The BV ID of the video.
        aid (Optional[int]): The AV ID of the video.
        cid (Optional[int]): The CID (part ID) of the video. Required for specific parts of multi-part videos if 'page_index' is not used.
        page_index (Optional[int]): The 1-based page index of the video part. Required for specific parts of multi-part videos if 'cid' is not used.

    Returns:
        Optional[dict]: A dictionary containing download link information, or None if the operation fails.
                        The dictionary typically includes URLs for different qualities.
    """
    if bvid is None and aid is None:
        logger.error("Error: Either bvid or aid must be provided.")
        return None

    if bvid:
        v = video.Video(bvid=bvid)
        video_identifier = bvid
    else:
        v = video.Video(aid=aid)
        video_identifier = aid

    try:
        download_url_info = await v.get_download_url(cid=cid, page_index=page_index)
        logger.info(f"Download link information for video {video_identifier}: {download_url_info}")
        return download_url_info
    except Exception as e:
        logger.error(f"Failed to get download link for {video_identifier}: {e}")
        return None

