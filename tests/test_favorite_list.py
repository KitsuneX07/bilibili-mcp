import os
import sys

from bilibili_api import favorite_list
from dotenv import load_dotenv
from loguru import logger


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
from app.utils.credential import CredentialManager

cre = CredentialManager.get_instance()
uid = os.getenv("DEDEUSERID")


async def test_create_favorite_list():
    resp = await favorite_list.create_video_favorite_list(title="Test Favorite List", introduction="This is a test favorite list.", private=True, credential=cre)
    id = resp.get("id")
    logger.info(f"Created favorite list with ID: {id}")


async def test_get_favorite_list():
    from app.favorite_list.favorite_list import get_favorite_list_info

    resp = await get_favorite_list_info()
    import pprint

    pprint.pprint(resp)


async def test_delete_favorite_list():
    resp = await favorite_list.delete_video_favorite_list(media_ids=[3533640315], credential=cre)
    logger.info(f"Deleted favorite list response: {resp}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_get_favorite_list())
