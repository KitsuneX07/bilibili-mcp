import os

from bilibili_api import favorite_list
from loguru import logger

from app import mcp
from app.utils.credential import CredentialManager


@mcp.tool()
async def create_video_favorite_list(title: str, introduction: str = "", private: bool = True) -> dict:
    cre = CredentialManager.get_instance()
    try:
        resp = await favorite_list.create_video_favorite_list(title=title, introduction=introduction, private=private, credential=cre)
        logger.info(f"Created favorite list : {resp}")
        return f"Favorite list {title} created successfully."

    except Exception as e:
        logger.error(f"Failed to create favorite list: {e}")
        return f"Failed to create favorite list: {e}"
