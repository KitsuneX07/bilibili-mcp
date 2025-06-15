from bilibili_api import comment
from loguru import logger
from app import mcp
from app.utils.credential import CredentialManager
from app.video.video import get_aid_by_bvid
from app.models.video import VideoCommentResponse

cre = CredentialManager().get_instance()


@mcp.tool()
async def get_video_comments(bvid: str, page_index: int = 1, time_order: bool = False):
    """Retrieves comments for a given Bilibili video.

    This function fetches comments for a specified video BVID, supporting pagination
    and ordering by time or likes. It converts the BVID to an AID internally
    before making the API call.

    Args:
            bvid (str): The BVID (Bilibili Video ID) of the video.
            page_index (int, optional): The page number of comments to retrieve. Defaults to 1.
            time_order (bool, optional): If True, comments are ordered by time; otherwise, by likes.
                    Defaults to False.

    Returns:
            dict: A dictionary containing the video comments data, validated against
                    the VideoCommentResponse model.

    Side Effects:
            Logs information about the fetched comments, including the BVID, AID,
            page index, order, and the fetched data itself, using the configured logger.
    """
    aid = await get_aid_by_bvid(bvid)
    resp = await comment.get_comments(oid=aid, type_=comment.CommentResourceType.VIDEO, page_index=page_index, order=comment.OrderType.TIME if time_order else comment.OrderType.LIKE, credential=cre)
    result = VideoCommentResponse.model_validate(resp).model_dump()
    logger.info(f"Fetched comments for video {bvid} (aid: {aid}), page {page_index}, order {'time' if time_order else 'like'}")
    logger.info(f"Comments data: {result}")
    return result


@mcp.tool()
async def send_comment(bvid: str, message: str):
    """Sends a comment to a specified Bilibili video.

    This function allows users to post comments on a Bilibili video identified by its BVID.
    It internally converts the BVID to an AID before sending the comment via the Bilibili API.

    Args:
        bvid (str): The BVID (Bilibili Video ID) of the video to comment on.
        message (str): The content of the comment to be sent.

    Returns:
        dict: A dictionary containing the API response from sending the comment,
                typically indicating success or failure.
    """
    aid = await get_aid_by_bvid(bvid)
    resp = await comment.send_comment(text=message, oid=aid, type_=comment.CommentResourceType.VIDEO, credential=cre)
    logger.info(f"Sent comment to video {bvid} (aid: {aid}): {message}")
    return resp


async def reply_comment():
    raise NotImplementedError
