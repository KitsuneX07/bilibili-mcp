import os
import difflib
from loguru import logger
from bilibili_api import favorite_list
from app.utils.credential import CredentialManager
from app.models.favorite_list import FavoriteListResponse

cre = CredentialManager.get_instance()


async def get_favorite_list_info() -> dict:
    resp = await favorite_list.get_video_favorite_list(uid=os.getenv("DEDEUSERID"), credential=cre)

    result = FavoriteListResponse.model_validate(resp).model_dump()
    return result


async def get_favorite_list_id_by_title(title: str) -> int:
    result = await get_favorite_list_info()
    title_to_id = {item["title"]: item["id"] for item in result["list"]}
    logger.debug(f"Title to ID mapping: {title_to_id}")
    if not title_to_id:
        return None

    matches = difflib.get_close_matches(title, title_to_id.keys(), n=1, cutoff=0.6)

    if not matches:
        return None

    closest_match_str = matches[0]
    return str(title_to_id[closest_match_str])
